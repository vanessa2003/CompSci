from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper
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



class State():
    susceptible = 0
    infected = 1
    recovered = 0


class SimpleAgent(Agent):
    

    def __init__(self, name):
        super(SimpleAgent, self,).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = State.susceptible
        self.infection_duration = 0

    def step_prologue(self, model):
        print("This is the prologue, so I will say my name: {0}".format(
            self.name))
         

        """
    def step_main(self, model):
        people = model.schedule.agents 
        if random.random() >= 0.5:
            for other in people:
                if self.state is State.infected and other.state is State.susceptible:
                    other.state = State.infected
                    other.infection_duration = self.model.schedule.time
                    other.recovery_duration = model.the_recovery_time()
                    """

          
    def step_epilogue(self, model):
        print("This is the epilogue, and {0} says the counter is set to"
              " {1}".format(self.name, model.properties["counter"]))
        if self.state == State.infected:
             #t = model.schedule.time-self.infection_duration
             print("there are {0} agents infected".format(model.properties["infected"]))


class SimpleHelper(Helper):

    def step_prologue(self, model):
        model.properties["counter"] += 1
        for i in model.schedule.agents:
            infected = np.random.choice([0,1], p=[0.9,0.1])
            if infected == 1:
                self.state = State.infected
                model.properties["infected"] += 1
       
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
model.properties["population"] = model.schedule.agents
model.schedule.agents_to_schedule.add(SimpleAgent("Adam"))
model.schedule.agents_to_schedule.add(SimpleAgent("Beth"))
model.schedule.agents_to_schedule.add(SimpleAgent("james"))
model.schedule.agents_to_schedule.add(SimpleAgent("sarah"))
model.schedule.helpers.append(SimpleHelper())

model.run()

