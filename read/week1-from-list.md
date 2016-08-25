##Antonio Filieri, Carlo Ghezzi, Alberto Leva, and Martina Maggio. 2011. Self-adaptive software meets control theory: A preliminary approach supporting reliability requirements. In Proceedings of the 2011 26th IEEE/ACM International Conference on Automated Software Engineering (ASE '11). IEEE Computer Society, Washington, DC, USA, 283-292. DOI=http://dx.doi.org/10.1109/ASE.2011.6100064

### ii. Keywords
ii1: Discrete Time Markov Chain (DTMC) - A Markov Chain is a particular way of modeling random behavior between different states.  One which operates over discrete time means precisely that the time variable is discrete (i.e. events occur at distinct points in time/at given intervals).  This is sometimes contrasted with a "Markov Process" or Continuous Time Markov Chain.

ii2: Probabilistic Computational Tree Logic (PCTL) - A tree-based logic model that allows for probabilistic transition between states.  Often used for formal verification and similar problems.

ii3: Finite State Machine (FSM) - An abstraction of a computational machine which has a set of states and a transition function to move from one state to another.  In the case of this paper, the addition of randomness (DTMC) makes the machine non-deterministic.

ii4: Dynamic System - A system with sensitive dependence on an input (most often time).  Generally this means that a slight pertubation at a given point can result in radically different behavior.

### iii. A Few Notes
iii1: Motivation - This paper suggests a new means of creating self-adaptive software that can maintain compliance with a given (possibly changing) set of reliability requirements within a limited setting.

iii2: New Results - The self-adaptation is accomplished by using a feedback loop to control for the dynamic system.  This feedback loop is discussed theoretically and implemented in the form of a FSM which represents a DTMC model.

iii3: Mathematical Foundation - The paper discusses the general form of a dynamic system, then goes through a modification of it to account for real world behavior (e.g. approximation of values, external influence on the system).  It then gives a description of the mathematics behind setpoints in this context and discusses the appropriate error norms for the optimization problem.

iii4: Future Work - This paper only applies to one type of model (DTMC), to optimizing one type of requirement (reliability expressed in a certain way), etc.  Generalization of any/all of these is needed.


### iv. Weaknesses
iv1: 

iv2: 

iv3: 
