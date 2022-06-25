'''
generate_files.py
Michael Glushchenko

'''
import time                             # pylint: disable=import-error
from datetime import datetime           # pylint: disable=import-error
import ujson as json                    # pylint: disable=import-error
from yahoo_fin import stock_info as si  # pylint: disable=import-error
import requests                         # pylint: disable=import-error
import pandas as pd                     # pylint: disable=import-error

CONSUMER_KEY = 'UCJA7GWHIKKXO2G69GXDMEFUX24QZ0PD'

class TdPriceHistory():
    '''
    DESCRIPTION: Utility class that can be used to interract with
    the TD Ameritrade API endpoints and to pool historical price
    data for every ticker in the s&p 500, nasdaq, and dow jones.
    
    NOTES: contains a create_file method that can be used
    to create a json-format file of a given ticker's data.
    contains a create_files method that will create a file
    for every ticker symbol mentioned above.

    RUNNING FILE DIRECTLY will create two files
    for each ticker mentioned above, with the first file
    containing the last 20 years of daily data and the
    second file containing last 10 days of minute data.

    USING CLASS AS AN IMPORT will provide utility
    without running file creation automatically.
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
        Also get all stocks in the yahoo 'other' category.

        Input: none.
        Output: a set containing ticker symbols that exist on yahoo finance.
        '''
        df1 = pd.DataFrame(si.tickers_sp500())
        df2 = pd.DataFrame(si.tickers_nasdaq())
        df3 = pd.DataFrame(si.tickers_dow())
        df4 = pd.DataFrame(si.tickers_other())

        sym1 = set( symbol for symbol in df1[0].values.tolist() )
        sym2 = set( symbol for symbol in df2[0].values.tolist() )
        sym3 = set( symbol for symbol in df3[0].values.tolist() )
        sym4 = set( symbol for symbol in df4[0].values.tolist() )

        symbols = set.union( sym1, sym2, sym3, sym4 )
        avoid_endings = ['W', 'R', 'P', 'Q']
        save = set()

        for symbol in symbols:
            if not (len(symbol) > 4 and symbol[-1] in avoid_endings) and symbol != '':
                save.add(symbol)

        return save

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

        Input: string containing the symbol of a ticker, as well as the API
                parameters that will be used.
                period_type values: day, month, year, ytd.
                period values (by petiod type): day: 1, 2, 3, 4, 5, 10
                                                month: 1, 2, 3, 6
                                                year: 1, 2, 3, 5, 10, 15, 20
                                                ytd: 1
                frequency type values (by period type): day: minute*
                                                        month: daily, weekly
                                                        year: daily, weekly, monthly
                                                        ytd: daily, weekly
                frequency values (by frequency type): minute: 1, 5, 10, 15, 30
                                                      daily: 1
                                                      weekly: 1
                                                      monthly: 1
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

        Input: api parameters for the given search.
                period_type values: day, month, year, ytd.
                period values (by petiod type): day: 1, 2, 3, 4, 5, 10
                                                month: 1, 2, 3, 6
                                                year: 1, 2, 3, 5, 10, 15, 20
                                                ytd: 1
                frequency type values (by period type): day: minute*
                                                        month: daily, weekly
                                                        year: daily, weekly, monthly
                                                        ytd: daily, weekly
                frequency values (by frequency type): minute: 1, 5, 10, 15, 30
                                                      daily: 1
                                                      weekly: 1
                                                      monthly: 1
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
                time.sleep(10)

            result = self.get_endpoint_data(self.endpoint.format(ticker=item.upper()), params)
            if result is None:
                print('... ENCOUNTERED ERROR ON THIS PAGE.')
            elif not result['empty']:
                self.reformat_dates(result)
                results.append(result)
                print('... ACQUIRED DATA #' + str(len(results)) + ' SUCCESSFULLY.')
            else:
                print('... FAILED, NO DATA AT THIS LINK, CHECK PARAMETERS.')
        return results

    def create_file(self, ticker, data, candle_timeframe):
        '''
        Saves historical data pulled from the API to a local file titled with the ticker's symbol.
        A dictionary is stored within a json format file.

        Input: a dictionary returned by get_endpoint_data().
        Output: none, two new file re created for every stock ticker in the get_tickers_set().
        '''
        try:
            json_filename = './data/' +  candle_timeframe +  '/' + ticker.lower() + '.json'
            file = open(json_filename, 'w', encoding='utf-8', mode='x')
            json.dump(data['candles'], file, indent=4)
            file.close()
        except OSError as file_error:
            print(file_error)

    def create_files(self, data_list, candle_timeframe):
        '''
        Saves historical data pulled from the API to a local file titled with the ticker's symbol.
        In the first file, a dictionary is stored, and the file is in json format.
        Files are not created for data containing less than 20 data points.
        If file already exists, a call to update_file is made instead.

        Input: a dictionary returned by get_endpoint_data(), and the timeframe of each candle.
        Output: none, a new file is created for every stock ticker in the get_tickers_set().
        '''
        steps = 1
        for data in data_list:
            if len(data['candles']) > 20:    
                try:
                    json_filename = './data/' +  candle_timeframe +  '/' + data['symbol'].lower() + '.json'
                    file = open(json_filename, encoding='utf-8', mode='x')
                    json.dump(data['candles'], file, indent=4)
                    file.close()
                    print('>>>WROTE NEW FILE ' + str(json_filename) + '.')
                except OSError:
                    pass # STUB STUB STUB

                print('>>>FINISHED STEP #' + str(steps) + '.')
                steps = steps + 1

    def update_file(self, ticker, period_type, period, frequency_type, frequency):
        '''
        If file exists, updates data of existing file by appending everything
        that is not already in the file but is in the data parameter.
        Otherwise, creates the file first, then writes data to it.
        '''
        filename = './data/' + str(frequency_type) + '/' + str(ticker).lower() + '.json'
        try:
            file = open(filename, encoding='utf-8', mode='r')
            data = json.load(file)
            file.close()
        except OSError:
            print('>>>FILE DOES NOT EXIST, CREATING NEW FILE.')
            data = []

        old_dates = set(item['datetime'] for item in data)
        testing = self.get_ticker(ticker.lower(), period_type, period, frequency_type, frequency)['candles']

        for item in testing:
            if item['datetime'] not in old_dates:
                data.append(item)

        try:
            file = open(filename, encoding='utf-8', mode='w')
            data = json.dump(data, file, indent=4)
            file.close()
            print('>>>SUCCESSFULLY WROTE TO FILE ' + str(filename) + '.')
        except OSError:
            print('>>>FAILED TO WRITE TO FILE.')

    def update_files(self, period_type, period, frequency_type, frequency):
        '''
        Creates/updates all files in the list of tickers returned
        by the get_tickers_set method.
        '''
        tickers = self.get_tickers_set()
        for ticker in tickers:
            self.update_file(ticker, period_type, period, frequency_type, frequency)
        print('>>>ALL FILES SUCCESSFULLY UPDATED')
