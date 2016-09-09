Antonio Filieri, Carlo Ghezzi, Alberto Leva, and Martina Maggio. 2011. Self-adaptive software meets control theory: A preliminary approach supporting reliability requirements. In Proceedings of the 2011 26th IEEE/ACM International Conference on Automated Software Engineering (ASE '11). IEEE Computer Society, Washington, DC, USA, 283-292. DOI=http://dx.doi.org/10.1109/ASE.2011.6100064

### ii. Keywords
ii1: Discrete Time Markov Chain (DTMC) - A Markov Chain is one way of modeling random behavior between states.  Here over discretized time (i.e. events occur at distinct points in time/at given intervals).  

ii2: Probabilistic Computational Tree Logic (PCTL) - A tree-based logic model that allows for probabilistic transition between states.  Often used for formal verification and similar problems.

ii3: Finite State Machine (FSM) - An abstract computational machine which has a set of states and a transition function to move from one state to another.  In the case of this paper, the FSM is non-deterministic.

ii4: Dynamic System - A system with sensitive dependence on an input (most often time).  Generally this means that a slight perturbation can result in radically different system behavior.

### iii. A Few Notes
iii1: Motivation - This paper suggests a new means of creating self-adaptive software that can maintain compliance with a (possibly changing) set of reliability requirements within a limited setting.

iii2: New Results - Self-adaptation is accomplished by using a feedback loop to control for the dynamic system.  This feedback loop is discussed theoretically and implemented in the form of a FSM which represents a DTMC model.

iii3: Mathematical Foundation - The paper discusses the general form of a dynamic system, modification for real world behavior, and analysis of fixed points.  The mathematical background is helpful for establishing the authors’ approach.

iii4: Future Work - This paper only applies to one type of model (DTMC), to optimizing one type of requirement (reliability expressed in a certain way), etc.  Generalization of any/all of these is needed.


### iv. Weaknesses
iv1: Very Limited Results - While expected of most research papers, the results presented are extremely limited, dealing with a special case of a subset of a special case.

iv2: "Pure Delay" Model - At the end of section IV, the authors mention that the model used is a "pure delay" model - meaning there is an assumption that "any action at the beginning of a step has exhausted its effect at the end of that step".  This assumption must be validated.

iv3: Style - In several cases the authors make simple grammar mistakes that slightly distract from the paper.  Also, at the end of section IV the authors do not follow best practice of writing out acronyms at least once before using them (PCTL).

### v. Connection to Other Papers
The base paper (Harman et al. 2012) tries to give a general agenda for adaptive software based on search-based software engineering (SBSE).  This paper is an attempt to create adaptive software in a non-SBSE way.  It served as a guide for one direction in current research, while also showing the need for an SBSE approach.
