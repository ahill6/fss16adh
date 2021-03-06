#Product Development and Signaling

##Overview
###Background
At present, all analysis in many economic fields is limited to equations which permit closed-form solution and analysis.  This results in necessary simplification of all modeling assumptions and independent variables, both of which can reduce correlation with real-world behavior.  By depending on automated methods to “exercise” the model rather than manual analysis, a significantly more complex model can be used - one which includes real-world behavior that is neglected in current techniques used in the field.

One example is signaling behavior during product development.  Companies may choose to publically announce that they are developing a new product if they believe such behavior will result in a competitor not entering the market (e.g. the competitor’s development is behind and the announcement causes the competitor to believe it is in their interest to cut losses), thus reducing competition.  Likewise, the company could refrain from announcing a timeline in order to hide the fact that their own product is behind schedule.  However, this is an imperfect information situation, as competitors do not know the true state of a company’s development and an announcement could be merely for show.  A May 2016 model of this behavior includes only 2 companies and limited potential behaviors due to the need to manually analyze differentiable functions to describe optimal behavior.

In addition, chance events can impact outcomes even after signalling (e.g. failure at the manufacturing plant, social event resulting in increased/decreased demand for their product, improbable breakthrough of competitor), thus adding a random perturbation to the economic situation in the case when a company’s initial beliefs were accurate.  These perturbative effects are not included in such models.  

###Objective
The goal of this project is to develop a model which describes product development behavior with signaling in a real-world environment (without neglecting real-world effects).  A variety of optimization algorithms would then be run to find Pareto-optimal behavior in product development.

To support the development of this model, existing literature in competitive models, product development and product lines, and signaling behaviors in economics will be consulted.  Interpretation of the results and domain knowledge will be supplied by Dr. William Caylor at SMU.  He specializes in economic analysis of product development and signaling behaviors, and has agreed to collaborate on this project.

##Project Phases

###Iteration 1

Single company which desires to optimize behavior over possible choices, initial setup of model, experimental rig, and validation of design assumptions.  Model will be exercised via random sampling and random walk to determine range of potential outputs, domain knowledge will be added as needed to make an interesting but not overly complex model (in first iteration).

####Sample Model at End of Iteration 1:
#####Decisions
+ Product features
+ Product materials/process quality 
+ Haste (whether to try to speed production)
+ When to announce new product
+ How much information to give in announcement

#####Objectives
+ Profit (calculated sales price - cost calculated from features)
+ Feature reuse
+ Long-term brand loyalty/reputation

#####Non-Decision Inputs
+ Current brand reputation
+ Resources available (limit to haste value)
+ Random inputs for various events (e.g. unexpected failure at manufacturing plant, change in market conditions, failure of haste attempt to accelerate product deployment)

It is expected that optimal behavior for this iteration will not include behaviors designed to react to competitors (e.g. product announcement) since such behavior will have no effect without a competitor.

**N.B.** After each iteration, data will be shared with the subject matter expert for validation/interpretation and suggestions for model improvements.

###Iteration 2
2 companies, each with a true time-to-product and a belief about the other company’s time-to-product.  This belief will be calculated based on a base factor and other company’s announcement/lack, information given during the announcement, and a small random factor.

In addition, profitability will now include a factor of which product went to market first, as well as a random chance that the product is defective which depends on build quality and haste (consider the Galaxy Note 7 fires due to haste to reach market before the iPhone 7).  This also has the potential to affect long-term brand loyalty/reputation.

**N.B.** For comparison with the current state of the field, consider that analysis of behavior which includes market signals in imperfect information is publishable at this level (successful iteration 2) due to the intensity of the (manual) analysis required

###Iteration 3

Expand competition to n initially identical companies.  In iterations 3 and 4 n will be varied experimentally.  Potentially add regulatory action (i.e. if companies act outside certain bounds, they risk regulatory action/audits), the potential for multiple announcements, and/or an explicit advertising factor.  Note that for multi-party competition, economic theory suggests the presence of relatively stable equilibria in company behavior, so optimizers should be able to find interacting Pareto fronts.

###Iteration 4

N companies, each with different starting values and caps (e.g. amount of resources available for haste, initial brand reputation).  With improvements in the model from domain knowledge in iterations 1-4, successfully reaching this iteration would represent a significant improvement in current state-of-the-art.
###Iteration 5+

Depending on the results of Iterations 1-4 and time remaining, a potential iteration 5 and beyond would begin to attempt to model multiple-move situations, where the system is repeated with the starting point dependent on each company’s previous ending values.  A meta-model with a more abstract fitness function including discounted potential future income (likely using standard exponential discounting assumptions) would be used to score overall behavior in the multiple-move space.  Together with model improvements from domain knowledge in iterations 1-4, a successful iteration 5+ would result in the most complete existing model of industry behavior.


##Variables (Iterations 1-4)

Caveat - All of the following are likely to be modified as domain knowledge increases

###Decisions
+ Product features
+ Product materials/process quality 
+ Haste (whether to try to speed production)
+ When to announce new product
+ How much information to give in announcement
+ Credulity (input for belief of other companies’ time-to-market) [starting iteration 2]

###Objectives
+ Profit (maximize)
..+ Inputs
....+ Cost: product features, materials, haste, random inputs
....+ Sale Price: product features, materials, competition (based on time-to-market), current brand reputation, known competitor product, random inputs
+ Feature reuse (maximize)
..+ Inputs: Product features, haste
+ Long-term brand loyalty/reputation (maximize)
..+ Inputs: current reputation, product features, materials, haste, random inputs
..+ Updating function will likely be related to Bayesian updating
+ Coverage of competitor’s features (maximize)
..+ Inputs: product features, materials, haste, random inputs, known competitor product
+ Decision stability (maximize) [potential]
..+ This would attempt to take the potential of random events into account
+ Government interference (minimize) [potential]

###Non-Decision Inputs
+ Current brand reputation
+ Known competitor product (represents knowledge of competition as a proxy for calculating percentage of market that will purchase company’s new product as a function of relative features)
+ Resources available (limit to haste value)
+ Random inputs for various events (e.g. unexpected failure at manufacturing plant, change in market conditions, failure of haste attempt to accelerate product deployment)
+ Actual time-to-market (calculated from decisions and an initial setting, an input to profit objective)

###Potential additions for dynamic model could include items such as 
+ Adaptability (prior likelihood of a company to change course due to events)
+ Varying levels of risk-aversion 
+ Ability for a company to be in debt for a given period of time before becoming profitable (real-world situation)
