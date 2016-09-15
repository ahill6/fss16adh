Harman, Mark, and Phil McMinn. "A theoretical and empirical study of search-based testing: Local, global, and hybrid search." IEEE Transactions on Software Engineering 36.2 (2010): 226-247.

### ii. Keywords
ii1: Schema Theory - An expansion of the work of John Holland, the theoretical underpinning of Genetic Algorithms, which explains why genetic algorithms work.  The properties sometimes fail in Evolutionary and multimodal cases.

ii2: Royal Road - Genetic/Evolutionary Algorithms rely on an assumption that some subset of fit behaviors also encourage fitness (i.e. if you cross-breed two fit solutions, you will not destroy what was good about them).  Royal Road Theory/Functions/Properties address what type of spaces, functions, properties are necessary for this to be a reasonable assumption (i.e. they attempt to say when using an Evolutionary-type algorithm is a good idea).

ii3: Hybrid Search Techniques - The combination of a greedy algorithm and an evolutionary or genetic technique in an effort to get the best of both.

ii4: Search Based Testing - The application of SBSE to the generation of software tests and program testing coverage.

### iii. A Few Notes
iii1: Motivation - The paper responds to a lack of theory by providing a theoretical foundation for Search-Based Testing, making predictions based on the theory, then doing empirical tests to validate the predictions.

iii2: Theoretical Background - In order to provide theory, the paper develops a generalization of existing work which updates work on Genetic Algorithms to apply to Evolutionary Algoithms.

iii3: New Results - The paper reports many findings, such as:
+ Greedy methods were far more competitive than expected under a variety of conditions
+ Development and presentation of a hybrid method which used a Hill-climber to save work and an Evolutionary Algorithm to get in those hard-to-reach corners.
+ Provided theory that the authors claimed did not previously exist.

iii4: Future Work - Expansion of the theory presented, improving the hybrid method used (it failed to reach one pathological branch that an Evolutionary Algorithm did reach), and a practical means of identifying whether the current location calls for a hill-climber or an evolutionary algorithm.


### iv. Weaknesses
iv1: Length - The paper was over 20 pages, making it the longest paper I have encounted outside of book chapters.  Several sections could have been reduced in size without impacting the quality of the work.

iv2: Unnecessary Citations - Section 6 is a "Related Work" section which includes listing the 20-year-old paper that first conceived of some parts of the field.  It seemed the authors were just going for more references.

iv3: Test Case - The authors repeatedly referenced a test case having to do with ISBNs, but never explained what they were testing or how.

### v. Connection To Other Papers
This paper supplies much of the background in the area of Search-Based Testing for the base paper, as well as providing a theoretical framework from which the base paper proposes future directions.
