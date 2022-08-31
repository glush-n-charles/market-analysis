from td_price_history import TdPriceHistory as Td
import time

if __name__ == '__main__':
    util = Td()

    start2 = time.time()
    util.update_file('a', 'year', 20, 'daily', 1)
    end2 = time.time()
    
    start = time.time()
    util.new_update_file('a', 'year', 20, 'daily', 1)
    end = time.time()

    new = end - start
    old = end2 - start2
    improvenemnt = 100 * float((float(old - new) / old))

    print(f'new one took {new} seconds')
    print(f'old one took {old} seconds')

    print(f'imporovement of {improvenemnt}%')