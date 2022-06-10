from sqlite3 import connect
import requests
import json
from datetime import datetime
import pprint

TICKER = str(input('Enter a ticker: ')).upper()

CONSUMER_KEY ='V36YI3DNMFCACJF7PLBCYIZKTUJRY83C'

PRICE_HISTORY_ENDPOINT = 'https://api.tdameritrade.com/v1/marketdata/' + TICKER + '/pricehistory'
PRICE_HISTORY_PARAMS = {'apikey' : CONSUMER_KEY,
                            'periodType' : 'year',
                            'period' : 20,
                            'frequencyType' : 'daily',
                            'frequency' : 1}

GET_QUOTES_ENDPOINT = 'https://api.tdameritrade.com/v1/marketdata/quotes'
GET_QUOTES_PARAMS = {'apikey' : CONSUMER_KEY,
                        'symbol': TICKER}

def get_data(endpoint, parameters):
    '''
    Performs get request on the endpoint with given parameters.

    Input: endpoint URL, dictionary of search parameters.
    Output: dictionary of returned values.
    '''
    try:
        page = requests.get(url=endpoint,
                        params=parameters)
    except requests.RequestException as request_exception:
        print(request_exception)

    if page.status_code == 200:
        return json.loads(page.content)

    return "BAD REQUEST ERROR. PAGE STATUS = " + str(page.status_code)

def reformat_dates(content):
    '''
    Changes unix timestamp format to readable date format.
    Input: dictionary containing a 'datetime' column of unix timestamp values.
    Output: modified dictionary
    '''
    for item in content['candles']:
        item['datetime'] = datetime.utcfromtimestamp(item['datetime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    result = get_data(PRICE_HISTORY_ENDPOINT, PRICE_HISTORY_PARAMS)
    reformat_dates(result)
    pprint.pprint(result)