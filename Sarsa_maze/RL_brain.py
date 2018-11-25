import numpy as np;
import pandas as pd;

class RL(object):
    def __init__(self,actions=['right','left','up','down']):
        self.actions=actions
        self.gamma=0.9
        self.lr=0.01
        self.choose_rate=0.9

        self.q_table=pd.DataFrame(columns=self.actions)

    def choose_action(self,observation):
        self.check_state_exist(observation)

        if np.random.rand()<self.choose_rate:
            state_action=self.q_table.loc[observation,:]
            action=np.random.choice(state_action[state_action==np.max(state_action)].index)

        else:
            action=np.random.choice(self.actions)
        return action
        
    def check_state_exist(self,observation):
        if observation not in self.q_table.index:
            q_table.loc[observation]=[0]*len(self.actionsk)