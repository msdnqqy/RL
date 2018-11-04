import numpy as np;
import pandas as pd;
import time;

class Env:
    def __init__(self,length=7):
        self.length=length#长度
        self.target_position=np.random.randint(0,length)#目标位
        self.all_action=['left','right']#可执行的所有动作
    """
    重新生成人物的位置
    """
    def reset(self):
        self.role_position=np.random.randint(0,self.length)
        return self.role_position

    """
    获取当前可以移动的位置
    """
    def get_avaliable_action(self):
        if self.role_position==0:
            self.avaliable_action=['right']
        elif self.role_position==(self.length-1):
            self.avaliable_action=['left']
        else:
            self.avaliable_action=['left','right']
        return self.avaliable_action

    """
    获取反馈+新的位置
    """
    def get_feedback(self,action):
        step=1 if action=='right' else -1
        if (self.role_position+step)==self.target_position:
            self.role_position+=step;
            return 1,self.role_position
        else:
            self.role_position+=step;
            return 0,self.role_position


class RLBrain:
    def __init__(self,actions=['left','right']):
        self.actions=actions
        self.table=pd.DataFrame(columns=actions)#生成空的对象
        self.a=0.7
        self.p=0.1

    """
    检查状态是否存在
    """
    def check_state_exist(self,position):
        if not (position in self.table.index):
            self.table.loc[position]=[0.0 for i in range(len(self.actions))]


    """
    更新自己的状态值
    """
    def update(self,position,action,reward,position_next):
        #[position,action]+=p(Q现实-Q估计)
        #Q现实=1 or a([postion_next,:].max)
        self.check_state_exist(position_next)
        q_real=reward if reward==1 else self.a*self.table.loc[position_next,:].max()
        q_pred=self.table.loc[position,action]
        self.table.loc[position,action]+=self.p*(q_real-q_pred)
        return True if reward==1 else False

    def choose_action(self,position):
        self.check_state_exist(position)
        action=''
        if np.random.rand()>0.9:
            action=np.random.choice(self.actions,size=1)
            return action
        else:
            action=np.random.choice(self.table.loc[position,self.table.loc[position,:]==self.table.loc[position,:].max()].index)
            return action

    def choose_action_from_avaliable(self,positon,avaliable_action):
        self.check_state_exist(positon)
        action=''
        if np.random.rand()>0.9:
            action=np.random.choice(avaliable_action,size=1)
        else:
            #从可选的动作中选择最大的
            max_action=np.array(avaliable_action)[self.table.loc[positon,avaliable_action]==self.table.loc[positon,avaliable_action].max()]
            action=np.random.choice(max_action,size=1)

        return action[0]


def mainloop():
    role=Env(10)
    
    rl=RLBrain(role.all_action)

    for i in range(10):
        role.reset()
        is_success=False
        step=0
        while not is_success:
            step+=1
            position=role.role_position
            actions_avaliable=role.get_avaliable_action()
            action=rl.choose_action_from_avaliable(position,actions_avaliable)
            reward,position_next=role.get_feedback(action)
            is_success=rl.update(position,action,reward,position_next)
        
        print("i:{0}\nstep:{1}\ntarget:{3}\ntable:{2}".format(i,step,rl.table,role.target_position))




if __name__=='__main__':
    mainloop()

# if __name__=="__main__":
#     role=Env(10)
#     role.reset()
#     actions=role.get_avaliable_action()
#     postion=role.role_position
#     # feedback=role.get_feedback(actions[0])
#     print("actions:{0}\nposition：{1}\nfeedback:{2}".format(actions,postion,0))

#     rl=RLBrain(role.all_action)
#     print(rl.table)
#     action=rl.choose_action_from_avaliable(postion,role.get_avaliable_action())
#     reward,position_next=role.get_feedback(action)
#     rl.update(postion,action,reward,position_next)
#     print(rl.table)


