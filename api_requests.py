from yahoo_fin import stock_info as si
import requests
import json
from datetime import datetime
import pprint
import pandas as pd

class Td():
    '''
    Utility class that will be used to interract with the
    TD Ameritrade API endpoints and pool historical price data
    for every ticker in the s&p 500, nasdaq, and dow jones.
    
    Additionally, contains a create_files method that creates a file for every
    ticker mentioned above, with each file containing a dataframe
    of the data that the get request returned.
    '''
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory'
    params = ''

    def __init__(self, apikey, period_type, period, frequency_type, frequency):
        '''
        Initializes the endpoint and parameters of the search that will be used on that endpoint.
        Possible values:
            period_types: day, month, year, or ytd.

        For each period_type,
            periods: day: 1, 2, 3, 4, 5, 10
                    month: 1, 2, 3, 6
                    year: 1, 2, 3, 5, 10, 15, 20
                    ytd: 1
            frequency_types: day: minute
                            month: daily, weekly
                            year: daily, weekly, monthly
                            ytd: daily, weekly

        For each frequency_type,
            frequency:  minute: 1, 5, 10, 15, 30
                        daily: 1
                        weekly: 1
                        monthly: 1
        '''
        self.params = {'apikey' : apikey,
                        'periodType' : period_type,
                        'period' : period,
                        'frequencyType' : frequency_type,
                        'frequency' : frequency}


    def get_tickers_set(self):
        '''
        Gets all stock tickers in sp500, nasdaq, and dow indices.

        Input: none.
        Output: a set containing ticker symbols that exist on yahoo finance.
        '''
        df1 = pd.DataFrame( si.tickers_sp500() )
        df2 = pd.DataFrame( si.tickers_nasdaq() )
        df3 = pd.DataFrame( si.tickers_dow() )

        sym1 = set( symbol for symbol in df1[0].values.tolist() )
        sym2 = set( symbol for symbol in df2[0].values.tolist() )
        sym3 = set( symbol for symbol in df3[0].values.tolist() )

        symbols = set.union( sym1, sym2, sym3 )
        avoid_endings = ['W', 'R', 'P', 'Q']
        sav_set = set()

        for symbol in symbols:
            if not (len(symbol) > 4 and symbol[-1] in avoid_endings):
                sav_set.add( symbol )

        return sav_set

    def get_endpoint_data(self, endpoint, params):
        '''
        Performs get request on the endpoint with given parameters.

        Input: endpoint URL, dictionary of search parameters.
        Output: returns a dictionary of returned values if request successful.
                the dictionary contains data for the
                high, low, open, close, volume, and datetime columns
                returns none otherwise.
        '''
        print('>>>GETTING DATA FROM ' + str(endpoint), end='')
        try:
            page = requests.get(url=endpoint, params=params)
        except requests.RequestException as request_exception:
            print(request_exception)

        if page.status_code == 200:
            return json.loads(page.content)

        print('>>>BAD REQUEST ERROR. PAGE STATUS = ' + str(page.status_code))
        return None

    def reformat_dates(self, content):
        '''
        Changes unix timestamp format to readable date format.

        Input: dictionary containing a 'datetime' column of unix timestamp values.
        Output: returns a modified dictionary.
        '''
        for item in content['candles']:
            item['datetime'] = datetime.utcfromtimestamp(item['datetime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

    def get_ticker(self, ticker):
        '''
        Uses get_endpoint_data() on a single ticker symbol.

        Input: string containing the symbol of a ticker.
        Output: if request successful: returns a single dictionary containing
                the high, low, open, close, volume, and datetime columns
                for a given ticker in set returned by get_tickers_set().
                returns none otherwise.
        '''
        result = self.get_endpoint_data(self.endpoint.format(ticker=ticker.upper()), self.params)
        if not result['empty']:
            print('... ACQUIRED DATA SUCCESSFULLY.')
            self.reformat_dates(result)
            return result
        print('... FAILED.')
        return None

    def get_tickers(self):
        '''
        Uses get_endpoint_data() on every ticker symbol in set returned by get_tickers_set().
        Before returning a value, function uses write_to_file to create a
        csv file of a dataframe containing the data that has just been pulled.

        Input: none.
        Output: returns a list of dictionaries, each dictionary containing
                the high, low, open, close, volume, and datetime columns
                for each given ticker in the set returned by get_tickers_set().
        '''
        results = []
        for item in self.get_tickers_set():
            if item != '':
                result = self.get_endpoint_data(self.endpoint.format(ticker=item.upper()), self.params)
                if not result['empty']:
                    self.reformat_dates(result)
                    results.append(result)
                    print('... ACQUIRED DATA #' + str(len(results)) + ' SUCCESSFULLY.')
                else:
                    print('... FAILED.')
        return results


    def create_files(self, data_list, candle_timeframe):
        '''
        Saves historical data pulled from the API to a local file titled with the ticker's symbol.

        Input: a dictionary returned by get_endpoint_data().
        Output: none, a new file is created or an old file is overwritten if one existed before.
        '''
        for historical_data in data_list:
            filename = './data/' +  candle_timeframe +  '/' + historical_data['symbol'].lower() + '.csv'
            historical_data = pd.DataFrame(historical_data['candles'])
            historical_data.to_csv(filename, encoding='utf-8')

if __name__ == '__main__':
    consumer_key = 'V36YI3DNMFCACJF7PLBCYIZKTUJRY83C'

    api_utility = Td(consumer_key, 'year', 20, 'daily', 1)
    data = api_utility.get_tickers()
    print('\n>>>DONE ACQUIRING DATA')
    print('>>>STARTING TO CREATE FILES')
    api_utility.create_files(data, 'daily')
    print('\n>>>File creation complete.')
