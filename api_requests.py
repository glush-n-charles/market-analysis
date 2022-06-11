from yahoo_fin import stock_info as si
import requests
import json
from datetime import datetime
import pandas as pd
import time

CONSUMER_KEY = 'UCJA7GWHIKKXO2G69GXDMEFUX24QZ0PD'

class TdPriceHistory():
    '''
    Utility class that will be used to interract with the
    TD Ameritrade API endpoints and pool historical price data
    for every ticker in the s&p 500, nasdaq, and dow jones.
    
    Additionally, contains a create_files method that creates two files for every
    ticker mentioned above, with the first file containing data returned by
    the get request in json format, and the second file containing a dataframe
    of the data that the get request returned.
    '''
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory'
    apikey = ''

    def __init__(self, apikey=CONSUMER_KEY):
        '''
        Initializes the endpoint and the api key that will be used (if user wants to specify one).
        '''
        self.apikey = apikey

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
            if not (len(symbol) > 4 and symbol[-1] in avoid_endings) and symbol != '':
                sav_set.add(symbol)

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

    def get_ticker(self, ticker, period_type, period, frequency_type, frequency):
        '''
        Uses get_endpoint_data() on a single ticker symbol.

        Input: string containing the symbol of a ticker.
        Output: if request successful: returns a single dictionary containing
                the high, low, open, close, volume, and datetime columns
                for a given ticker in set returned by get_tickers_set().
                returns none otherwise.
        '''
        params = {'apikey' : self.apikey,
                        'periodType' : period_type,
                        'period' : period,
                        'frequencyType' : frequency_type,
                        'frequency' : frequency}
        result = self.get_endpoint_data(self.endpoint.format(ticker=ticker.upper()), params)
        if not result['empty']:
            print('... ACQUIRED DATA SUCCESSFULLY.')
            self.reformat_dates(result)
            return result
        print('... FAILED.')
        return None

    def get_tickers(self, period_type, period, frequency_type, frequency):
        '''
        Uses get_endpoint_data() on every ticker symbol in set returned by get_tickers_set().
        Before returning a value, function uses write_to_file to create a
        csv file of a dataframe containing the data that has just been pulled.

        Input: none.
        Output: returns a list of dictionaries, each dictionary containing
                the high, low, open, close, volume, and datetime columns
                for each given ticker in the set returned by get_tickers_set().
        '''
        params = {'apikey' : self.apikey,
                        'periodType' : period_type,
                        'period' : period,
                        'frequencyType' : frequency_type,
                        'frequency' : frequency}
        results = []
        for item in self.get_tickers_set():
            if len(results) % 120 == 119 and frequency_type == 'minute':
                time.sleep(7)

            result = self.get_endpoint_data(self.endpoint.format(ticker=item.upper()), params)
            if result is None:
                print('... ENCOUNTERED ERROR ON THIS PAGE.')
            elif not result['empty']:
                self.reformat_dates(result)
                results.append(result)
                print('... ACQUIRED DATA #' + str(len(results)) + ' SUCCESSFULLY.')
            else:
                print('... FAILED.')
        return results

    def create_file(self, ticker, data, candle_timeframe):
        '''
        Saves historical data pulled from the API to a local file titled with the ticker's symbol.
        In the first file, a dictionary is stored, and the file is in json format.
        In the second file, a dataframe is stored, and the file in csv format.

        Input: a dictionary returned by get_endpoint_data().
        Output: none, two new file re created for every stock ticker in the get_tickers_set().
        '''
        csv_filename = './data/' +  candle_timeframe +  '/' + ticker.lower() + '.csv'
        df_data = pd.DataFrame(data['candles'])
        df_data.to_csv(csv_filename, encoding='utf-8')

        try:
            json_filename = './data/' +  candle_timeframe +  '/' + ticker.lower() + '.json'
            file = open(json_filename, 'w', encoding='utf-8')
            file.write(json.dumps(data))
            file.close()
        except OSError as file_error:
            print(file_error)

    def create_files(self, data_list, candle_timeframe):
        '''
        Saves historical data pulled from the API to a local file titled with the ticker's symbol.
        In the first file, a dictionary is stored, and the file is in json format.
        In the second file, a dataframe is stored, and the file in csv format.
        Files are not created for data containing less than 20 data points.

        Input: a dictionary returned by get_endpoint_data().
        Output: none, two new file re created for every stock ticker in the get_tickers_set().
        '''
        counter = 1
        for historical_data in data_list:
            if len(historical_data['candles']) > 20:    
                csv_filename = './data/' +  candle_timeframe +  '/' + historical_data['symbol'].lower() + '.csv'
                json_filename = './data/' +  candle_timeframe +  '/' + historical_data['symbol'].lower() + '.json'
                
                historical_data = pd.DataFrame(historical_data['candles'])
                historical_data.to_csv(csv_filename, encoding='utf-8')

                try:
                    file = open(json_filename, encoding='utf-8')
                    file.write(historical_data)
                    file.close()
                except OSError as file_error:
                    print(file_error)

                print('>>>FINISHED WRITING TO FILE #' + str(counter) + '.')
                counter = counter + 1

def run_td_api():
    '''
    Creates a Td class and calls its create_files() function. Could use
    the createFile() function inside of get_tickers(), but I kept get_tickers
    from making any files so that function can be used for getting ticker info.

    Input: none.
    Output: none, new files created in the data/daily and data/minute folders.
    '''
    api_utility = TdPriceHistory()

    daily_data = api_utility.get_tickers('year', 20, 'daily', 1)
    minute_data = api_utility.get_tickers('day', 10, 'minute', 1)

    api_utility.create_files(daily_data, 'daily')
    api_utility.create_files(minute_data, 'minute')

    print('\n>>>File creation complete.')

if __name__ == '__main__':
    run_td_api()
