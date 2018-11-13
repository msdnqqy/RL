"""
    Q_learning 模型代码
    1.初始化state_table
    2.根据state_table[position,:].max() 在 可选的action中选择一个action
    3.根据action反馈reward 更新state_table

    额外方法：
        check_state_exist:检查state_table中是否存在该状态，如果不存在则在state_table中添加一行，初始化该行所有权重为0
"""
import pandas as pd;
import numpy as np;
import time ;

class RLbrain(object):
    def __init__(self,actions=['left','right','up','down'],gamma=0.9,lr=0.1):
        self.actions=actions
        self.gamma=gamma
        self.lr=lr

        self.state_table=pd.DataFrame(columns=self.actions)

    def check_state_exist(self,state):
        if state not in self.state_table.index:
            # self.state_table.loc[state]=[0.0]*len(self.actions)
            # self.state_table.loc[state]=np.random.rand((len(self.actions)))
            self.state_table.loc[state]=[0.0]*len(self.actions)

    """
        根据环境奖励、惩罚更新state_table
        state_table[state,action]+=lr*(Q_现实-Q_估计)
        Q_估计=self.state_table[state,action]
        Q_现实=reward if is_success else gamma*(state_table[state_next,:].max())
    """
    def update(self,state,action,state_next,reward,is_success,steps):
        self.check_state_exist(state)
        self.check_state_exist(state_next)

        q_pred=self.state_table.loc[state,action]
        q_real= reward if is_success else (reward+self.gamma*(self.state_table.loc[state_next,:].max()))

        if([state,action] in steps):
            self.state_table.loc[state,action]-=abs(self.lr*(q_real-q_pred))
        else:   
            self.state_table.loc[state,action]+=(self.lr*(q_real-q_pred))
        # self.state_table.loc[state,action]+=(self.lr*(q_real-q_pred))

        return is_success,self.state_table

    """
        根据state，选中权重最大的action
    """
    def choose_action(self,state,avaliable_actions):
        self.check_state_exist(state)

        #给予一定概率随机选择
        if np.random.rand()>0.9:
            return np.random.choice(avaliable_actions,size=1)[0]
        
        #其他情况从state中选择
        #选出state中权重最大的索引arr
        max_actions=np.array(avaliable_actions)[self.state_table.loc[state,avaliable_actions]==self.state_table.loc[state,avaliable_actions].max()]
        return np.random.choice(max_actions,size=1)[0]

    def forceUpdate(self,steps,reward):
        # if len(steps)<10: return
        steps_gone=[]
        for i in range(len(steps)):
            step=steps[i]
            if step[0] in steps_gone:
                self.state_table.loc[step[0],step[1]]-=abs((self.gamma**(i))*reward)
            else:
                self.state_table.loc[step[0],step[1]]+=abs((self.gamma**(i))*reward)
            steps_gone.append(step[0])
        return self.state_table


if __name__=='__main__':
    rl=RLbrain()
    print(rl.state_table)
    state='state0'
    action=rl.choose_action(state,['right','left','down'])
    state_next='state1'
    rl.update(state,action,state_next,-1,is_success=False)
    print(rl.state_table)

    state_next='state2'
    rl.update(state,action,state_next,1,is_success=True)
    print(rl.state_table)