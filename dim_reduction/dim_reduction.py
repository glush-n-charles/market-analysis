'''
dim_reduction.py

Roughly testing out different parameters of UMAP to see
what difference they make for our data.

Studying the effect of the amount of data provided as input
on the results of the UMAP (Uniform Manifold Approximation & Projection) output.

File will need to be rewritten much more neatly...
'''

import umap.umap_ as umap
from sklearn.cluster import KMeans
import time
import pandas as pd
import matplotlib.pyplot as plt
import ijson
import decimal
import multiprocessing as mp

PROCESSES_TO_USE = 4 # using 4 as to not overheat the computer.

# parse json file for all the patterns.
def setup():
    curr = []
    patterns = []

    start = time.time()

    for item in ijson.parse(open('patterns.json')):
        if type(item[2]) is decimal.Decimal:
            curr.append(float(item[2]))
        
            if len(curr) == 1000:
                patterns.append(curr)
                curr = []

    print(f'READING THE PATTERNS JSON FILE TAKES {time.time() - start} SECONDS')
    print(f'WE HAVE {len(patterns)} PATTERNS ON OUR HANDS\n')
    print('>>> CREATING DATAFRAME OF PATTERNS')
    patterns = pd.DataFrame(patterns)
    print('>>> SUCCESSFULLY CREATED DATAFRAME OF PATTERNS')

    # create umap reducers.

    reducer00 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.75,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.01, n_components=2, n_epochs=10000,
            n_neighbors=5, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer0 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.5,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.5, n_components=2, n_epochs=10000,
            n_neighbors=5, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer1 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.95,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.01, n_components=2, n_epochs=10000,
            n_neighbors=5, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer2 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.95,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.5, n_components=2, n_epochs=10000,
            n_neighbors=10, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer3 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.75,
            local_connectivity=1.0, low_memory=False, metric='chebyshev',
            metric_kwds=None, min_dist=0.1, n_components=2, n_epochs=5000,
            n_neighbors=50, negative_sample_rate=5, output_metric='chebyshev',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer4 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.75,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.5, n_components=2, n_epochs=5000,
            n_neighbors=50, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer5 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.75,
            local_connectivity=1.0, low_memory=False, metric='chebyshev',
            metric_kwds=None, min_dist=0.5, n_components=2, n_epochs=10000,
            n_neighbors=75, negative_sample_rate=5, output_metric='chebyshev',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer6 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.25,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.5, n_components=2, n_epochs=25000,
            n_neighbors=25, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer7 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.95,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.01, n_components=2, n_epochs=10000,
            n_neighbors=2, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducer8 = umap.UMAP(a=None, angular_rp_forest=False, b=None,
            force_approximation_algorithm=False, init='spectral', learning_rate=0.75,
            local_connectivity=1.0, low_memory=False, metric='euclidean',
            metric_kwds=None, min_dist=0.01, n_components=2, n_epochs=10000,
            n_neighbors=10, negative_sample_rate=5, output_metric='euclidean',
            output_metric_kwds=None, random_state=42, repulsion_strength=1.0,
            set_op_mix_ratio=1.0, spread=1.0, target_metric='categorical',
            target_metric_kwds=None, target_n_neighbors=-1, target_weight=0.5,
            transform_queue_size=4.0, transform_seed=42, unique=False, verbose=False)

    reducers = [reducer00, reducer0, reducer1, reducer2, reducer6, reducer7, reducer8, reducer3, reducer4, reducer5]
    return reducers, patterns

def run_umap_model(queue, i, patterns):
    reducer = queue.get()

    start = time.time()

    model = reducer.fit(patterns)

    print(f'TOTAL TIME FOR MODEL {i} WAS {time.time() - start} SECONDS\n')

    embedding = model.embedding_
    
    fig = plt.figure()
    plt.scatter(embedding[:, 0], embedding[:, 1])

    name = './plots/trial' + str(i + 3) + '.png'
    fig.savefig(name, dpi=fig.dpi)
        
if __name__ == '__main__':
    reducers, patterns = setup()

    # create a queue of reducers
    queue = mp.Queue()
    for reducer in reducers:
        queue.put(reducer)

    start = time.time()

    processes = []
    for i in range(PROCESSES_TO_USE):
        # create processes, assign them all to test one model from reducers list.
        proc = mp.Process(target=run_umap_model, args=(queue, i, patterns, ))
        proc.start()
        processes.append(proc)

    # wait for all processes to finish running.
    for proc in processes:
        proc.join()
    # kill all processes.
    for proc in processes:
        proc.kill()

    print(f'TOTAL (PARALLEL) UMAP TIME = {time.time() - start} SECONDS\n')
