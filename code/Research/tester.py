#!/usr/bin/env python
'''
CREATED:2011-11-12 08:23:33 by Brian McFee <bmcfee@cs.ucsd.edu>
MODIFIED: starting 2016-09-08 by Andrew Hill <ahill6@ncsu.edu>
Spatial tree demo for matrix data
'''
import numpy, random, sys, pprint, timeit
from spatialtree import spatialtree
from fileio import summarize, csv_reader2, make_stats, csv_reader
from numpy.linalg.linalg import LinAlgError


results_memo = {}
def matrixDemoTestWorker(size = None, dimensions = None, tree_type = None, spill_rate = None, samp = None, k_neighbors = None, tree_depth=None, files=None):
    #this_run = dict()
    
    # Create random matrix
    N = size or 5000
    D = dimensions or 20 
    
    # Create testing variables
    tree= tree_type or 'kd'
    spill = spill_rate or .25
    samples = samp or 100
    k_near = k_neighbors or 10
    k = 5
    max_value = 100
    filename = files
    
    # Python interprets spill_layer = 0 as False, and so sets spill to .25
    if spill_rate == 0:
        spill = 0
    
        
    # read in the data
    filedata,reduceddata, removed = csv_reader2(filename)
    N = len(filedata)
    D = len(filedata[0])
    #reducedD = len(reduceddata[0])
    timer = open(tree+".txt", 'w')
    
    c = list(zip(filedata, reduceddata))
    random.shuffle(c)
    filedata, reduceddata = zip(*c)

    # divide the data into 5 groups for cross validation
    Y = [[] for i in xrange(5)]
    Z = [[] for i in xrange(5)]
    """
    i = 0
    for item in filedata:
        Y[i%5].append(item)
        i += 1
    """
    i = 0
    for item in reduceddata:
        Z[i%5].append(item)
        Y[i%5].append(item)
        i += 1
        
    for k in range(len(Y)):
        print("Building ", tree_type)
        t = []
        for x in xrange(len(Z)):
            if x != k:
                t.extend(Z[x])
        training = numpy.array(t)
        t2 = []
        for x in xrange(len(Y)):
            if x != k:
                t2.extend(Y[x])
        training_real = numpy.array(t2)
        
        start_time = timeit.default_timer()
        #T = spatialtree(training, spill=spill, height=tree_depth, rule='entropic')
        T = spatialtree(training, spill=0, height = tree_depth, rule=tree)
        elapsed = timeit.default_timer() - start_time
        timer.write(str(elapsed) + ",")
        #print("mine:\t" + str(elapsed))
        
        #start_time = timeit.default_timer()
        #T2 = spatialtree(training_real, spill=spill, height=tree_depth, rule=tree)
        #elapsed = timeit.default_timer() - start_time
        #print("theirs:\t" + str(elapsed))
        #print 'done.'
        
        # If we want to compare accuracy against brute-force search,
        # we can make a height=0 tree:
        
        T_root = spatialtree(training, height=0)
        index = '' + tree + '_' + str(spill) + '_' + str(tree_depth)
        
        recall = 0
        f = open(index + ".txt", 'w')
        # Generate test points from the test set
        for test_point in range(len(Y[k])):
            
            #print(this, test_point, len(Y[4]), len(Z[4]))
            test2 = Y[k][test_point]
            test = Z[k][test_point]
        
            # Find the 10 approximate nearest neighbors of the 500th data point
            # returned list is row#'s of X closest to the query index, 
            # sorted by increasing distance
            knn_a = T.k_nearest(training, k=k_near, vector = test)
            #print 'KNN approx (index) : ', knn_a
            #print(training[knn_a[0]])
            
            
            #knn_b = T2.k_nearest(training_real, k=k_near, vector = test2)
            #print 'KNN approx (index) : ', knn_b
        
            # Now, get the true nearest neighbors
            knn_t = T_root.k_nearest(training, k=k_near, vector = test2)
            #knn_t = T_root.k_nearest(training_real, k=2*k_near, vector = test2)
            #print 'KNN true   (index) : ', knn_t
            #print(training_real[knn_t[0]])
            
            true_pos = len(set(knn_a) & set(knn_t)) * 1.0
            false_pos = len(set(knn_t)) - true_pos
            true_neg = len(training) - false_pos
            f.write(str(true_pos) + '-' + str(false_pos) + '-' + str(true_neg) + ',')
            recall += true_pos / len(set(knn_t))
    f.write("\n")
    f.close()
    timer.close()
    return N, D
        #return N,D # return the number of entries and decisions so they can be passed to data postprocessing

def matrixTestMaster(samples, trials, size = None, dimensions = None, tree_type = None, spill_rate = None, samp = None, k_neighbors = None):
    #call the method with different tree types, spill levels, et al  many times and average/collate the data 
    #All cases listed first for ease of reference
    #results = dict()
    #trees = ['kd', 'pca', '2-means', 'rp', 'where', 'random', 'spectral', 'entropic2']
    #spill_rates = [0, 0.01, 0.05, 0.10, 0.15, 0.2, 0.25]
    #tree_depth = [5, 6, 7, 8, 9, 10, 11, 12, 13]
    #files = ['cassandra.csv', 'diabetes.csv', 'mccabes_mc12.csv', 'testdata.csv']
    tree_depths = [5, 7, 9, 11, 13]
    trees = ['pca', 'kd']
    spill_rates = [0]
    files = ['mccabes_mc12.csv']
    
    n = 0
    d = 0
    
    for b in files:
        for x in xrange(len(trees)):
            for y in xrange(len(spill_rates)):
                for z in xrange(len(tree_depths)):
                    for a in xrange(trials):
                        try:
                            n, d = matrixDemoTestWorker(tree_type = trees[x], spill_rate = spill_rates[y], tree_depth = tree_depths[z], files=b)
                        except LinAlgError:
                            break
                        
    #make_stats(num_entries = n, num_decisions=d)

def pretty_print(d):
    for k in sorted(d.keys()):
        print k,"\t\t : ", d[k]
    
matrixTestMaster(0, 1)
