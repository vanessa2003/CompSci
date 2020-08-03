from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper

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
    

    def __init__(self, name,):
        super(SimpleAgent, self,).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = State.susceptible
        self.infection_duration = 0

    def step_prologue(self, model):
         print("This is the prologue, so I will say my name: {0}".format(
            self.name))
         if self.state == State.infected:
             t = self.model.schedule.time-self.infection_duration
             if t >= self.recovery_duration:
                 self.state = State.recovered
       

    def step_main(self, model):
        people = self.model.N
        if self.random.random() >= 0.5:
            for other in people:
                if self.state is State.infected and other.state is State.susceptible:
                    other.state = State.infected
                    other.infection_duration = self.model.schedule.time
                    other.recovery_duration = model.the_recovery_time()


    def step_epilogue(self, model):
        print("This is the epilogue, and {0} says the counter is set to"
              " {1}".format(self.name, model.properties["counter"]))


class SimpleHelper(Helper):

    def step_prologue(self, model):
        model.properties["counter"] += 1


model = Model(10)
model.properties["counter"] = 0

model.schedule.agents_to_schedule.add(SimpleAgent("Adam"))
model.schedule.agents_to_schedule.add(SimpleAgent("Beth"))
model.schedule.helpers.append(SimpleHelper())

model.run()
