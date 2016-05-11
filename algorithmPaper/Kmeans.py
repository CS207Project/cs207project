"""Algorithm Paper:
Hilawi Belachew, Christian Junge, Akhil Ketkar, Juaquin Sanchez, Daniel Yue

The Scikit-Learn implementation of K-means contains several optimizations that are designed to reduce computation.  This implementation includes several options that allow the user to navigate the tradeoffs between desired accuracy and computation.  These fall under the following categories:

1)  Initialization

2)  Thresholds

3)  Parallelization of multiple jobs

4)  C under the hood

5)  Precompute Distances 



1)  **Initialization**

The k-means clustering algorithm finds cluster centers iteratively by starting with a set of cluster center assignments, and then assigning each point to the closest cluster center.  Once all points are assigned, cluster centers are recalculated to be the center of all of the points in that cluster, and each point is reassigned to the closest cluster center.  This terminates when no updates are made to the cluster assignments or cluster centers.  

This process is guaranteed to converge, but not necessarily on the global optimum.  The worst case complexity is given by O(n^(k+2/p)) with n = n_samples, p = n_features. (D. Arthur and S. Vassilvitskii, ‘How slow is the k-means method?’ SoCG2006), but in practice the algorithm converges very quickly.  

Given a specific set of initial clusters, the k-means algorithm is deterministic, so the results are sensitive to initialization.  The most basic initialization is to randomly select k of the data points to be the initial cluster centers.  The weakness of this method is that if these initial points are close together, the algorithm may fail to find the true cluster centers.  The k-means++ initialization attempts to take care of this weakness by first randomly assigning one point to be the first initial cluster center, then choosing the next initial cluster center based on a probability weighted by its distance to the first cluster center, and so on until k initial cluster centers have been assigned.  

The advantage of k-means++ is that it will, on average, space the initial cluster centers out more evenly across the space than a completely random initialization.  Because the probabilities of being selected are merely weighted by the distance, however, this initialization does not guarantee that the centers will be more widely spaced, it simply makes this more likely.  Furthermore, there is a computational overhead for the k-means++ initialization, as it requires distances between every point and every cluster center so far created to be calculated as each cluster center is added.  The tradeoff is that this initialization tends to produce better cluster centers, and can potentially reduce the number of iterations for convergence.  

The scikit-learn implementation also allows the user to specify the initial cluster centers rather than using random assignments.  This could be useful if the user has some a priori idea of where the cluster centers should be, potentially based on some domain knowledge, or when adding more data after earlier clustering runs.  This option would be unlikely to be used for clustering that is performed as part of data exploration, however, and in practice most users will be relying on some level of randomization for their initial cluster assignments.  

Because the cluster assignments are deterministic, they are very sensitive to the initialization, and the algorithm is not guaranteed to converge on the global optimum.  One way to avoid being stuck in an unfavorable local optimum is to reinitialize and run the clustering again.  The scikit-learn implementation includes a ‘n_init’ keyword argument to allow the user to specify the number of re-initializations that are performed, and the final version that is returned is the one that minimizes the sum of the distances from the cluster centers.  

2)  **Thresholds**
    
The scikit-learn k-means implementation has two features that allow the user to limit computation explicitly: a threshold for convergence, and a maximum number of iterations.  
    
The convergence threshold is passed as the ‘tol’ argument, and the basic idea behind this option is to stop early and declare that the algorithm has converged when changes to the cluster centers become very small, rather than waiting for them to stop changing completely.  In practice, this works by first calculating the product of tol with the mean of the variances of each feature in the whole dataset, producing a quantity to be used to determine convergence that takes into account the scale of the variation of the individual features.  Then when the change in the squared norm falls below this tolerance value, the algorithm terminates, cutting off what could potentially be many more iterations that are making very minute changes to what is already a nearly complete clustering run.  
    
The maximum number of iterations is passed as the ‘max_iter’ argument, and the algorithm simply runs within a for loop for this number of iterations.  Within each iteration, the convergence check described above is performed, and allows the algorithm to break out of the for loop early when the updates become small.  

3)  **Parallelization of multiple jobs**
    
While the k-means algorithm is serial, the user has the option (described above) to perform multiple runs with different initializations and take the result with the lowest total distance to the cluster centers.  The scikit-learn implementation parallelizes these runs using scikit-learn’s own Parallel function within its externals/joblib module.  By default, this uses Python multiprocessing, and the user can specify the number of jobs to run with the ‘n_jobs’ argument.  The user can allow this assignment to be made automatically by passing ‘n_jobs=-1’, in which case all CPU’s are used.  The user can also opt to run everything with a single job, in which case multiprocessing is not used at all.  

4)  **C under the hood**
    
The computation of the cluster means and the computation of the cluster assignments within each iteration are embarrassingly parallel.  All of this computation is performed in Cython in the ._k_means.pyx file.  Both the cluster means and cluster assignments calculations have two versions each, one for dense arrays and one for sparse arrays.  The code first uses scipy.sparse.issparse() to determine identify whether the array to compute on is a regular numpy matrix or a scipy Compressed Sparse Row matrix before selecting which function to pass the array to.  All of these Cython functions enjoy increased efficiency gains from defining variables with static C type declarations and performing matrix multiplication with cblas_ddot.  

5)  **Precompute Distances**
    
In all cases, label assignments are updated in-place, reducing memory usage.  Distances to cluster centers can also be updated in place, but speed gains can be made by precomputing the distances via numpy matrix operations within the euclidian_distances function from sklearn.metrics.pairwise, rather than one-by-one within the for loop that updates label assignments.  These speed gains come with the tradeoff of increasing memory usage by requiring two copies of distances to be stored, however, so this option is given to the user.  There is an ‘auto’ option, which precomputes the distances if it will not result in memory usage above a hard-coded threshold.  This threshold corresponds to 100MB of overhead per job, and is calculated as number of samples * number of clusters < 12e6.  

The option to precompute distances is ignored for scipy sparse matrices.  Instead, the distance of each point from its cluster center is updated in a for loop as in the precompute_distances=False option for a regular numpy array.  Examination of the euclidean_distances function revealed that it can operate on scipy sparse matrices, so it is unclear why this option is not applied for this data type.  

"""

CS 207 algorithm paper

We discuss K-means and K-means++, but do not address Mini-Batch K-means in this paper.  

"""

The following was cut and pasted from https://github.com/scikit-learn/scikit-learn/blob/51a765a/sklearn/cluster/k_means_.py#L660

We have inserted comments to point out the optimizations described above.  
"""

#### THE COMMENTS THAT ARE PART OF THE ORIGINAL CODE HAVE BEEN LEFT IN PLACE.  
#### OUR ADDED COMMENTS AND DISCUSSION ARE BOLDED AND IN ALL CAPS TO MAKE THEM EASY TO IDENTIFY.


### K-means clustering

# Authors: Gael Varoquaux <gael.varoquaux@normalesup.org>
#          Thomas Rueckstiess <ruecksti@in.tum.de>
#          James Bergstra <james.bergstra@umontreal.ca>
#          Jan Schlueter <scikit-learn@jan-schlueter.de>
#          Nelle Varoquaux
#          Peter Prettenhofer <peter.prettenhofer@gmail.com>
#          Olivier Grisel <olivier.grisel@ensta.org>
#          Mathieu Blondel <mathieu@mblondel.org>
#          Robert Layton <robertlayton@gmail.com>
# License: BSD 3 clause

import warnings

import numpy as np
import scipy.sparse as sp

from ..base import BaseEstimator, ClusterMixin, TransformerMixin
### THE euclidean_distances() FUNCTION IS USED THROUGHOUT THE CODE, AND USES FUNCTIONS LIKE slearn.utils.extmath.row_norms AND sklearn.utils.extmath.safe_sparse_dot, WHICH CALL sklearn.sparsefuncs_fast.csr_row_norms, WHICH IS A CYTHON FUNCTION.  ALL OF THIS IS MUCH MORE EFFICIENT THAN IMPLEMENTING THE LINEAR ALGEBRA IN PYTHON.  

from ..metrics.pairwise import euclidean_distances
from ..utils.extmath import row_norms, squared_norm
from ..utils.sparsefuncs_fast import assign_rows_csr
from ..utils.sparsefuncs import mean_variance_axis
from ..utils.fixes import astype
from ..utils import check_array
from ..utils import check_random_state
from ..utils import as_float_array
from ..utils import gen_batches
from ..utils.validation import check_is_fitted
from ..utils.validation import FLOAT_DTYPES
from ..utils.random import choice
### sklearn.externals.joblib.Parallel IS USED TO RUN K-MEANS WITH MULTIPLE INITIALIZATIONS IN PARALLEL USING MULTIPROCESSING.  
from ..externals.joblib import Parallel
from ..externals.joblib import delayed
from ..externals.six import string_types
### THE _k_means FILE IS A CYTHON FILE THAT PERFORMS THE LABEL ASSIGNMENTS AND CLUSTER CENTER DISTANCE CALCULATIONS IN CYTHON.  EACH OF THESE TASKS HAS AN IMPLEMENTATION FOR SCIPY SPARSE MATRICES AND REGULAR NUMPY MATRICES, ALLOWING THE USER TO POTENTIALLY SPEED UP COMPUTATION BY USING SPARSE MATRICES IF THE DATASET IS APPROPRIATE.  
from . import _k_means


###############################################################################
# Initialization heuristic

#### _k_init USES THE K-MEANS++ INITIALIZATION TO HAVE A BETTER CHANCE OF PICKING INITIAL CLUSTER CENTERS THAT BETTER SEPARATE THE DATA, POTENTIALLY LEADING TO FASTER CONVERGENCE AND BETTER RESULTS.  
def _k_init(X, n_clusters, x_squared_norms, random_state, n_local_trials=None):
    """Init n_clusters seeds according to k-means++
    Parameters
    -----------
    X: array or sparse matrix, shape (n_samples, n_features)
        The data to pick seeds for. To avoid memory copy, the input data
        should be double precision (dtype=np.float64).
    n_clusters: integer
        The number of seeds to choose
    x_squared_norms: array, shape (n_samples,)
        Squared Euclidean norm of each data point.
    random_state: numpy.RandomState
        The generator used to initialize the centers.
    n_local_trials: integer, optional
        The number of seeding trials for each center (except the first),
        of which the one reducing inertia the most is greedily chosen.
        Set to None to make the number of trials depend logarithmically
        on the number of seeds (2+log(k)); this is the default.
    Notes
    -----
    Selects initial cluster centers for k-mean clustering in a smart way
    to speed up convergence. see: Arthur, D. and Vassilvitskii, S.
    "k-means++: the advantages of careful seeding". ACM-SIAM symposium
    on Discrete algorithms. 2007
    Version ported from http://www.stanford.edu/~darthur/kMeansppTest.zip,
    which is the implementation used in the aforementioned paper.
    """
    n_samples, n_features = X.shape

    centers = np.empty((n_clusters, n_features))

    assert x_squared_norms is not None, 'x_squared_norms None in _k_init'

    # Set the number of local seeding trials if none is given
    if n_local_trials is None:
        # This is what Arthur/Vassilvitskii tried, but did not report
        # specific results for other than mentioning in the conclusion
        # that it helped.
        n_local_trials = 2 + int(np.log(n_clusters))

    # Pick first center randomly
    center_id = random_state.randint(n_samples)
    if sp.issparse(X):
        centers[0] = X[center_id].toarray()
    else:
        centers[0] = X[center_id]

    # Initialize list of closest distances and calculate current potential
    closest_dist_sq = euclidean_distances(
        centers[0, np.newaxis], X, Y_norm_squared=x_squared_norms,
        squared=True)
    current_pot = closest_dist_sq.sum()

    # Pick the remaining n_clusters-1 points
    for c in range(1, n_clusters):
        # Choose center candidates by sampling with probability proportional
        # to the squared distance to the closest existing center
        rand_vals = random_state.random_sample(n_local_trials) * current_pot
        candidate_ids = np.searchsorted(closest_dist_sq.cumsum(), rand_vals)

        # Compute distances to center candidates
        distance_to_candidates = euclidean_distances(
            X[candidate_ids], X, Y_norm_squared=x_squared_norms, squared=True)

        # Decide which candidate is the best
        best_candidate = None
        best_pot = None
        best_dist_sq = None
        for trial in range(n_local_trials):
            # Compute potential when including center candidate
            new_dist_sq = np.minimum(closest_dist_sq,
                                     distance_to_candidates[trial])
            new_pot = new_dist_sq.sum()

            # Store result if it is the best local trial so far
            if (best_candidate is None) or (new_pot < best_pot):
                best_candidate = candidate_ids[trial]
                best_pot = new_pot
                best_dist_sq = new_dist_sq

        # Permanently add best center candidate found in local tries
        if sp.issparse(X):
            centers[c] = X[best_candidate].toarray()
        else:
            centers[c] = X[best_candidate]
        current_pot = best_pot
        closest_dist_sq = best_dist_sq

    return centers


###############################################################################
# K-means batch estimation by EM (expectation maximization)

def _validate_center_shape(X, n_centers, centers):
    """Check if centers is compatible with X and n_centers"""
    if len(centers) != n_centers:
        raise ValueError('The shape of the initial centers (%s) '
                         'does not match the number of clusters %i'
                         % (centers.shape, n_centers))
    if centers.shape[1] != X.shape[1]:
        raise ValueError(
            "The number of features of the initial centers %s "
            "does not match the number of features of the data %s."
            % (centers.shape[1], X.shape[1]))


def _tolerance(X, tol):
    """Return a tolerance which is independent of the dataset"""
    if sp.issparse(X):
        variances = mean_variance_axis(X, axis=0)[1]
    else:
        variances = np.var(X, axis=0)
    return np.mean(variances) * tol


def k_means(X, n_clusters, init='k-means++', precompute_distances='auto',
            n_init=10, max_iter=300, verbose=False,
            tol=1e-4, random_state=None, copy_x=True, n_jobs=1,
            return_n_iter=False):
    """K-means clustering algorithm.
    Read more in the :ref:`User Guide <k_means>`.
    Parameters
    ----------
    X : array-like or sparse matrix, shape (n_samples, n_features)
        The observations to cluster.
    n_clusters : int
        The number of clusters to form as well as the number of
        centroids to generate.
    max_iter : int, optional, default 300
        Maximum number of iterations of the k-means algorithm to run.
    n_init : int, optional, default: 10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.
    init : {'k-means++', 'random', or ndarray, or a callable}, optional
        Method for initialization, default to 'k-means++':
        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence. See section
        Notes in k_init for more details.
        'random': generate k centroids from a Gaussian with mean and
        variance estimated from the data.
        If an ndarray is passed, it should be of shape (n_clusters, n_features)
        and gives the initial centers.
        If a callable is passed, it should take arguments X, k and
        and a random state and return an initialization.
    precompute_distances : {'auto', True, False}
        Precompute distances (faster but takes more memory).
        'auto' : do not precompute distances if n_samples * n_clusters > 12
        million. This corresponds to about 100MB overhead per job using
        double precision.
        True : always precompute distances
        False : never precompute distances
    tol : float, optional
        The relative increment in the results before declaring convergence.
    verbose : boolean, optional
        Verbosity mode.
    random_state : integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.
    copy_x : boolean, optional
        When pre-computing distances it is more numerically accurate to center
        the data first.  If copy_x is True, then the original data is not
        modified.  If False, the original data is modified, and put back before
        the function returns, but small numerical differences may be introduced
        by subtracting and then adding the data mean.
    n_jobs : int
        The number of jobs to use for the computation. This works by computing
        each of the n_init runs in parallel.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging. For n_jobs below -1,
        (n_cpus + 1 + n_jobs) are used. Thus for n_jobs = -2, all CPUs but one
        are used.
    return_n_iter : bool, optional
        Whether or not to return the number of iterations.
    Returns
    -------
    centroid : float ndarray with shape (k, n_features)
        Centroids found at the last iteration of k-means.
    label : integer ndarray with shape (n_samples,)
        label[i] is the code or index of the centroid the
        i'th observation is closest to.
    inertia : float
        The final value of the inertia criterion (sum of squared distances to
        the closest centroid for all observations in the training set).
    best_n_iter: int
        Number of iterations corresponding to the best results.
        Returned only if `return_n_iter` is set to True.
    """
    if n_init <= 0:
        raise ValueError("Invalid number of initializations."
                         " n_init=%d must be bigger than zero." % n_init)
    random_state = check_random_state(random_state)

    if max_iter <= 0:
        raise ValueError('Number of iterations should be a positive number,'
                         ' got %d instead' % max_iter)

    best_inertia = np.infty
    X = as_float_array(X, copy=copy_x)
### TOLERANCE IS USED HERE TO SPECIFY A CONVERGENCE THRESHOLD TO PREMATURELY STOP THE ALGORITHM WHEN UPDATES ARE MAKING VERY SMALL CHANGES, POTENTIALLY SPEEDING UP THE ALGORITHM IF IT IS TAKING A LONG TIME TO CONVERGE.  
    tol = _tolerance(X, tol)

    # If the distances are precomputed every job will create a matrix of shape
    # (n_clusters, n_samples). To stop KMeans from eating up memory we only
    # activate this if the created matrix is guaranteed to be under 100MB. 12
    # million entries consume a little under 100MB if they are of type double.
### precompute_distances  HAS AN 'auto' OPTION WHICH USES 12e6 ENTRIES AS THE CUTOFF FOR WHEN THE INCREASED MEMORY COSTS OUTWEIGH THE SPEED GAINS FROM PRECOMPUTING DISTANCES.  IF 'auto' IS SPECIFIED, THE ALGORITHM UPDATES precompute_distances TO True OR False BASED ON THIS THRESHOLD.  
    if precompute_distances == 'auto':
        n_samples = X.shape[0]
        precompute_distances = (n_clusters * n_samples) < 12e6
    elif isinstance(precompute_distances, bool):
        pass
    else:
        raise ValueError("precompute_distances should be 'auto' or True/False"
                         ", but a value of %r was passed" %
                         precompute_distances)

    # subtract of mean of x for more accurate distance computations
    if not sp.issparse(X) or hasattr(init, '__array__'):
        X_mean = X.mean(axis=0)
    if not sp.issparse(X):
        # The copy was already done above
        X -= X_mean

    if hasattr(init, '__array__'):
        init = check_array(init, dtype=np.float64, copy=True)
        _validate_center_shape(X, n_clusters, init)

        init -= X_mean
        if n_init != 1:
            warnings.warn(
                'Explicit initial center position passed: '
                'performing only one init in k-means instead of n_init=%d'
                % n_init, RuntimeWarning, stacklevel=2)
            n_init = 1

    # precompute squared norms of data points
### HERE, row_norms() USES CYTHON FUNCTIONS DOWNSTREAM TO CALCULATE THESE NORMS MORE QUICKLY.  
    x_squared_norms = row_norms(X, squared=True)

    best_labels, best_inertia, best_centers = None, None, None
    if n_jobs == 1:
### IF THE USER HAS SPECIFIED n_jobs=1, MULTIPROCESSING IN PARALLEL IS NOT USED BECAUSE THIS WOULD NEEDLESSLY CREATE OVERHEAD FROM SETTING UP THE MULTIPROCCESSING FOR A SINGLE PROCESS. 
        # For a single thread, less memory is needed if we just store one set
        # of the best results (as opposed to one set per run per thread).
        for it in range(n_init):
            # run a k-means once
            labels, inertia, centers, n_iter_ = _kmeans_single(
                X, n_clusters, max_iter=max_iter, init=init, verbose=verbose,
                precompute_distances=precompute_distances, tol=tol,
                x_squared_norms=x_squared_norms, random_state=random_state)
            # determine if these results are the best so far
            if best_inertia is None or inertia < best_inertia:
                best_labels = labels.copy()
                best_centers = centers.copy()
                best_inertia = inertia
                best_n_iter = n_iter_
    else:
        # parallelisation of k-means runs
        seeds = random_state.randint(np.iinfo(np.int32).max, size=n_init)
### IF THE USER HAS SPECIFIED MULTIPLE RE-INITIALIZATIONS TO BE PERFORMED WITH MULTIPLE JOBS, THESE ARE DONE IN PARALLEL HERE.  THE USER CAN EVEN PASS -1 AS AN ARGUMENT TO ALLOW Parallel TO CALCULATE THE APPROPRIATE NUMBER OF CORES TO RUN ON.  
        results = Parallel(n_jobs=n_jobs, verbose=0)(
            delayed(_kmeans_single)(X, n_clusters, max_iter=max_iter,
                                    init=init, verbose=verbose, tol=tol,
                                    precompute_distances=precompute_distances,
                                    x_squared_norms=x_squared_norms,
                                    # Change seed to ensure variety
                                    random_state=seed)
            for seed in seeds)
        # Get results with the lowest inertia
        labels, inertia, centers, n_iters = zip(*results)
        best = np.argmin(inertia)
        best_labels = labels[best]
        best_inertia = inertia[best]
        best_centers = centers[best]
        best_n_iter = n_iters[best]

    if not sp.issparse(X):
        if not copy_x:
            X += X_mean
        best_centers += X_mean

    if return_n_iter:
        return best_centers, best_labels, best_inertia, best_n_iter
    else:
        return best_centers, best_labels, best_inertia


def _kmeans_single(X, n_clusters, x_squared_norms, max_iter=300,
                   init='k-means++', verbose=False, random_state=None,
                   tol=1e-4, precompute_distances=True):
    """A single run of k-means, assumes preparation completed prior.
    Parameters
    ----------
    X: array-like of floats, shape (n_samples, n_features)
        The observations to cluster.
    n_clusters: int
        The number of clusters to form as well as the number of
        centroids to generate.
    max_iter: int, optional, default 300
        Maximum number of iterations of the k-means algorithm to run.
    init: {'k-means++', 'random', or ndarray, or a callable}, optional
        Method for initialization, default to 'k-means++':
        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence. See section
        Notes in k_init for more details.
        'random': generate k centroids from a Gaussian with mean and
        variance estimated from the data.
        If an ndarray is passed, it should be of shape (k, p) and gives
        the initial centers.
        If a callable is passed, it should take arguments X, k and
        and a random state and return an initialization.
    tol: float, optional
        The relative increment in the results before declaring convergence.
    verbose: boolean, optional
        Verbosity mode
    x_squared_norms: array
        Precomputed x_squared_norms.
    precompute_distances : boolean, default: True
        Precompute distances (faster but takes more memory).
    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.
    Returns
    -------
    centroid: float ndarray with shape (k, n_features)
        Centroids found at the last iteration of k-means.
    label: integer ndarray with shape (n_samples,)
        label[i] is the code or index of the centroid the
        i'th observation is closest to.
    inertia: float
        The final value of the inertia criterion (sum of squared distances to
        the closest centroid for all observations in the training set).
    n_iter : int
        Number of iterations run.
    """
    random_state = check_random_state(random_state)

    best_labels, best_inertia, best_centers = None, None, None
    # init
    centers = _init_centroids(X, n_clusters, init, random_state=random_state,
                              x_squared_norms=x_squared_norms)
    if verbose:
        print("Initialization complete")

    # Allocate memory to store the distances for each sample to its
    # closer center for reallocation in case of ties
    distances = np.zeros(shape=(X.shape[0],), dtype=np.float64)

    # iterations
    for i in range(max_iter):
        centers_old = centers.copy()
        # labels assignment is also called the E-step of EM
        labels, inertia = \
### _labels_inertia DETERMINES WHETHER THE MATRIX IS SPARSE OR NOT, AND IF IT IS NOT, DISTANCES ARE OPTIONALLY PRECOMPUTED TO DECREASE RUNTIME.  IN EITHER CASE, LABELING (CLUSTER ASSIGNMENT FOR EACH POINT) IS PERFORMED IN PLACE, WHICH REMOVES THE NEED TO STORE AN EXTRA COPY OF THE ASSIGNMENTS IN MEMORY.  
            _labels_inertia(X, x_squared_norms, centers,
                            precompute_distances=precompute_distances,
                            distances=distances)

        # computation of the means is also called the M-step of EM
### THE _centers_sparse FUNCTION IS WRITTEN IN CYTHON, AND CALCULATES THE CLUSTER CENTERS FOR SCIPY SPARSE MATRICES.  
        if sp.issparse(X):
            centers = _k_means._centers_sparse(X, labels, n_clusters,
                                               distances)
### THE _centers_dense FUNCTION IS WRITTEN IN CYTHON, AND CALCULATES THE CLUSTER CENTERS FOR NUMPY MATRICES
        else:
            centers = _k_means._centers_dense(X, labels, n_clusters, distances)

        if verbose:
            print("Iteration %2d, inertia %.3f" % (i, inertia))

        if best_inertia is None or inertia < best_inertia:
            best_labels = labels.copy()
            best_centers = centers.copy()
            best_inertia = inertia

        shift = squared_norm(centers_old - centers)
        if shift <= tol:
            if verbose:
                print("Converged at iteration %d" % i)

            break

    if shift > 0:
        # rerun E-step in case of non-convergence so that predicted labels
        # match cluster centers
        best_labels, best_inertia = \
            _labels_inertia(X, x_squared_norms, best_centers,
                            precompute_distances=precompute_distances,
                            distances=distances)

    return best_labels, best_inertia, best_centers, i + 1

### _labels_inertia_precompute_dense IS CALLED WHEN THE MATRIX IS A REGULAR (NON-SPARSE) TYPE, AND THE USER ELECTED TO PRECOMPUTE DISTANCES TO REDUCE RUNTIME.  
def _labels_inertia_precompute_dense(X, x_squared_norms, centers, distances):
    """Compute labels and inertia using a full distance matrix.
    This will overwrite the 'distances' array in-place.
    Parameters
    ----------
    X : numpy array, shape (n_sample, n_features)
        Input data.
    x_squared_norms : numpy array, shape (n_samples,)
        Precomputed squared norms of X.
    centers : numpy array, shape (n_clusters, n_features)
        Cluster centers which data is assigned to.
    distances : numpy array, shape (n_samples,)
        Pre-allocated array in which distances are stored.
    Returns
    -------
    labels : numpy array, dtype=np.int, shape (n_samples,)
        Indices of clusters that samples are assigned to.
    inertia : float
        Sum of distances of samples to their closest cluster center.
    """
    n_samples = X.shape[0]
    k = centers.shape[0]
### HERE, DISTANCES ARE PRECOMPUTED INSTEAD OF UPDATED IN A FOR LOOP, MAKING THIS MUCH FASTER.  
    all_distances = euclidean_distances(centers, X, x_squared_norms,
                                        squared=True)
    labels = np.empty(n_samples, dtype=np.int32)
    labels.fill(-1)
    mindist = np.empty(n_samples)
    mindist.fill(np.infty)
    for center_id in range(k):
### THE FOR LOOP GOES OVER THE CLUSTER CENTERS RATHER THAN THE DATA POINTS, SLICING OUT THE PRECOMPUTED DISTANCES FOR THE POINTS ASSIGNED TO THAT CLUSTER.  THIS IS MUCH MORE TIME-EFFICIENT THAN GOING OVER THE DATA POINTS, BUT REQUIRES THE SET OF ALL DISTANCES TO BE STORED IN MEMORY.  
        dist = all_distances[center_id]
### LABELS ARE UPDATED IN PLACE, WHICH IS AN EFFICIENT USE OF MEMORY, AND SLICING IS USED TO PERFORM PERFORM MULTIPLE ASSIGNMENTS SIMULTANEOUSLY.  
        labels[dist < mindist] = center_id
        mindist = np.minimum(dist, mindist)
    if n_samples == distances.shape[0]:
        # distances will be changed in-place
        distances[:] = mindist
    inertia = mindist.sum()
    return labels, inertia

### _labels_inertia DELEGATES THE LABEL ASSIGNMENT TO THE APPROPRIATE FUNCTION BASED ON THE ARRAY TYPE AND WHETHER precompute_distances HAS BEEN SELECTED.  
def _labels_inertia(X, x_squared_norms, centers,
                    precompute_distances=True, distances=None):
    """E step of the K-means EM algorithm.
    Compute the labels and the inertia of the given samples and centers.
    This will compute the distances in-place.
    Parameters
    ----------
    X: float64 array-like or CSR sparse matrix, shape (n_samples, n_features)
        The input samples to assign to the labels.
    x_squared_norms: array, shape (n_samples,)
        Precomputed squared euclidean norm of each data point, to speed up
        computations.
    centers: float64 array, shape (k, n_features)
        The cluster centers.
    precompute_distances : boolean, default: True
        Precompute distances (faster but takes more memory).
    distances: float64 array, shape (n_samples,)
        Pre-allocated array to be filled in with each sample's distance
        to the closest center.
    Returns
    -------
    labels: int array of shape(n)
        The resulting assignment
    inertia : float
        Sum of distances of samples to their closest cluster center.
    """
    n_samples = X.shape[0]
    # set the default value of centers to -1 to be able to detect any anomaly
    # easily
    labels = -np.ones(n_samples, np.int32)
    if distances is None:
        distances = np.zeros(shape=(0,), dtype=np.float64)
    # distances will be changed in-place
### FOR SPARSE MATRICES, DISTANCES ARE NEVER PRECOMPUTED, RATHER THE _k_means._assign_labels_csr IS A CYTHON FUNCTION THAT UPDATES CLUSTER ASSIGNMENTS IN PLACE USING A FOR LOOP.  
    if sp.issparse(X):
        inertia = _k_means._assign_labels_csr(
            X, x_squared_norms, centers, labels, distances=distances)
    else:
        if precompute_distances:
### REGULAR MATRICES HAVE THE OPTION TO USE THE PRECOMPUTATION OPTION ABOVE TO AVOID LOOPING OVER ALL THE DATA POINTS.  
            return _labels_inertia_precompute_dense(X, x_squared_norms,
                                                    centers, distances)
### EVEN IF DISTANCES ARE NOT PRECOMPUTED, THE CLUSTER ASSIGNMENTS ARE PERFORMED IN PLACE, REDUCING MEMORY USAGE, AND BENEFITTING FROM THE EFFICIENCY OF THE CYTHON IMPLEMENTATION IN SPITE OF THE FOR LOOP OVER ALL THE DATA POINTS. 
        inertia = _k_means._assign_labels_array(
            X, x_squared_norms, centers, labels, distances=distances)
    return labels, inertia


def _init_centroids(X, k, init, random_state=None, x_squared_norms=None,
                    init_size=None):
    """Compute the initial centroids
    Parameters
    ----------
    X: array, shape (n_samples, n_features)
    k: int
        number of centroids
    init: {'k-means++', 'random' or ndarray or callable} optional
        Method for initialization
    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.
    x_squared_norms:  array, shape (n_samples,), optional
        Squared euclidean norm of each data point. Pass it if you have it at
        hands already to avoid it being recomputed here. Default: None
    init_size : int, optional
        Number of samples to randomly sample for speeding up the
        initialization (sometimes at the expense of accuracy): the
        only algorithm is initialized by running a batch KMeans on a
        random subset of the data. This needs to be larger than k.
    Returns
    -------
    centers: array, shape(k, n_features)
    """
    random_state = check_random_state(random_state)
    n_samples = X.shape[0]

    if x_squared_norms is None:
        x_squared_norms = row_norms(X, squared=True)

    if init_size is not None and init_size < n_samples:
        if init_size < k:
            warnings.warn(
                "init_size=%d should be larger than k=%d. "
                "Setting it to 3*k" % (init_size, k),
                RuntimeWarning, stacklevel=2)
            init_size = 3 * k
        init_indices = random_state.random_integers(
            0, n_samples - 1, init_size)
        X = X[init_indices]
        x_squared_norms = x_squared_norms[init_indices]
        n_samples = X.shape[0]
    elif n_samples < k:
        raise ValueError(
            "n_samples=%d should be larger than k=%d" % (n_samples, k))

    if isinstance(init, string_types) and init == 'k-means++':
        centers = _k_init(X, k, random_state=random_state,
                          x_squared_norms=x_squared_norms)
    elif isinstance(init, string_types) and init == 'random':
        seeds = random_state.permutation(n_samples)[:k]
        centers = X[seeds]
    elif hasattr(init, '__array__'):
        centers = init
    elif callable(init):
        centers = init(X, k, random_state=random_state)
    else:
        raise ValueError("the init parameter for the k-means should "
                         "be 'k-means++' or 'random' or an ndarray, "
                         "'%s' (type '%s') was passed." % (init, type(init)))

    if sp.issparse(centers):
        centers = centers.toarray()

    _validate_center_shape(X, k, centers)
    return centers

### ALL OF THE FUNCTIONS AND OPTIMIZATIONS ABOVE HAVE BEEN BROUGHT TOGETHER IN THE KMeans CLASS TO PERFORM CLUSTERING EFFICIENTLY.  WE HAVE REMOVED THE MINI-BATCH CODE FROM THIS PAPER FOR BREVITY, BUT THE GIST OF THE MINI-BATCH IMPLEMENTATION IS THAT IT REDUCES COMPUTATION BY OPERATING ON SUBSETS OF THE DATA.  THIS IS AN ALGORITHMIC OPTIMIZATION, AND DOES NOT INTRODUCE ANY ADDITIONAL INTERESTING INTEGRATED C-CODE TO ENHANCE PERFORMANCE.  

class KMeans(BaseEstimator, ClusterMixin, TransformerMixin):
    """K-Means clustering
    Read more in the :ref:`User Guide <k_means>`.
    Parameters
    ----------
    n_clusters : int, optional, default: 8
        The number of clusters to form as well as the number of
        centroids to generate.
    max_iter : int, default: 300
        Maximum number of iterations of the k-means algorithm for a
        single run.
    n_init : int, default: 10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.
    init : {'k-means++', 'random' or an ndarray}
        Method for initialization, defaults to 'k-means++':
        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence. See section
        Notes in k_init for more details.
        'random': choose k observations (rows) at random from data for
        the initial centroids.
        If an ndarray is passed, it should be of shape (n_clusters, n_features)
        and gives the initial centers.
    precompute_distances : {'auto', True, False}
        Precompute distances (faster but takes more memory).
        'auto' : do not precompute distances if n_samples * n_clusters > 12
        million. This corresponds to about 100MB overhead per job using
        double precision.
        True : always precompute distances
        False : never precompute distances
    tol : float, default: 1e-4
        Relative tolerance with regards to inertia to declare convergence
    n_jobs : int
        The number of jobs to use for the computation. This works by computing
        each of the n_init runs in parallel.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging. For n_jobs below -1,
        (n_cpus + 1 + n_jobs) are used. Thus for n_jobs = -2, all CPUs but one
        are used.
    random_state : integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.
    verbose : int, default 0
        Verbosity mode.
    copy_x : boolean, default True
        When pre-computing distances it is more numerically accurate to center
        the data first.  If copy_x is True, then the original data is not
        modified.  If False, the original data is modified, and put back before
        the function returns, but small numerical differences may be introduced
        by subtracting and then adding the data mean.
    Attributes
    ----------
    cluster_centers_ : array, [n_clusters, n_features]
        Coordinates of cluster centers
    labels_ :
        Labels of each point
    inertia_ : float
        Sum of distances of samples to their closest cluster center.
    Notes
    ------
    The k-means problem is solved using Lloyd's algorithm.
    The average complexity is given by O(k n T), were n is the number of
    samples and T is the number of iteration.
    The worst case complexity is given by O(n^(k+2/p)) with
    n = n_samples, p = n_features. (D. Arthur and S. Vassilvitskii,
    'How slow is the k-means method?' SoCG2006)
    In practice, the k-means algorithm is very fast (one of the fastest
    clustering algorithms available), but it falls in local minima. That's why
    it can be useful to restart it several times.
    See also
    --------
    MiniBatchKMeans:
        Alternative online implementation that does incremental updates
        of the centers positions using mini-batches.
        For large scale learning (say n_samples > 10k) MiniBatchKMeans is
        probably much faster to than the default batch implementation.
    """

    def __init__(self, n_clusters=8, init='k-means++', n_init=10, max_iter=300,
                 tol=1e-4, precompute_distances='auto',
                 verbose=0, random_state=None, copy_x=True, n_jobs=1):

        self.n_clusters = n_clusters
        self.init = init
        self.max_iter = max_iter
        self.tol = tol
        self.precompute_distances = precompute_distances
        self.n_init = n_init
        self.verbose = verbose
        self.random_state = random_state
        self.copy_x = copy_x
        self.n_jobs = n_jobs

    def _check_fit_data(self, X):
        """Verify that the number of samples given is larger than k"""
        X = check_array(X, accept_sparse='csr', dtype=np.float64)
        if X.shape[0] < self.n_clusters:
            raise ValueError("n_samples=%d should be >= n_clusters=%d" % (
                X.shape[0], self.n_clusters))
        return X

    def _check_test_data(self, X):
        X = check_array(X, accept_sparse='csr', dtype=FLOAT_DTYPES,
                        warn_on_dtype=True)
        n_samples, n_features = X.shape
        expected_n_features = self.cluster_centers_.shape[1]
        if not n_features == expected_n_features:
            raise ValueError("Incorrect number of features. "
                             "Got %d features, expected %d" % (
                                 n_features, expected_n_features))

        return X

    def fit(self, X, y=None):
        """Compute k-means clustering.
        Parameters
        ----------
        X : array-like or sparse matrix, shape=(n_samples, n_features)
        """
        random_state = check_random_state(self.random_state)
        X = self._check_fit_data(X)

        self.cluster_centers_, self.labels_, self.inertia_, self.n_iter_ = \
            k_means(
                X, n_clusters=self.n_clusters, init=self.init,
                n_init=self.n_init, max_iter=self.max_iter,
                verbose=self.verbose, return_n_iter=True,
                precompute_distances=self.precompute_distances,
                tol=self.tol, random_state=random_state, copy_x=self.copy_x,
                n_jobs=self.n_jobs)
        return self

    def fit_predict(self, X, y=None):
        """Compute cluster centers and predict cluster index for each sample.
        Convenience method; equivalent to calling fit(X) followed by
        predict(X).
        """
        return self.fit(X).labels_

    def fit_transform(self, X, y=None):
        """Compute clustering and transform X to cluster-distance space.
        Equivalent to fit(X).transform(X), but more efficiently implemented.
        """
        # Currently, this just skips a copy of the data if it is not in
        # np.array or CSR format already.
        # XXX This skips _check_test_data, which may change the dtype;
        # we should refactor the input validation.
        X = self._check_fit_data(X)
        return self.fit(X)._transform(X)

    def transform(self, X, y=None):
        """Transform X to a cluster-distance space.
        In the new space, each dimension is the distance to the cluster
        centers.  Note that even if X is sparse, the array returned by
        `transform` will typically be dense.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data to transform.
        Returns
        -------
        X_new : array, shape [n_samples, k]
            X transformed in the new space.
        """
        check_is_fitted(self, 'cluster_centers_')

        X = self._check_test_data(X)
        return self._transform(X)

    def _transform(self, X):
        """guts of transform method; no input validation"""
        return euclidean_distances(X, self.cluster_centers_)

    def predict(self, X):
        """Predict the closest cluster each sample in X belongs to.
        In the vector quantization literature, `cluster_centers_` is called
        the code book and each value returned by `predict` is the index of
        the closest code in the code book.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data to predict.
        Returns
        -------
        labels : array, shape [n_samples,]
            Index of the cluster each sample belongs to.
        """
        check_is_fitted(self, 'cluster_centers_')

        X = self._check_test_data(X)
        x_squared_norms = row_norms(X, squared=True)
        return _labels_inertia(X, x_squared_norms, self.cluster_centers_)[0]

    def score(self, X, y=None):
        """Opposite of the value of X on the K-means objective.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data.
        Returns
        -------
        score : float
            Opposite of the value of X on the K-means objective.
        """
        check_is_fitted(self, 'cluster_centers_')

        X = self._check_test_data(X)
        x_squared_norms = row_norms(X, squared=True)
        return -_labels_inertia(X, x_squared_norms, self.cluster_centers_)[1]


d
### BELOW IS THE BASIC PYTHON K-MEANS IMPLEMENTATION THAT WE WROTE.  THIS WAS GENERATED FOR AND TESTED ON 28*28 PIXEL IMAGES OF HANDWRITTEN DIGITS, SO THE DISPLAY CODE REFLECTS THAT.  THIS WAS ORIGINALLY WRITTEN AS PART OF A HOMEWORK ASSIGNMENT FOR CS181: MACHINE LEARNING. 

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# L2 norm
def distance(image1, image2):
    difference = image1 - image2
    return np.sum(difference**2)

class KMeans(object):
    # K is the K in KMeans
    # useKMeansPP is a boolean. If True, initialize using KMeans++
    def __init__(self, K, useKMeansPP):
        self.K = K
        self.useKMeansPP = useKMeansPP

    # X is a (N x 28 x 28) array where 28x28 is the dimensions of each of the N images.
    def fit(self, X, show_initial=False):
        # Create an empty array of K cluster centers that will be initialized and updated. 
        cluster_centers = np.zeros((self.K, X.shape[1], X.shape[2]))

        # Create arrays to store the cluster identities of each image.
        N = X.shape[0] # number of images
        cluster_ids = np.zeros(N)
        cluster_ids_old = np.zeros(N) # To hold last iteration's clusters to compare for convergence.

        if self.useKMeansPP==False:
            # 1) Define random initial cluster centers using Forgy's method:

            # Sample indices for the points that will be used as initial cluster centers:
            idxs = np.random.choice(X.shape[0], self.K, replace=False)

            # Assign the sampled points to be the initial cluster centers. 
            cluster_centers[range(self.K)] = X[idxs]

        else: # K-means ++
            # Pick the first cluster center randomly.
            cluster_centers[0] = X[np.random.randint(N)]

            # Array of probabilities of selecting each point to be the next cluster center.
            prob = np.zeros(N)

            for i in range(1,self.K):
                # For each of the remaining cluster centers, calculate distances from each cluster
                #   center that has been defined to each data point, and assign the minimum of these
                #   distances as the probability of selecting that point to be the next cluster center.  
                for k in range(N):
                    prob[k] = np.min([distance(X[k], cluster_centers[j]) for j in range(0,i+1)])
                # Normalize probabilities.  
                prob = prob/sum(prob)
                # Select index of the next cluster
                index_of_next_cluster_center = np.random.choice(range(N),size=1,p=prob)
                cluster_centers[i] = X[index_of_next_cluster_center]

        if show_initial==True: # Show initial cluster means
            initials = np.zeros((X.shape[1], self.K*X.shape[2]))
            for i in range(self.K):
                initials[:,i*X.shape[2]:(i+1)*X.shape[2]] = cluster_centers[i]
            plt.figure()
            plt.imshow(-initials, cmap='Greys_r')
            plt.savefig('img12.png')
            plt.show()

        # 2) Start iteratively assigning all the images to their closest cluster center

        counter = 0

        # Array used to store distances used to calculate objective function.  
        objectives = np.zeros(N)
        # List of objective function values at each iteration
        objective = []

        while True:#not converged:
            # Assign every image to its closest cluster center
            for i in range(N):
                # Calculate norm to every cluster center and store to calculate objective function value
                dists = [distance(X[i], cluster_centers[j]) for j in range(self.K)]
                objectives[i] = np.min(dists)

                # Assign the image to the closest cluster center.
                cluster_id = np.argmin(dists)
                cluster_ids[i] = cluster_id

            objective.append(np.sum(objectives))
            # Verify that objective function only increases:
            if objective[counter] > objective[counter-1]:
                print "Objective function increased!"
            
            # After each pass through all the images, update the cluster centers to the mean of each.
            cluster_centers = [np.mean(X[cluster_ids==i], axis=0) for i in range(self.K)]

            # After each pass through all the images, check for convergence.  
            # If the cluster assignments are the same as last iteration, break.   
            if np.array_equal(cluster_ids_old, cluster_ids): 
                break

            # If we haven't converged, keep a copy of this iteration's results for the next one.  
            cluster_ids_old = np.copy(cluster_ids)

            counter += 1
            if counter%1==0:
                print counter

        # Store the images, means, and cluster assignments to use later
        self.X = X
        self.N = len(X)
        self.means = cluster_centers 
        self.clusters = cluster_ids_old

        # Show plot of objective function values over time.  
        plt.figure()
        plt.plot(objective)
        plt.xlabel("Iterations")
        plt.ylabel("Value of Objective Function")
        plt.title("Objective Function Value over Time")
        # plt.savefig("obj.png")
        plt.show()


    # This should return the arrays for K images. Each image should represent the mean of each of the fitted clusters.
    def get_mean_images(self):
        return self.means

    # This should return the arrays for D images from each cluster that are representative of the clusters.
    def get_representative_images(self, D):
        # Here, I define shortest distance to the cluster mean as most representative of the cluster.  

        # Empty array, to fill each row with the representative images for each cluster.  
        rep_images = np.zeros((self.K, D, self.X.shape[1], self.X.shape[2]))

        for i in range(self.K):
            # For each cluster, sort the images by their distance from the cluster mean.  
            
            distances = []              # Distances from mean for each cluster
            idxs = []                   # Indexes of each distance in the distance list
            mask = (self.clusters==i)   # Mask to use only the images in this cluster.  

            for j in range(self.N): 
                if mask[j]==True:   # Consider only the images in this class.
                    # For each image in the cluster, calculate the distance from the cluster mean.  
                    distances.append(distance(self.X[j], self.means[i]))
                    idxs.append(j)

            # Get the indices of the order of the distances for the cluster.     
            order = np.argsort(distances)
            # Take the specified number from the list, and slice out the corresponding indexes from the list
            #   created in the loop.  
            indexes = np.array(idxs)[order[:D]]

            # Use the indexes to call the appropriate images.  
            rep_images[i,:] = self.X[[indexes]]

        return rep_images


    # img_array should be a 2D (square) numpy array.
    # Note, you are welcome to change this function (including its arguments and return values) to suit your needs. 
    # However, we do ask that any images in your writeup be grayscale images, just as in this example.
    def create_image_from_array(self, img_array):
        plt.figure()
        plt.imshow(img_array, cmap='Greys_r')
        plt.savefig('img5.png')
        plt.show()
        return

# This line loads the images.
pics = np.load("images.npy", allow_pickle=False)

K = 10
num_ex = 4

KMeansClassifier = KMeans(K, useKMeansPP=True)
KMeansClassifier.fit(pics, show_initial=False)
cluster_means = KMeansClassifier.get_mean_images()

representative_images = KMeansClassifier.get_representative_images(num_ex)


# Make an empty array to hold the output display.  

# Separator in the output array to distinguish cluster means from representative examples.  
sep_width = 2

# It has a column for the means, a separator
cluster_examples=np.zeros((K * 28, 28 + sep_width + 28*num_ex))

# Fill in the separator as the max pixel value to make a dark vertical bar
cluster_examples[:,28:28+sep_width] = np.max(pics[0])

# Fill in the rows
for i in range(K):
    # Cluster means
    cluster_examples[i*28:(i+1)*28, 0:28] = cluster_means[i]

    for j in range(num_ex):
        # Representative images
        cluster_examples[i*28:(i+1)*28, sep_width+28+j*28:sep_width+28+(j+1)*28]=representative_images[i,j]
        
KMeansClassifier.create_image_from_array(-cluster_examples)