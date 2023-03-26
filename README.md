# Market Analysis.
### Data Aggregation, Dimensionality Reduction, and Continuous-Time Markov Chains.
##### By Michael Glushchenko and Charles Delapa.

## Table of Contents
* [Purpose](https://github.com/mglush/market-analysis/blob/main/README.md#purpose)
* [Goals and Steps](https://github.com/mglush/market-analysis/blob/main/README.md#goals-and-steps)
* [Files](https://github.com/mglush/market-analysis/blob/main/README.md#files)
* [How to Run](https://github.com/mglush/market-analysis/blob/main/README.md#how-to-run)
* [Sources](https://github.com/mglush/market-analysis/blob/main/README.md#sources)

## Purpose
The purpose of this project is to improve my data-science skills by aggregating financial data, and to improve my statistical skills by attempting to apply what I've learned in undergrad Statistics to a real-world (mostly chaotic and unsolvable) problem. Since this problem isn't exactly solvable, the ultimate goal of this project is to find models that approximate the movement of some stocks with a 'decently-high' degree of success.

## Goals and Steps
1. We use the [data-aggregation](https://github.com/mglush/data-aggregation) repository to create the financial data for all steps that follow.
2. Next, we will clean up the aggregated data, filling in all gaps and fixing the fact that there's no financial data on weekends and holidays, as well as during certain times of day.
3. Use the Uniform Manifold Approximation & Projection Algorithm (UMAP) to reduce the dimensionality of each pattern (from 1000 data points to a 2-dimensional point on a plane). We will try to do this for separate groups of stocks, as well as separate time-frames, one time-frame at a time. The goals for this step would be to determine acceptable parameters for the UMAP algorithm, to obtain clusters/piles of different patterns, to run k-means clustering on the resulting patterns, and to map the labelings of each of those clusters back to the original patterns.
4. Once patterns are successfully labeled and put into separate groups, we can try to apply the idea of markov chains to approximate the probability that a certain stock pattern will appear next given some sequence of patterns.
5. It would be nice to eventtually provide an interface where a user can enter an instrument symbol, and, as an output, receive a chart of that stock with the 3-5 most-likely paths for the next timeframe (within the next couple minutes). We are doing this on a minute-by-minute basis so that the amount of extraneous variables is kept to a minimum.
6. Finally, we will write a research paper documenting our findings and any new discoveries made/skills learned.

## Files
While the files contain self-explanatory code, this section briefly summarizes the purpose of each file.
1. [Data Aggregation](https://github.com/mglush/data-aggregation)
* Repository that we use to create financial data we work on throughout this project. More details can be found in the readme on the page linked.
2. [dim_reduction/utils.py](https://github.com/glush-n-charles/market-analysis/blob/main/dim_reduction/utils.py)
* Provides functions used in the pre-processing and data-cleaning part of the the project (functions that clean up the data, smooth it out, etc.).
3. [dim_reduction/pre_processing.py](https://github.com/glush-n-charles/market-analysis/blob/main/dim_reduction/pre_processing.py)
* Using functions from utils.py, the file cleans up the financial data aggreagted using data-aggregation, breaks up each stock's chart into patterns of a pre-specified length, and saves those patterns, preparing for the dimensionality reduction portion of the project.
4. [dim_reduction/Umap.ipynb](https://github.com/glush-n-charles/market-analysis/blob/main/dim_reduction/Umap.ipynb)
* Test out some parameters of UMAP on a small amount of data to get a feel for how it works, whether it works at all, and to outline the approach that will be used for the large amount of data we have at hand.

## How to Run
Still in development.

## Sources
* [Umap How To](https://umap-learn.readthedocs.io/en/latest/index.html)

2022-2023 &copy; Michael Glushchenko, Charles Delapa
