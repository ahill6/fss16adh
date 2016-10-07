### i .Paper
de Carvalho, Vinicius Renan, Silvia Regina Vergilio, and Aurora Pozo. "Uma hiper-heurıstica de seleç ao de meta-heurısticas para estabelecer sequências de módulos para o teste de software."

### ii. Keywords
ii1: Choice Function - A function used to select which of several optimizers or optimizees will be used (e.g. use NSGA-II or SPEA-2, optimize hypervolume or RNI)

ii2: Multiobjective Optimization and Coupling-based Approach for the Integration and Test Order problem using Hyper Heuristics (MOCAITO-HH) - The algorithm suggested by the paper, which uses hyper-heuristics to decide which MOEA algorithm to use

ii3: Hyper Heuristic - A choice of what meta-heuristic to use, or a heuristic for how to select heuristics.

ii4: Ratio of Non-dominated Individuals (RNI) - The ratio nd/p where nd = number of non-dominated individuals and p = population size.  Can be used as a metric to be optimized or as a measure of algorithm effectiveness

### iii. A Few Notes
iii1: Motivation - This paper seeks to automate the task of selecting the best meta-heuristic/algorithm to use in a given optimization program.  

iii2: Related Work - The authors acknowledge this line of research goes back to 2001, and have a particularly detailed "Related Work" section detailing research in hyper-heuristics for 2012-2015.

iii3: New Results - The paper reports many new findings or suggestions, such as:
+ The authors' MOCAITO-HH algorithm successfully replicates the performance of the best algorithm, and automatically selects which algorithm is appropriate to the situation
+ As a means to the above goal, this paper presents a means of comparing algorithmic effectiveness across many quality measures

iii4: Future Work - This algorithm needs to be applied to more test cases, and the authors mention that they would like to try other Choice Functions.

### iv. Weaknesses
iv1: Little Analysis - The choice function and rest of the algorithm are both rather complex, but the paper never addresses how each part contributes.  It is possible only one portion of the algorithm is what is accomplishing the results, but without analysis of it, that is left unexplored.

iv2: Few Test Cases - The paper's results are only for four test cases.  More evidence from more varied sources is needed.

iv3: Magic Parameters - The authors' algorithm requires magic parameters, which they set by trial-and-error.

### v. Connection To Other Papers
This paper is a response to the base paper calling for more studies in the usefulness of hyper-heuristics to SBSE.
