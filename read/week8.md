### i .Paper
Kumari, A. Charan, and K. Srinivas. "Hyper-heuristic approach for multi-objective software module clustering." Journal of Systems and Software 117 (2016): 384-401.

### ii. Keywords
ii1: Module Dependency Graphs (MDGs) - A graphical method of describing software modules (clusters of highly-interdependent code snippets)

ii2: Modularization Quality (MQ) - A single measure combining coupling and cohesion in order to try to balance them so that excessive coupling is limited

ii3: Maximizing Cluster Approach (MCA) - A clustering algorithm which seeks to maximize interdependence within clusters, minimize dependence between clusters, maximize the number of clusters and MQ, while minimizing isolated clusters.

ii4: Equal-size Cluster Approach (ECA) - A clustering algorithm which seeks to minimize the difference between the maximum and minimum number of modules in a cluster, as well as all objectives of MCA (except minimizing isolated clusters)

### iii. A Few Notes
iii1: Motivation - This paper presents a new algorithm for clustering software modules to improve maintainability, as well as a tool built to demonstrate their algorithm.

iii2: Related Work - The authors' related work section includes a summary of the development of their chosen fitness functions and a literature defense of their choice of metrics to compare algorithms.  It is thorough while also compact.

iii3: New Results - The paper reports many new findings or suggestions, such as:
+ The authors' MHypEA algorithm finds solutions comparable to SA, NSGA-II, and Two-Archive algorithms on problems for which those are claimed to be best suited, at a reduction of nearly 95% in runtime.
+ The authors use their result to suggest hyper-heuristics as a means of making general-use algorithms capable of selecting the best metaheuristic for each problem automatically.

iii4: Future Work - The authors only real-world datasets were MDGs without edge weights.  This is because they could not convince an author with an edge-weighted dataset to let them use it and generated simulated data instead.  Still, validating their results on MDGs with edge weights is needed.

### iv. Weaknesses
iv1: Poorly Organized and Overwhelming Data - One positive of this paper is that it makes extensive use of data.  Every claim is supported by some discussion of data or statistical test, and much of the data is provided in the paper itself.  That being said, the data is not presented in a way which is easy to read.  There are nearly 11 pages of graphs/charts/screenshots in a 15 page paper (not including reference section).  About 7 of those pages should have been made available on github rather than cluttering the paper with unnecessary information.

iv2: Overstating Results - The paper supports every claim with data.  However, the interpretation of the data sometimes neglects to mention that the difference is a small effect or overstates the implications for industry of a difference which is barely sufficient to be statistically significant.

iv3:  - The authors' algorithm requires magic parameters, which they set by trial-and-error.

### v. Connection To Other Papers
This paper is a response to the base paper calling for more studies in the usefulness of hyper-heuristics to SBSE.  In fact, the authors explicitly mention the base paper as their inspiration their technique.
