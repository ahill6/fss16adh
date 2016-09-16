### i. Paper
Weimer, Westley, et al. "Automatically finding patches using genetic programming." Proceedings of the 31st International Conference on Software Engineering. IEEE Computer Society, 2009.

### ii. Keywords
ii1: Abstract Syntax Tree - A tree representation of source code for a given programming language, often used for semantic analysis in compilers.

ii2: Stochastic Universal Sampling (SUS) - A means of selecting individuals for the crossover step in a genetic algorithm which reduces the fitness-based bias in selection.  Some GAs can be dominated by a single extremely fit individual early in the process.

ii3: k-minimal subset - An "interesting" subset such that removing any k elements from it makes it "uninteresting," where "interesting" is defined as desired.  This algorithm generates a 1-minimal patch.

ii4: Genetic Programming (GP) - A method inspired by evolution, in which a population undergoes crossover (reproduction), mutation, and then is evaluated by a fitness function to cull some members of the population.

### iii. A Few Notes
iii1: Motivation - This paper presents the first (to the authors' knowledge) successful implementation of GA to automatically repair multiple types of code defects without metadata, modifications to coding practices, or formal specifications.  It uses unit tests to define problems and desired behavior.

iii2: Theoretical Background - The paper gives extensive pseudocode and GA-based explanations for why each design decision was made, as well as giving a full walkthrough of a test-program from human analysis and explanation of the problem through each step of machine solution and presents the algorithm-generated patch.

iii3: New Results - The paper reports many findings, such as:
+ A new way of representing programming operations which allows efficient scaling of GP for automatic repair problems
+ Empirical results showing success in automatic program repair of multiple defect types 
+ An algorithm to conduct program repair with the above results based on test cases that describe problems and desired functionality

iii4: Future Work - The expansion of this algorithm to more complex code defects (only 2 programs tested required more than 4 lines to fix).  In addition, the algorithm assumes that all mistakes have something already in the program which can fix the defect.  Extension to use code libraries would be a next step.


### iv. Weaknesses
iv1: When Will This Work -  Algorithm presented will not work if the problem is overdetermined or underdetermined (too many or too few test cases), but no means of determining these parameters is given.  

iv2: Scalability - The paper does not give any indication of whether this technique will scale.

iv3: Parameter Tuning - The algorithm uses a weighted path metric to reduce the portion of the code considered for code defects.  The parameters of this weighting are somewhat arbitrarily chosen and may require tuning. 

### v. Connection To Other Papers
This paper was given by the original paper as an example of the new and exciting work done in the field, an exemplar of the type of accomplishments the author was hoping would occur regularly if his vision for the future was followed.
