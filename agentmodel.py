from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper
from panaxea.core.Environment import ObjectGrid2D
from enum import IntEnum
import time
import numpy as np
from statistics import mean
import random



peak_infectious = []
all_peak_infectious = []
time_taken = []

class State(IntEnum):
    susceptible = 0
    infected = 1
    infectious = 2
    recovered = 3



class SimpleAgent(Agent):
    

    def __init__(self, name, position, initial_state=State.susceptible):
        super(SimpleAgent, self).__init__()
        self.name = name
        self.age = random.normalvariate(20,100)
        self.state = initial_state
        self.infection_duration = 0
        self.recovery_duration = 5
        self.incubation_period = 0
        self.ptrans = 0.1
        self.position = position
       
    
   

    def step_prologue(self, model):
        #print(self.position)
        
        xlimit,ylimit = env_limit(model.environments["virus_env"])
        xstart = 0
        ystart = 0


        x_direct = random.choice((-1, 0, 1))
        y_direct = random.choice((-1, 0, 1))
       
        
        

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
        if spatial_mode:
            if self.state is State.infectious:
                agents = model.schedule.agents
                neighbourhood = model.environments["virus_env"].get_moore_neighbourhood(self.position)
                neighbourhood.append(self.position)
                potential_targets = list()
                for a in agents:
                    pos_of_a = a.position
                    if pos_of_a in neighbourhood and a.state is State.susceptible:
                        potential_targets.append(a)

            self.infection_duration += 1
        return (potential_targets)         


         #else:
                        
            #randomselection
         
       
            
    def step_main(self, model):
        for someone in self.potential_targets(model.properties['spatial_transmission']):
            if someone.state is State.susceptible:
                if random.random() <= self.ptrans:
                    someone.state = State.infected

                    
       
        
            
                        
          


    def step_epilogue(self, model):

        
        if self.state == State.infected:
            self.state = State.infectious
           
        if self.state is State.infectious:
            if self.infection_duration == self.recovery_duration:
                self.state = State.recovered
               
            
      
                
class SimpleHelper(Helper):

    def step_prologue(self, model):
       
        
        population_stats['susceptible_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.susceptible])
        population_stats['infectious_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.infectious])
        peak_infectious.append(population_stats['infectious_pop'])
        population_stats['recovered_pop'] = len([agent for agent in model.schedule.agents if agent.state == State.recovered])
        population_stats['day'] = model.current_epoch
        if  population_stats['infectious_pop'] == 0:
            time_taken.append(peak_infectious.index(max(peak_infectious))+1)
            all_peak_infectious.append(max(peak_infectious))
            model.exit = True
        print(population_stats)
        
        

        print("Helper prologue")
        
        
        
    
        

    def step_epilogue(self,model):
        population_stats['newly_infected'] = len([agent for agent in model.schedule.agents if agent.state == State.infected])
        print("Helper epilogue")
        
        
        #print(State.infected)
    



def env_limit(env):
    xlimit = env.xsize - 1
    ylimit = env.ysize - 1
    return (xlimit,ylimit)





def setup_model(num_agents, num_infectious, spatial_mode=True, max_num_epochs=1000):
    model = Model(max_num_epochs)
    xsize = ysize = 30
    ObjectGrid2D("virus_env", xsize, ysize, model)
    peak_infections = []
    model.properties['spatial_transmission'] = spatial_mode
    for i in range(num_agents):
        xlimit,ylimit = env_limit(model.environments["virus_env"])
        agent_position = (random.randint(0,xlimit),random.randint(0,ylimit))
        agent = SimpleAgent(i,agent_position)
        model.schedule.agents.add(agent)
        agent.add_agent_to_grid("virus_env", agent_position, model)
    for p in range(1,num_infectious+1):
        agent_position2 = (random.randint(0,xlimit),random.randint(0,ylimit))
        ill_agent = SimpleAgent(p+i,agent_position2,initial_state=State.infectious)
        model.schedule.agents.add(ill_agent)
        ill_agent.add_agent_to_grid("virus_env",agent_position2, model)
    return model







all_runstats = list()
runs = 10
for r in range(runs):
    model = setup_model(119, 1) #users pass in how many susceptible agents they want and how many infectious agents they want
    population_stats = {'infectious_pop':0, 'newly_infected':0, 'susceptible_pop':0, 'recovered_pop':0, 'day':0}
    
    
    model.schedule.helpers.append(SimpleHelper())
    model.run()
    
    all_runstats.append(population_stats)
    
    

print(all_runstats)
print(all_peak_infectious)

 



total_infecteds = [run_stat['recovered_pop'] for run_stat in all_runstats]

#print(total_infected)
print("maximum number of people infected in an outbreak is",max(total_infecteds))
print("minimum number of people infected in a outbreak is",min(total_infecteds))
print("average number of people infected in a outbreak is",mean(total_infecteds))


outbreak_lengths = [run_stat['day'] for run_stat in all_runstats]

#print(outbreak_length)

print("longest outbreak duration is",max(outbreak_lengths),"days")
print("shortest outbreak duration is",min(outbreak_lengths),"days")
print("average outbreak duration is",mean(outbreak_lengths),"days")


print("largest number of infectious cases in a day",max(all_peak_infectious))







