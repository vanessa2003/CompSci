from panaxea.core.Model import Model                               
from panaxea.core.Steppables import Agent, Helper
from panaxea.core.Environment import ObjectGrid2D
from enum import IntEnum
import time
import numpy as np
from statistics import mean
import random
import json

"""
This is my Agent based model and here are some notes:

epoch: a day in each outbreak, epoch 0 = day 1

the program executes in this order for each epoch:
Counter prologue
ExposedAgent prologue
Counter Main (there isnt a main counter in this program)
ExposedAgent Main
Counter Epilogue
ExposedAgent Epilogue







"""






infectious_pop = []
all_peak_infectious = []    #These are the global variables set for use anywhere in the program
time_taken = []
INFECTION_LIMIT = 10
susceptible_pop = []
avg_susceptible = []
avg_infecteds = []
recovered_pop = []
avg_recovered = []
class State(IntEnum):   #These are the different states an agent can be in and also allows for agents to change from one state to another
    susceptible = 0
    infected = 1
    infectious = 2
    recovered = 3


  

class Person(Agent):   
    '''This class holds all the different behaviours of an agent from how they move on a 
       grid to how they infect one another, this class also inherits methods from the Agent 
       class in the steppables file'''

    

    def __init__(self, name, position, initial_state=State.susceptible):
        super(Person, self).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = initial_state
        self.infection_duration = 0                    #These are the different attributes of an agent
        self.recovery_duration = 5
        self.incubation_period = 0
        self.ptrans = 0.1
        self.position = position
        self.r_rate = 0
       
    
   

    def step_prologue(self, model):
       
        
        xlimit,ylimit = env_limit(model.environments["virus_env"])
        xstart = 0
        ystart = 0


        x_direct = random.choice((-1, 0, 1))
        y_direct = random.choice((-1, 0, 1))
                                               #This shows how the agents move in a spatial model, conditions have been set to stop the agents leaving the grid.
                                               #In general the agents are only allowed to move 1 up, down, left or right depending on what the random function decides
                                               #Or if 0 is chosen then they dont move in that axis
        selfx = self.position[0]
        selfy = self.position[1]


        if selfx <= xstart:
            selfx == xstart

        if selfx >= xlimit:
            selfx == xlimit

        if selfy <= ystart:
            selfy == ystart

        if selfy >= ylimit:
            selfy == ylimit


        selfx += x_direct
        selfy += y_direct



        self.position = (round(selfx), round(selfy))
        self.move_agent("virus_env", self.position, model)





      
                
       
          
    def potential_targets(self, spatial_mode):
        potential_targets = list()
        agents = model.schedule.agents                                                      #The potential_targets function determines how agents can infect one another whether thats in a spatial model or in random model 
        if spatial_mode:
            if self.state is State.infectious:
                neighbourhood = model.environments["virus_env"].get_moore_neighbourhood(self.position)     #The neighbourhood function allows for infectious agent to only infect someone thats near them 
                neighbourhood.append(self.position)                                                        #It allows for infectious agents to infect other agents in the 8 cells that surround them                                          
                for a in agents:
                    pos_of_a = a.position
                    if pos_of_a in neighbourhood and a.state is State.susceptible:
                        potential_targets.append(a)
                self.infection_duration += 1
        else:
            if self.state is State.infectious:
                for someone in random.choices(list(agents),k=random.randint(0,INFECTION_LIMIT)):
                    potential_targets.append(someone)
                
                self.infection_duration += 1
         
        return (potential_targets)

                                                                                                       #In a random model the user can choose the maximum number of agents an infectious agent can infect, this is done by changing the global parameter infectious_limit.
                                                                                                       #the agents in a neigbourhood or those randomly selected are then added to a list.    

    def step_main(self, model):
        for someone in self.potential_targets(model.properties['spatial_transmission']):
            if someone.state is State.susceptible:
                if random.random() <= self.ptrans:
                    someone.state = State.infected
                    self.r_rate += 1
                

                    
                                                                                                        #Here the agents in the potential target list have a chance off getting infected the chance of them getting infected can be changed if the value
                                                                                                        #in the ptrans attribute of the agent is changed so currently the ptrans value is at 0.1 so agents have a 10% chance of infection.

    def step_epilogue(self, model):
        if self.state == State.infected:
            self.state = State.infectious                                       #Here is where the agents states are changed and since this is the last step of each epoch it comes to effect at the beginning of the next epoch
           
        if self.state is State.infectious:
            if self.infection_duration == self.recovery_duration:
                self.state = State.recovered      
                
class Counter(Helper):

    def step_prologue(self, model):                             
        population_stats['susceptible_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.susceptible])
        susceptible_pop.append(population_stats['susceptible_pop'])                                                                                                         #for every agent in a particular state they are then added to a count
        population_stats['infectious_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.infectious])      
        infectious_pop.append(population_stats['infectious_pop'])
        population_stats['recovered_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.recovered])                   #peak infectious population and the number of days it took to reach peak infectious population is calculated here
        recovered_pop.append(population_stats['recovered_pop'])
        population_stats['day'] = model.current_epoch
        if  population_stats['infectious_pop'] == 0:
            avg_susceptible.append(mean(susceptible_pop))
            avg_infecteds.append(mean(infectious_pop))
            avg_recovered.append(mean(recovered_pop))
            all_peak_infectious.append(max(infectious_pop))
            time_taken.append(infectious_pop.index(max(infectious_pop))+1)
            model.exit = True
        print(population_stats)

    def step_epilogue(self,model):
        population_stats['newly_infected'] = len([agent for agent in model.schedule.agents if agent.state == State.infected])

def env_limit(env):
    xlimit = env.xsize - 1
    ylimit = env.ysize - 1
    return (xlimit,ylimit)          #sets the actual environment limit so an environment with size of 30x30 actually only goes from 0 to 29.

def setup_model(num_agents, num_infectious, spatial_mode=True, max_num_epochs=1000):
    model = Model(max_num_epochs)
    xsize = ysize = 10                                                                     #The actual environment for the agents are set here, the agents are also placed on the grid at random positions
    ObjectGrid2D("virus_env", xsize, ysize, model)
    xlimit,ylimit = env_limit(model.environments["virus_env"])                              #spatial_mode can be set to true or false depending on what model you want to run if it set to false it runs the random model and when set to true viceversa.
    model.properties['spatial_transmission'] = spatial_mode
    for i in range(num_agents):
        agent_position = (random.randint(0,xlimit),random.randint(0,ylimit))
        agent = Person(i,agent_position)
        model.schedule.agents.add(agent)
        agent.add_agent_to_grid("virus_env", agent_position, model)
    for p in range(1,num_infectious+1):
        agent_position2 = (random.randint(0,xlimit),random.randint(0,ylimit))
        ill_agent = Person(p+i,agent_position2,initial_state=State.infectious)
        model.schedule.agents.add(ill_agent)
        ill_agent.add_agent_to_grid("virus_env",agent_position2, model)
    return model




runs = 10
#INFECTION_LIMIT = 10


infectious_pop = []
all_peak_infectious = []    #Resetting the global variables
time_taken = []
all_runstats = list()
susceptible_pop = []
avg_susceptible = []
avg_infecteds = []
recovered_pop = []
avg_recovered = []
r_0_1 = list()
for r in range(runs):                  #The model runs for however many times you want it to you can change the number of runs by changing the value in the variable.
    model = setup_model(119, 1, spatial_mode=True) #users pass in how many susceptible agents they want and how many infectious agents they want
    population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0, 'day':0}
    infectious_pop.clear()
    susceptible_pop.clear()
    recovered_pop.clear()
    model.schedule.helpers.append(Counter())                         
    model.run()
    r_0_1.append(mean([a.r_rate for a in model.schedule.agents if a.state == State.recovered]))
    
    all_runstats.append(population_stats)

total_infecteds = [run_stat['recovered_pop'] for run_stat in all_runstats]
outbreak_lengths = [run_stat['day'] for run_stat in all_runstats]
  
spatial_model_data = {'all_peak_infectious':all_peak_infectious,'time_taken':time_taken, 'total_infecteds':total_infecteds, 'outbreak_lengths':outbreak_lengths,'average_susceptible':avg_susceptible,'average_infected':avg_infecteds, 'average_recovered':avg_recovered }

################################################For loop written twice so that the spatial model runs and then non-spatial model runs.
infectious_pop = []
all_peak_infectious = []    #These are the global variables set for use anywhere in the program
time_taken = []
all_runstats = list()
susceptible_pop = []
avg_susceptible = []
avg_infecteds = []
recovered_pop = []
avg_recovered = []
r_0_2 = list()
for r in range(runs):                  #The model runs for however many times you want it to you can change the number of runs by changing the value in the variable.
    model = setup_model(119, 1, spatial_mode=False) #users pass in how many susceptible agents they want and how many infectious agents they want
    population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0, 'day':0}
    infectious_pop.clear()
    susceptible_pop.clear()
    recovered_pop.clear()
    model.schedule.helpers.append(Counter())                         
    model.run()
    r_0_2.append(mean([a.r_rate for a in model.schedule.agents if a.state == State.recovered]))
    all_runstats.append(population_stats)

total_infecteds = [run_stat['recovered_pop'] for run_stat in all_runstats]
outbreak_lengths = [run_stat['day'] for run_stat in all_runstats]
  
non_spatial_model_data = {'all_peak_infectious':all_peak_infectious,'time_taken':time_taken, 'total_infecteds':total_infecteds, 'outbreak_lengths':outbreak_lengths, 'average_susceptible':avg_susceptible,'average_infected':avg_infecteds, 'average_recovered':avg_recovered}

total_data = {'spatial_model_data':spatial_model_data,
              'non_spatial_model_data': non_spatial_model_data}

for i in range(len(all_peak_infectious)):
    print("in outbreak",i,"it took",time_taken[i],"day(s) to reach a maximum infectious population of",all_peak_infectious[i])

print("largest number of infectious cases in a day",max(all_peak_infectious))
print("On average it takes",mean(time_taken),"day(s) to reach an average maximum infectious population of",mean(all_peak_infectious))

total_infecteds = [run_stat['recovered_pop'] for run_stat in all_runstats]

print("maximum number of people infected in an outbreak is",max(total_infecteds))                                            #This is how the statistics are calculated usually done by adding specific values to a list and calculating certain results from these lists
print("minimum number of people infected in a outbreak is",min(total_infecteds))
print("average number of people infected in a outbreak is",mean(total_infecteds))                                            #The statistics allows us to analyse the behaviour of either the spatial or random model.

outbreak_lengths = [run_stat['day'] for run_stat in all_runstats]

print("longest outbreak duration is",max(outbreak_lengths),"days")
print("shortest outbreak duration is",min(outbreak_lengths),"days")
print("average outbreak duration is",mean(outbreak_lengths),"days")
print("Spatial R0 = ", r_0_1)
print("Random  R0 = ", r_0_2)
print("Spatial R0 = ", mean(r_0_1))
print("Random  R0 = ", mean(r_0_2))

with open('statistics.json', 'w') as resultfile:
    json.dump(total_data, resultfile)
