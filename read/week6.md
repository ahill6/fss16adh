Harman, Mark, Yue Jia, and William B. Langdon. "Babel pidgin: SBSE can grow and graft entirely new functionality into a real world system." International Symposium on Search Based Software Engineering. Springer International Publishing, 2014.

### ii. Keywords
ii1: Genetic Improvement (GI) - An SBSE technique which involves treating blocks of code as the "genetic material" for a genetic algorithm.

ii2: Grow and Graft - First, grow a new piece of code with desired functionality using Genetic Programming (GP) and some guidance (e.g. unit tests).  Second, use GP to find suitable locations to insert this new code into an existing piece of software in order to integrate the new functionality.

ii3: Aggressive Elitism - During the selection phase of a Genetic Algorithm, take many more of the best solutions and cull many of the worst.  Here they insert mutations of the best solution between 1 and 250 times for population of 500.

ii4: Coupon Collector Distribution - A distribution based on the Coupon Collection problem in mathematics.  The distribution is a generalization of how long it will take to get a desired number of items when arrival times are geometrically distributed.  E(x) = nlog(n)

### iii. A Few Notes
iii1: Motivation - The paper is testing the Grow and Graft method of generating new functionality for programs and integrating it within an existing program.

iii2: Related Work - A significant part of the introduction is dedicated to showing how this work fits within larger trends in SE, and within GP in particular.

iii3: New Results - The paper reports many new findings or suggestions, such as:
+ First time new functionality was successfully made and integrated autonomously via GP.
+ The description of the Grow and Graft technique as a hyper-heuristic for software modification

iii4: Future Work - The authors successfully created one new piece of functionality in a system which was 50k Lines of Code (LoC).  This result must be replicated in other systems.

### iv. Weaknesses
iv1: Overstated Results - The title/abstract claim real-world success for their technique, but the paper makes clear that this technique requires significantly more human guidance than the title/abstract implied.

iv2: Limited General Use - This technique requires extensive rule creation to guide the GP.  The authors argue (with some merit) that the result can be achieved using only the rules which are predominantly automatically generated, but the framework will need modification before it is generally applicable.

iv3: Computationally Infeasible - The GP completed enumerated the entire graft space.  For this example that was only size 46, of which the majority failed to compile or quickly errored.  Still, enumeration of all possibilities raises serious questions about scalability.

### v. Connection To Other Papers
The purpose of the paper is as stated in the "Motivation" section.  That fits within Harman's larger scheme as introduced in the base paper of creating dynamic software via hyper-heuristics.  Grow and Graft is one such heuristic that the author is using to make dynamic software in this paper.
