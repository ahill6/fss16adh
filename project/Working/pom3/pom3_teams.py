__author__ = 'joe krall'

from pom3_team import *
from random import randint, random
import math

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
        p3d.haste = int(X[10])
        p3d.price   = X[11]
    
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
        elif var == 'Signals':
            p3d.signals = val
        elif var == 'TTM':
            p3d.haste = val
        elif var == 'Price':
            p3d.price = val
        else:
            raise Exception('tried to set a value not in pom3 decisions')
        
class pom3_teams:
    def __init__(p3t, requirements, decisions):
        p3t.teams = []
        listflag = False
        if isinstance(decisions[0], float):
            p3t.decisions = [pom3_decisions(decisions)]
        else:
            p3t.decisions = [pom3_decisions(x.decisions) for x in decisions]
            listflag = True

        # Build Each Team
        total_size = 0
        tries = 0
        
        if listflag:
            for i in range(len(decisions)):
                p3t.teams.append(Team(p3t.decisions[i], i))
        else:
            p3t.teams.append(Team(p3t.decisions,0))

        # Assign Initial Tasks to Each Team---lots of overlap but not all overlap
        for team in p3t.teams:
            end = randint(1, max(3, math.ceil(.1*(len(requirements.tasks)-1))))
            for k in range(0, end):
                team.tasks.append(requirements.tasks[k])
        
        # Mark Initial Visibility of Tasks for Each Team
        for team in p3t.teams:
            team.markTasksVisible()

        # Apply Effect of Boehm-Turner Personnel Scales to Task Costs
        scales_alpha = [0.45, 0.50, 0.55, 0.60, 0.65]
        scales_beta  = [0.40, 0.30, 0.20, 0.10, 0.00]
        scales_gamma = [0.15, 0.20, 0.25, 0.30, 0.35]
        for team in p3t.teams:
            numAlphas = scales_alpha[p3t.decisions[team.name].size]*team.team_size
            numBetas = scales_beta[p3t.decisions[team.name].size]*team.team_size
            numGammas = scales_gamma[p3t.decisions[team.name].size]*team.team_size
            #print numAlphas, numBetas, numGammas
            team.alpha = numAlphas
            team.beta = numBetas
            team.gamma = numGammas
            team.power = team.alpha + 1.22*team.beta + 1.6*team.gamma

            for task in team.tasks:
                task.val.cost += task.val.cost * ((numAlphas + 1.22*numBetas + 1.6*numGammas)/100.0)

                # and apply effect of criticality while we're at it
                task.val.cost = task.val.cost * (team.decisions.criticality_modifier ** team.decisions.criticality) # cost' = cost * X^criticality

        #Print Out of Teams & Requirements
        """
        for i,team in enumerate(p3t.teams):
            print "___________________TEAM #" + str(i) + "______________________"
            for e,task in enumerate(team.tasks):
                print "> TASK #" + str(e) + ": " + str(task)
        """