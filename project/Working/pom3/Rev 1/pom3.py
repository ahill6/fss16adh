__author__ = 'joe krall'

from pom3_teams import *
from pom3_requirements import *
from copy import deepcopy
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
        p3d.signals = int(X[9])
        p3d.price   = X[10]
        
    def setter(p3d, var, val):
        if var == 'Culture':
            p3d.culture = val
        elif var == 'Criticality':
            p3d.criticality = val
        elif var == 'Criticality Modifier':
            p3d.criticality_modifier = val
        elif var == 'Initial Known':
            p3d.initial_known = val
        elif var == 'Inter-Dependency':
            p3d.interdependency = val
        elif var == 'Dynamism':
            p3d.dynamism = val
        elif var == 'Size':
            p3d.size = val
        elif var == 'Plan':
            p3d.plan = val
        elif var == 'Team Size':
            p3d.team_size = val
        else:
            raise Exception('tried to set a value not in pom3 decisions')
            
class pom3:
    def initialization(p3, decs, interdep):
        # Generate Requirements 
        p3.POM3_REQUIREMENTS_0 = pom3_requirements(decs, interdep)
        p3.POM3_REQUIREMENTS = deepcopy(p3.POM3_REQUIREMENTS_0)
        p3.roundsmin = random.randint(2,6)
        p3.roundsmax = random.randint(p3.roundsmin, max(p3.roundsmin+ 4, 2*p3.roundsmin ))
        p3.numberOfShuffles = random.randint(p3.roundsmin, p3.roundsmax)
        return p3.POM3_REQUIREMENTS_0
    
    def reset(p3):
        p3.POM3_REQUIREMENTS = deepcopy(p3.POM3_REQUIREMENTS_0)
        
    def reset_teams(p3):
        p3.POM3_TEAMS = p3.POM3_TEAMS_0
        
    def establish_teams(p3, decs):
        p3.POM3_TEAMS = pom3_teams(p3.POM3_REQUIREMENTS, decs)
        
    def set_requirements(p3, reqs):
        p3.POM3_REQUIREMENTS_0 = deepcopy(reqs)
    
    def change_team_decision(p3, team_name, decision_name, new_decision):
        for p in p3.POM3_TEAMS.teams:
            if p.name == team_name:
                p.decisions.setter(decision_name, new_decision)

    def simulate(p3):
    
        numberOfShuffles = random.randint(2,6)# need to increase this number to get sufficient time-steps
        
        for shufflingIteration in range(numberOfShuffles):
            #insert part about signals changing values
            #if shufflingIteration in signals:
                #print("1")
            # if shufflingIteration in signals:
            #    signal()
            for team in p3.POM3_TEAMS.teams:
                team.updateBudget(numberOfShuffles)
                team.collectAvailableTasks(p3.POM3_REQUIREMENTS)
                team.applySortingStrategy()
                team.executeAvailableTasks()
                team.discoverNewTasks()
                #team.updateTasks()

        results = []
        
        # 4) Objective Scoring
        for team in p3.POM3_TEAMS.teams:
            cost_sum,value_sum,god_cost_sum,god_value_sum,completion_sum,available_sum,total_tasks = 0.0, 0.0, 0.0, 0.0, 0,0,0
            cost, score, completion, idle, value = 0.0, 0.0, 0.0, 0.0, 0.0

            features = []
            
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
                    features.append(task)

            if cost_sum == 0: our_frontier = 0.0
            else: our_frontier =     value_sum /     cost_sum
    
            if god_cost_sum == 0: god_frontier = 0.0
            else: god_frontier = god_value_sum / god_cost_sum
    
            if god_frontier == 0.0: score = 0.0
            else: score       =  our_frontier / god_frontier
    
            if completion_sum == 0: cost = 0
            else: cost = cost_sum/completion_sum 
            
            if completion_sum == 0: value = 0
            else: value = value_sum/completion_sum
            
            if available_sum == 0: idle = 0
            else: idle = 1 - completion_sum/float(available_sum)
    
            if total_tasks == 0: completion = 0
            else: completion = completion_sum/float(total_tasks)
            
            #results.append([cost, value, score, completion, idle, features])
            results.append([cost, value, score, completion, idle])

        return results
    
    def quit_check(p3, steps):
        # copy current state
        tmpteams = deepcopy(p3.POM3_TEAMS).teams
        tmprequirements = deepcopy(p3.POM3_REQUIREMENTS)
        
        #ON THE COPY, run through the rest of the sim
        tmpteams = p3.step_sim(steps, teams=tmpteams, reqs=tmprequirements)
        
        # run stats and check if cost/value (and/or whatever else) is within acceptable parameters
        score = p3.calculate_results(tmpteams)
        print(score[-1][1], score[-1][0])
        # return True if you should quit, else False
        return score[-1][1]*1.25 > score[-1][0]
        
    def step_sim(p3, steps, teams=None, reqs=None, shuffles=None):
        flag = False

        if reqs is None:
            if teams is None:
                teams = p3.POM3_TEAMS.teams
                reqs = p3.POM3_REQUIREMENTS
                flag = True
        if shuffles is None:
            shuffles = p3.numberOfShuffles
                
        for k in range(steps):
            for team in teams:
                team.updateBudget(shuffles)
                team.collectAvailableTasks(reqs)
                team.applySortingStrategy()
                team.executeAvailableTasks()
                team.discoverNewTasks()
                team.updateTasks()
        if flag:
            return teams
        
    def calculate_results(p3, teams=None):
        if teams is None:
            teams = p3.POM3_TEAMS.teams
        results = []
        
        # 4) Objective Scoring
        god_cost_sum, god_value_sum = 0.0, 0.0
        for team in teams:
            cost_sum,value_sum,completion_sum,available_sum,total_tasks = 0.0, 0.0, 0,0,0
            cost, score, completion, idle, value = 0.0, 0.0, 0.0, 0.0, 0.0

            features = []
            
            cost_sum += team.cost_total
            value_sum += team.value_total
            available_sum += team.numAvailableTasks
            completion_sum += team.numCompletedTasks
            for task in team.tasks:
                if task.val.visible:
                    total_tasks += 1
                if task.val.done == True:
                    god_cost_sum += task.val.cost
                    god_value_sum += task.val.value
                    features.append(task)
            
            if cost_sum == 0: our_frontier = 0.0
            else: our_frontier =     value_sum /     cost_sum
    
            if god_cost_sum == 0: god_frontier = 0.0
            else: god_frontier = god_value_sum / god_cost_sum
    
            if god_frontier == 0.0: score = 0.0
            else: score       =  our_frontier / god_frontier
    
            if completion_sum == 0: cost = 0
            else: cost = cost_sum/completion_sum 
            
            if completion_sum == 0: value = 0
            else: value = value_sum/completion_sum
            
            if available_sum == 0: idle = 0
            else: idle = 1 - completion_sum/float(available_sum)
    
            if total_tasks == 0: completion = 0
            else: completion = completion_sum/float(total_tasks)
            
            #results.append([cost, value, score, completion, idle, features])
            results.append([cost, value, score, completion, idle])

        return results