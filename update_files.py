from generate_files import TdPriceHistory as Td

def update_minute_data():
    api_utility = Td()

    minute_data = api_utility.get_tickers('day', 10, 'minute', 1)
    api_utility.create_files(minute_data, 'minute')

    print('\n>>>File update complete.')

if __name__ == '__main__':
    update_minute_data()
