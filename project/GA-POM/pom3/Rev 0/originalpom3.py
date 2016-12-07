__author__ = 'joe krall'

from pom3_teams import *
from originalpom3_requirements import *
import random

class pom3_decisions:
    def __init__(p3d, X):
        p3d.culture = X[0]
        p3d.criticality = X[1]
        p3d.criticality_modifier = X[2]
        p3d.initial_known = X[3]
        p3d.interdependency = X[4]
        p3d.dynamism = X[5]
        p3d.size = int(X[6])
        p3d.plan = int(X[7])
        p3d.team_size = X[8]

class pom3:
    def set_teams(p3, num_teams):
        p3.num_teams = num_teams
        
    def simulate(p3, inputs):

        # # # # # # # # # # #
        # 0) Initialization #
        # # # # # # # # # # #

        POM3_DECISIONS = pom3_decisions(inputs)
        numberOfShuffles = random.randint(2,6)

        # # # # # # # # # # # # # # #
        # 1) Generate Requirements  #
        # # # # # # # # # # # # # # #

        POM3_REQUIREMENTS = pom3_requirements(POM3_DECISIONS)

        # # # # # # # # # # #
        # 2) Generate Teams #
        # # # # # # # # # # #

        POM3_TEAMS = pom3_teams(POM3_REQUIREMENTS, POM3_DECISIONS, p3.num_teams)

        # # # # # # # #
        # 3) Shuffle  #
        # # # # # # # #


        for shufflingIteration in range(numberOfShuffles):

            for team in POM3_TEAMS.teams:
                team.updateBudget(numberOfShuffles)
                team.collectAvailableTasks(POM3_REQUIREMENTS)
                team.applySortingStrategy()
                team.executeAvailableTasks()
                team.discoverNewTasks()
                team.updateTasks()

        # # # # # # # # # # # # #
        # 4) Objective Scoring  #
        # # # # # # # # # # # # #

        cost = {}
        score = {}
        completion = {}
        idle = {}
        
        for team in POM3_TEAMS.teams:
            cost_sum,value_sum,god_cost_sum,god_value_sum,completion_sum,available_sum,total_tasks = 0.0, 0.0, 0.0, 0.0, 0,0,0
            
            cost_sum += team.cost_total
            value_sum += team.value_total
            available_sum += team.numAvailableTasks
            completion_sum += team.numCompletedTasks
            for task in team.tasks:
                if task.val.visible:
                    total_tasks += 1

            for task in team.tasks:
                if task.val.done == True:
                    god_cost_sum += task.val.cost
                    god_value_sum += task.val.value

            if cost_sum == 0: our_frontier = 0.0
            else: our_frontier =     value_sum /     cost_sum
    
            if god_cost_sum == 0: god_frontier = 0.0
            else: god_frontier = god_value_sum / god_cost_sum
    
            if god_frontier == 0.0: score[team.name] = 0.0
            else: score[team.name]        =  our_frontier / god_frontier
    
            if completion_sum == 0: cost[team.name] = 0
            else: cost[team.name] = cost_sum/completion_sum
    
            if available_sum == 0: idle[team.name] = 0
            else: idle[team.name] = 1 - completion_sum/float(available_sum)
    
            if total_tasks == 0: completion[team.name] = 0
            else: completion[team.name] = completion_sum/float(total_tasks)



        return [cost, score, completion, idle]