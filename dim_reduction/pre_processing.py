import pandas as pd
import os
import signal
import time

from utils import PATTERN_SIZE, findMin, findMax, normalize, zipp, findDec, connect_patterns

PRINT_HELPER_TEXT = False
successful, too_few_points, timed_out = 0, 0, 0
# we will be going through the minute directory and applying our results to the daily directory later.
directory = './../data/minute'
pattern_container = []

# handles time outs; eventually need to change this part to handle timeouts in a more efficient manner.
def handler(signum, frame):
   raise Exception('END OF TIME')

def process_chart(file_path):
    # load data from file.
    df = pd.DataFrame.from_records(pd.read_json(file_path))
    
    if (len(df) < 1000):
        too_few_points += 1
        if (PRINT_HELPER_TEXT):
            print('NOT ENOUGH DATA POINTS TO BREAK INTO SEPARATE PATTERNS!!!\n')
        return

    if (PRINT_HELPER_TEXT):
        print('LOADED DATA')

    # normalize highs and lows.
    vh = normalize(df['high'])
    vl = normalize(df['low'])

    if (PRINT_HELPER_TEXT):
        print('NORMALIZED DATA')

    # decrease amount of points we are working on by finding the local mins and maxs of each small range.
    xl, yl = findMin(range(len(vl)), vl, int(len(vh) / 75))
    xh, yh = findMax(range(len(vh)), vh, int(len(vh) / 75))

    if (PRINT_HELPER_TEXT):
        print('FOUND MIN AND MAX')

    # further decrease num of points we are working on via a custom-written zipp function.
    X, Y = zipp(yl, yh, xl, xh)

    if (PRINT_HELPER_TEXT):
        print('ZIPPED THAT SHIT UP')

    # break chart up into equally-sized patterns.
    decy, decx, decsex, decsey = findDec(vl, X, Y, 0.05, PATTERN_SIZE)

    if (PRINT_HELPER_TEXT):
        print('BROKE CHART INTO PATTERNS SUCCESSFULLY!!!')
    
    # clean up resulting patterns so they are all 1000 in length so that dimensionality reduction is easier to perform later.
    connect_patterns(decx, decy, PATTERN_SIZE)

    if (PRINT_HELPER_TEXT):
        print('CONNECTED THE PATTERNS SUCCESSFULLY!!!')

    patterns = pd.DataFrame(decy)
    patterns = patterns.dropna(axis=0)
    pattern_container.append(patterns)

    if (PRINT_HELPER_TEXT):
        print('DONE WITH CURRENT CHART.')


# start timer to compare the parallelized code to previously-serial code.
start = time.time()

# iterate over files in the given directory.
# load the data from each file, normalize it, break it up, append to result.
for filename in os.scandir(directory):
    if filename.is_file():
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)
        
        try:
            process_chart(filename.path)
            successful += 1
            if (PRINT_HELPER_TEXT_TWO):
                print(f'DONE WITH FILE {filename.name}\n')
        except Exception:
            timed_out += 1
            if (PRINT_HELPER_TEXT_TWO):
                print(f'{filename.name} TIMED OUT OR EXCEPTION RAISED\n')
        
        # cancel timer if function succeeded in under 1 seconds
        # (usually takes ~ 0.1-0.2 seconds, thus 1 second likely indicates a timeout).
        signal.alarm(0)

print(f'>>> WE RAN THROUGH ALL FILES IN {time.time() - start} SECONDS')

# combine all patterns within pattern_container into one dataframe.
pattern_dataframe = pd.concat(pattern_container)

# save patterns to patterns.json.
# (NOT SURE IF THIS IS THE BEST WAY TO DO THIS, MIGHT WANT TO
# PUT PATTERNS FROM DIFFERENT TIME FRAMES INTO DIFFERENT FILES).
try:
    pattern_dataframe.to_json('patterns.json', orient='records', lines=True)
except OSError:
    print('\n>>>FAILED TO WRITE PATTERNS TO FILE.')

print(f'>>> WE HAVE {len(pattern_dataframe)} PATTERNS IN TOTAL!\n')
print(f'>>>{timed_out} FILES TIMED OUT AND {too_few_points} FILES DID NOT HAVE ENOUGH POINTS...')
