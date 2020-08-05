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
    sick = 2
    recovered = 3

class population():
    tsick_pop = 0
    newly_infected = 0
    susceptible_pop = 0
    recovered_pop = 0
    

class SimpleAgent(Agent):
    

    def __init__(self, name):
        super(SimpleAgent, self).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = State.susceptible
        self.infection_duration = 0

    def step_prologue(self, model):
        print("This is the prologue, so I will say my name: {0}".format(
            self.name))
        

    def step_main(self, model):
        a = (tuple(model.schedule.agents))
        for person in a:
            infected = np.random.choice([0,1], p=[0.9,0.1])
            print(infected)
            if infected == 1:
                self.state = State.infected
                population.newly_infected +=1
        for someone in a:
            if self.state is State.infected and someone.state is State.susceptible:
                if random.random() >= 0.5:
                    #print(random.random())
                    someone.state = State.infected
                    #someone.infection_duration = self.model.schedule.time
          


    def step_epilogue(self, model):
        for i in range (model.epochs):
            if self.state == State.infected:
                self.state == State.sick
                population.tsick_pop = population.newly_infected
                print("The total number of infected people in this epoch is,",population.tsick_pop)


             #t = model.schedule.time-self.infection_duration
             #print("there are {0} agents infected".format(model.properties["infected"]))

class SimpleHelper(Helper):

    def step_prologue(self, model):
        print("Helper prologue")
        
    

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
model.properties["counter"] = 0
model.properties["infected"] = 0
model.properties["susceptible"] = 0
model.properties["recovered"] = 0
#model.properties["population"] = model.schedule.agents
#model.schedule.agents_to_schedule.add(SimpleAgent("Adam"))
model.schedule.agents_to_schedule.add(SimpleAgent("Beth"))
model.schedule.agents_to_schedule.add(SimpleAgent("james"))
model.schedule.agents_to_schedule.add(SimpleAgent("sarah"))
model.schedule.helpers.append(SimpleHelper())

model.run()

