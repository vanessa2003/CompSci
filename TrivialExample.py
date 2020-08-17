from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper
from panaxea.core.Environment import ObjectGrid2D
from enum import IntEnum
import time
import numpy as np
from statistics import mean
import random
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





class State(IntEnum):
    susceptible = 0
    infected = 1
    infectious = 2
    recovered = 3



class SimpleAgent(Agent):
    

    def __init__(self, name, initial_state=State.susceptible):
        super(SimpleAgent, self).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = initial_state
        self.infection_duration = 0
        self.recovery_duration = 5
        self.incubation_period = 0
        self.ptrans = 0.1
       
    
   

    def step_prologue(self, model):
        current_position = self.environment_positions["virus_env"]

        xlimit = model.environments["virus_env"].xsize - 1
        ylimit = model.environments["virus_env"].ysize - 1
        xstart = 0
        ystart = 0


        x_direct = random.choice((-1, 0, 1))
        y_direct = random.choice((-1, 0, 1))
        cand_x = x_direct + current_position[0]
        cand_y = y_direct + current_position[1]
        
        # While loop is wrong.
        # Test whether (cand_x, cand_y) is valid
        # If it is, then move there, otherwise wait until next epoch (do nothing)



        if cand_x <= xlimit and cand_x >= xstart:
            if cand_y <= ylimit and cand_y >= ystart:
                new_position = (cand_x, cand_y)
                self.move_agent("virus_env", new_position, model)
                
                
       
          
                
            
            
            

#        if current_position[0] == xlimit:
 #           new_position = (0,current_position[1] + random.randint(0,ysize) )
    #else:
     #       new_position = (current_position[0] + random.randint(0,xsize),current_position[1])

        # generate a candidate new postition
        #   1) At most 1 sqaure away
        #   2) Direction is random
               # x_direct = choice((-1, 0, 1))
               # y_direct = choice((-1, 0, 1))
               # cand_x = x_direct + curr_x
               # cand_y = y_direct + curr_y
        
        # Test if the candidate position is inside the grid
        # if it's inside, move there
        
        
        
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
            for someone in random.choices(list(a),k=random.randint(0,5)):
                if someone.state is State.susceptible:
                    if random.random() <= self.ptrans:
                        #print(random.random())
                        someone.state = State.infected
                        #someone.infection_duration = self.model.schedule.time
            
            self.infection_duration += 1
            # update length of infection
                        
          


    def step_epilogue(self, model):

        
        if self.state == State.infected:
            self.state = State.infectious
           
        if self.state is State.infectious:
            if self.infection_duration == self.recovery_duration:
                self.state = State.recovered
               
            
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
        
        population_stats['susceptible_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.susceptible])
        population_stats['infectious_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.infectious])
        population_stats['recovered_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.recovered])
        population_stats['day'] = model.current_epoch
        if  population_stats['infectious_pop'] == 0:
            model.exit = True
            population_stats['day'] = model.current_epoch
        print(population_stats)
        
        

        print("Helper prologue")
        
        
        
    
        

    def step_epilogue(self,model):
        population_stats['newly_infected'] = len([agent for agent in model.schedule.agents if agent.state == State.infected])
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


    
#for i in range(10):
 #   model.schedule.agents_to_schedule.add(SimpleAgent(i))
# i == 49
    
#for p in range(1,3):
#    model.schedule.agents_to_schedule.add(SimpleAgent(p+i, initial_state=State.infectious ))


def setup_model(num_agents, num_infectious, max_num_epochs=100):
    model = Model(max_num_epochs)
    xsize = ysize = 30
    ObjectGrid2D("virus_env", xsize, ysize, model)
    for i in range(num_agents):
        agent = SimpleAgent(i)
        model.schedule.agents_to_schedule.add(agent)
        agent.add_agent_to_grid("virus_env",(random.randint(0,xsize),random.randint(0,ysize)), model)
    for p in range(1,num_infectious+1):
        ill_agent = SimpleAgent(p+i, initial_state=State.infectious)
        model.schedule.agents_to_schedule.add(ill_agent)
        ill_agent.add_agent_to_grid("virus_env",(random.randint(0,xsize),random.randint(0,ysize)), model)
    return model







all_stats = list()
runs = 30
for r in range(runs):
    model = setup_model(50, 2) #users pass in how many susceptible agents they want and how many infectious agents they want
    #virus_env = model.environments["virus_env"]
    population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0, 'day':0}
    model.schedule.helpers.append(SimpleHelper())
    model.run()
    
    all_stats.append(population_stats)
    

#print(all_stats)

#max_infected = max(population_stats.keys(), key=(lambda k: population_stats['recovered_pop']))
#print("maximum infected population :",population_stats[max_infected])    

#def average(lst):
   # return sum(lst)/len(lst)



 
total_infected = [agent['recovered_pop'] for agent in all_stats]
#print(total_infected)
print("maximum number of people infected in a day is",max(total_infected))
print("minimum number of people infected in a day is",min(total_infected))
print("average number of people infected in a day is",mean(total_infected))

outbreak_length = [days['day'] for days in all_stats]
#print(outbreak_length)

print("longest outbreak duration is",max(outbreak_length),"days")
print("shortest outbreak duration is",min(outbreak_length),"days")
print("average outbreak duration is",mean(outbreak_length),"days")











#    model = Model(max_num_epochs)...
#    return model

#model = Model(100)

#for i in range(10):
 #   model.schedule.agents_to_schedule.add(SimpleAgent(i))
# i == 49

#for someone in random.choices(list(model.schedule.agents),k=2):
 #   someone.state = State.infectious

#for p in range(1,3):
 #   model.schedule.agents_to_schedule.add(SimpleAgent(p+i, initial_state=State.infectious ))

#model.schedule.agents_to_schedule.add(SimpleAgent(i+2, initial_state=State.infectious ))




   
    





#population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0} 

#model.run()

#all_stats = list()
#for r in range(10):
    # population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0} 
#     model = setup_model(50, 2)
#     model.run()
#     all_stats.append(population_stats)
# Average, min, max # infected over the outbreak
# Average, min, man length of outbreak
# Fixed # of epoch; run until no more infectious agents
# Multiples runs

# Total infected: number of agents recovered
# Peak infected: max number of newly infected agents each epoch [1:1, 2:5, 3:10, 4:5], max number of total cases = max.infectious_pop and max number of new cases = max.newly_infected
# Average length of infection: so how many epochs did it take for infectious_population = 0
# R0 ie how many people I'm likely to infect: for every infectious agents how many agents become newly infected

#State for a *set* runs
