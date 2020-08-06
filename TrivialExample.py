from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper
from enum import IntEnum
import time
import numpy as np
"""
A very simple model which illustrates the basis of creating a model.

An instance of the model is created specifying it will run for 10 epochs.

A class is defined for a SimpleAgent which, in the prologue, outputs its
name. In the epilogue, it outputs the model property counter.

A helper is created which once at the end of each epoch increases the counter
by 1.

Finally, two SimpleAgents and an instance of the helper are added to the
schedule and the model is run.
"""
import random




class State(IntEnum):
    susceptible = 0
    infected = 1
    infectious = 2
    recovered = 3

# BP: Consider using a dictionary instead?
# [1,2,3][0] => 1
# {1:'one', 2:'two', 3:'three'}[1] => 'one'
# {2:'two', 1:'one', 3:'three'}
# {'one':1, 'two':2, 'three':3}['one'] => 1
# population_stats = {'tsick_pop':0}
# population_stats['tsick_pop'] += 1

population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0} 
    

class SimpleAgent(Agent):
    

    def __init__(self, name):
        super(SimpleAgent, self).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = State.infectious
        self.infection_duration = 0
        self.recovery_duration = 5


    def step_prologue(self, model):
        print("This is the prologue, so I will say my name: {0}".format(
            self.name))
        
# Transmission model
# Propability of being infected is proportional to total number of infectous people.
# "susceptible" perspective
#    if I am suceptible, evaluate my chance of being infected and then check whether I am infected
# "infectious" perspective
#    if I am infectous, evaluate my chance of *infecting* every suceptible
    def step_main(self, model):
        a = model.schedule.agents
        # BP: a = model.schedule.agents
        if self.state is State.infectious:
            for someone in a:
                if someone.state is State.susceptible:
                    if random.random() >= 0.5:
                        #print(random.random())
                        someone.state = State.infected
                        #someone.infection_duration = self.model.schedule.time
            self.infection_duration += 1
            # update length of infection
          


    def step_epilogue(self, model):

        if self.state is State.infected:
            population_stats['newly_infected'] += 1
            population_stats['susceptible_pop'] -= 1

        if random.random() >= 0.9 and self.state is State.infected:
            self.state = State.infectious
            population_stats['infectious_pop'] +=1
                

        if self.infection_duration == self.recovery_duration:
            if self.state is State.infectious:
                self.state = State.recovered
                population_stats['recovered_pop'] += 1
                population_stats['infectious_pop'] -= 1
        
            
        # Update state
        # infected => infectious (sick)
        # infectious => recovered
        
        # Update statistics
        # 
        # BP: Loop is wrong
          
             #if self.state == State.infected:
              #  newly_infect += 1
               # tsick_pop += 1
                #self.state == State.sick
                #population.tsick_pop += population.newly_infected
                #print("The total number of infected people in this epoch is,",population.tsick_pop)
            #if selfstate == State.sick and length_of_infect == recoverytime:
                #update state
             #   population.tsick_pop -= 1

             #t = model.schedule.time-self.infection_duration
             #print("there are {0} agents infected".format(model.properties["infected"]))
     
# Stats at end of epoch:
#   How many newly infected
#   Current total sick == number currently infectious
#   Cumulative total == current infectious + recovered == recovered
                
class SimpleHelper(Helper):

    def step_prologue(self, model):
        population_stats['susceptible_pop'] = len(model.schedule.agents)
        population_stats['newly_infected'] = 0
        print(population_stats)
        print("Helper prologue")
        
        # zero out the newly_infected
        
    

    def step_epilogue(self,model):
        print("Helper epilogue")
        
        #print(State.infected)
"""
class simplemodel(model):

    def _(self, model):
        for i in range (model.schedule.agents):
            infected = np.random.choice([0,1], p=[0.9,0.1])
            if infected == 1:
                self.state = State.infected
       
   """
 

model = Model(10)
#model.properties["counter"] = 0
#model.properties["infected"] = 0
#model.properties["susceptible"] = 0
#model.properties["recovered"] = 0
#model.properties["population"] = model.schedule.agents
#model.schedule.agents_to_schedule.add(SimpleAgent("Adam"))
model.schedule.agents_to_schedule.add(SimpleAgent("Beth"))
model.schedule.agents_to_schedule.add(SimpleAgent("james"))
model.schedule.agents_to_schedule.add(SimpleAgent("sarah"))
model.schedule.helpers.append(SimpleHelper())

model.run()

