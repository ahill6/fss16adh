### i. Paper
Weimer, Westley, et al. "Automatically finding patches using genetic programming." Proceedings of the 31st International Conference on Software Engineering. IEEE Computer Society, 2009.

### ii. Keywords
ii1: Abstract Syntax Tree - A tree representation of source code for a given programming language, often used for semantic analysis in compilers.

ii2: Stochastic Universal Sampling (SUS) - A means of selecting individuals for the crossover step in a genetic algorithm which reduces the fitness-based bias in selection.  The benefit is that some GAs can be dominated by a single extremely fit individual early in the evolutionary process.

ii3: k-minimal subset - An "interesting" subset such that removing any k elements from it makes it "uninteresting," where "interesting" is defined by a specified fitness function or process.  This algorithm generates the smallest patch by making the patch a 1-minimal subset of software changes to the original (buggy) program.

ii4: Genetic Programming (GP) - A method inspired by evolution, in which a population undergoes crossover (reproduction), mutation, and then is evaluated by a fitness function to cull some members of the population.

### iii. A Few Notes
iii1: Motivation - This paper presents the first (to the authors' knowledge) successful implementation of GA to automatically repair multiple types of code defects without metadata, modifications to coding practices, or formal specifications.  The system makes use of unit tests which in some cases can also be automatically generated to define/maintain desired behavior during code modification.

iii2: Theoretical Background - In order to provide theory, the paper develops a generalization of existing work which updates work on Genetic Algorithms to apply to Evolutionary Algoithms.

iii3: New Results - The paper reports many findings, such as:
+ A new way of representing programming operations which allows efficient scaling of GP for automatic repair problems
+ Empirical results showing success in automatic program repair of multiple defect types 
+ An algorithm to conduct program repair with the above results based on test cases that describe problems and desired functionality

iii4: Future Work - .


### iv. Weaknesses
iv1: xxx - The paper was over 20 pages, making it the longest paper I have encounted outside of book chapters.  Several sections could have been reduced in size without impacting the quality of the work.

iv2: xxx - Section 6 is a "Related Work" section which includes listing the 20-year-old paper that first conceived of some parts of the field.  It seemed the authors were just going for more references.

iv3: xxx - The authors repeatedly referenced a test case having to do with ISBNs, but never explained what they were testing or how.

### v. Connection To Other Papers
This paper supplies much of the background in the area of Search-Based Testing for the base paper, as well as providing a theoretical framework from which the base paper proposes future directions
