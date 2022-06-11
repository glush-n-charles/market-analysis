from yahoo_fin import stock_info as si
import requests
import json
from datetime import datetime
import pprint
import pandas as pd

CONSUMER_KEY ='V36YI3DNMFCACJF7PLBCYIZKTUJRY83C'

PRICE_HISTORY_ENDPOINT = 'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory'
PRICE_HISTORY_PARAMS = {'apikey' : CONSUMER_KEY,
                            'periodType' : 'year',
                            'period' : 20,
                            'frequencyType' : 'daily',
                            'frequency' : 1}

class Td():
    '''
    Utility class that will be used to interract with the
    TD Ameritrade API endpoints and pool historical price data
    for every ticker in the s&p 500, nasdaq, and dow jones.
    '''
    def get_tickers_set(self):
        '''
        Gets all stock tickers in sp500, nasdaq, and dow indices.

        Input: none.
        Output: set containing ticker symbols that exist on yahoo finance.
        '''
        df1 = pd.DataFrame( si.tickers_sp500() )
        df2 = pd.DataFrame( si.tickers_nasdaq() )
        df3 = pd.DataFrame( si.tickers_dow() )
        # df4 = pd.DataFrame( si.tickers_other() )

        sym1 = set( symbol for symbol in df1[0].values.tolist() )
        sym2 = set( symbol for symbol in df2[0].values.tolist() )
        sym3 = set( symbol for symbol in df3[0].values.tolist() )
        # sym4 = set( symbol for symbol in df4[0].values.tolist() )

        symbols = set.union( sym1, sym2, sym3 )
        avoid_endings = ['W', 'R', 'P', 'Q']
        sav_set = set()

        for symbol in symbols:
            if len( symbol ) > 4 and symbol[-1] in avoid_endings:
                continue
            else:
                sav_set.add( symbol )

        return sav_set

    def get_endpoint_data(self, endpoint, params):
        '''
        Performs get request on the endpoint with given parameters.

        Input: endpoint URL, dictionary of search parameters.
        Output: dictionary of returned values if request successful.
                none otherwise.
        '''
        print('>>>GETTING DATA FROM ' + str(endpoint), end='')
        try:
            page = requests.get(url=endpoint,
                            params=params)
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
        Output: modified dictionary.
        '''
        for item in content['candles']:
            item['datetime'] = datetime.utcfromtimestamp(item['datetime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

    def get_ticker(self, ticker):
        '''
        Uses get_endpoint_data() on a single ticker symbol.

        Input: string containing the symbol of a ticker.
        Output: if get request was successful, returns a single dictionary containing
                the high, low, open, close, volume, and datetime columns
                for a given ticker in set returned by get_tickers_set().
                returns none otherwise.
        '''
        result = self.get_endpoint_data(PRICE_HISTORY_ENDPOINT.format(ticker=ticker.upper()), PRICE_HISTORY_PARAMS)
        if not result['empty']:
            print('... ACQUIRED DATA SUCCESSFULLY.')
            self.reformat_dates(result)
            return result
        print('... FAILED.')
        return None

    def get_tickers(self):
        '''
        Uses get_endpoint_data() on every ticker symbol in set returned by get_tickers_set().

        Input: none.
        Output: a list of dictionaries, each dictionary containing
                the high, low, open, close, volume, and datetime columns
                for a given ticker in the set returned by get_tickers_set().
        '''
        results = []
        for item in self.get_tickers_set():
            if item != '':
                result = self.get_endpoint_data(PRICE_HISTORY_ENDPOINT.format(ticker=item.upper()), PRICE_HISTORY_PARAMS)
                if not result['empty']:
                    self.reformat_dates(result)
                    results.append(result)
                    print('... ACQUIRED DATA SUCCESSFULLY.')
                else:
                    print('... FAILED.')
        return results

if __name__ == '__main__':
    api_utility = Td()
    for item in api_utility.get_tickers():
        pprint.pprint(item)
