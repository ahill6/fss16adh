### i. Paper
Harman, Mark, John Clark, and Mel O. Cinneidez. "Dynamic adaptive Search Based Software Engineering needs fast approximate metrics (keynote)." Emerging Trends in Software Metrics (WETSoM), 2013 4th International Workshop on. IEEE, 2013.

### ii. Keywords
ii1: SBSE for Metrics - The use of SBSE optimization techniques as a means of evaluating metrics on a space.  That is, because the optimization is guided by the fitness function, you can use an optimization technique to compare metrics.

ii2: Metametrics - Metrics which describe how different metrics relate to one another (i.e which are "close")

ii3: Dissonant Metrics - A pair of metrics for a given problem (which claim to measure the same thing) for which code refactoring causes one metric to change, but not the other.

ii4: Conflicted Metrics - A pair of metrics (which claim to measure the same thing) for a given problem for which code refactoring leads one metric to increase, and the other to decrease.

### iii. A Few Notes
iii1: Motivation - The paper describes a new application of SBSE techniques to metric evaluation and discusses the importance of fast metrics, even if they are approximate.

iii2: Related Work - The authors give extensive references to the papers which inspired this work.  Each section begins with a brief literature review, in addition to a "Further Reading" section at the conclusion.

iii3: New Results - The most important new result in this paper was the finding that 38% of studied metrics which claimed to measure code cohesion were conflicted metrics (see Keyword section).

iii4: Future Work - The paper suggested that future work on metametrics could provide clarity on why metrics claiming to measure the same quantity respond differently to code refactoring. 


### iv. Weaknesses
iv1: Chasing Rabbits - After spending most of the paper discussing problems with the metrics studied and the importance of fast approximate metrics, the last half page is a philosophical reflection on the nature of software engineering.  While interesting, it did not go with the rest of the paper.

iv2: Use of Space - The important claims are not given enough room in this paper.  It puts forward an important and shocking claim that not only do metrics determine results, but the most commonly used metrics in the area studied disagree.  This is an important issue, but the paper moves on from it after little more than 1-2 pages.

iv3: Concrete Suggestions - The portions of the paper not devoted to the need for metametrics bring up the importance of fast approximate metrics, but offer no concrete suggestions of fruitful directions or background on successful attempts to find such metrics.

### v. Connection To Other Papers
This paper represents a step forward for the agenda laid out in the base paper.  The agenda has found its first obstacle: the lack of understanding on the influence of metrics on optimization outcomes, and the lack of tools with which to compare what metrics are used by different algorithms.
