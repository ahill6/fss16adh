##Antonio Filieri, Carlo Ghezzi, Alberto Leva, and Martina Maggio. 2011. Self-adaptive software meets control theory: A preliminary approach supporting reliability requirements. In Proceedings of the 2011 26th IEEE/ACM International Conference on Automated Software Engineering (ASE '11). IEEE Computer Society, Washington, DC, USA, 283-292. DOI=http://dx.doi.org/10.1109/ASE.2011.6100064

### ii. Keywords
ii1: Discrete Time Markov Chain (DTMC) - 

ii2: Probabilistic Computational Tree Logic (PCTL) - 

ii3: Finite State Machine (FSM) - 

ii4: Dynamic System - 

### iii. A Few Notes
iii1: Motivation - This paper suggests a new means of creating self-adaptive software that can maintain compliance with a given (possibly changing) set of reliability requirements within a limited setting.

iii2: New Results - The self-adaptation is accomplished by using a feedback loop to control for the dynamic system.  This feedback loop is discussed theoretically and implemented in the form of a FSM which represents a DTMC model.

iii3: Mathematical Foundation - The paper discusses the general form of a dynamic system, then goes through a modification of it to account for real world behavior (e.g. approximation of values, external influence on the system).  It then gives a description of the mathematics behind setpoints in this context and discusses the appropriate error norms for the optimization problem.

iii4: Future Work - This paper only applies to one type of model (DTMC), to optimizing one type of requirement (reliability expressed in a certain way), etc.  Generalization of any/all of these is needed.


### iv. Weaknesses
iv1: Diction/grammar - On the whole the paper had good grammar and used words appropriately, but some portions had grammar/spelling errors which distracted from the text - particularly in section 5.  A proofreader could have prevented this.

iv2: Sets a very broad agenda in multiple areas - The purpose of the paper is to set an agenda for future work, so to some extent broad strokes are expected.  However, the paper loses a bit of focus as it addresses philosophy of science (empiricism vice experimentalism), and describes multiple distinct potential research areas without any discussion of how (or whether) research in each could interact.

iv3: Even an agenda paper needs to suggest a future direction - On the whole, the paper offers very little in the way of concrete suggestions, preferring to simply point out the problems.  The exception to this critique is the section on synthetic data.
