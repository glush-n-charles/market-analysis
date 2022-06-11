# Market Analysis
#### Dimensionality Reduction and Markov Chains
###### By Michael Glushchenko

Examining data similarities across stock/commodity/money markets. Applying the results to predict possible paths of a given stock.

## Table of Contents
* [Approach](https://github.com/mglush/market-analysis/blob/main/README.md#approaches)
* [Technologies](https://github.com/mglush/market-analysis/blob/main/README.md#technologies)
* [Sources](https://github.com/mglush/market-analysis/blob/main/README.md#sources)

## Approach
* First, we choose to focus on stocks in the S&P500, the Nasdaq, and the Dow Jones.
  * We use the TD Ameritrade API and scrap all historical data the API has about stocks in the above indices.
  * Initially, the data collected includes 20 years of daily high, low, open, close, and volume data points, as well as 10 days of by the minute data.

## Technologies
* TD Ameritrade API.
* Python (libraries include *requests*, *json*, *datetime*, *pandas*, *umap*, *matplotlib*).

## Sources
* [Umap How To](https://umap-learn.readthedocs.io/en/latest/index.html)
* [Yahoo Finance How To](https://levelup.gitconnected.com/how-to-get-all-stock-symbols-a73925c16a1b)

2022 &copy; Michael Glushchenko, Charles Delapa
