import numpy as np;
import pandas as pd;
import time;
from maze import Maze;
from RLbrain import RLbrain;

def render():
    for j in range(200):
        maze.reset([0,0])
        is_success=False

        steps=[]
        while not is_success:
            avaliable_actions,state=maze.get_avaliable_action()#获取当前所有能执行的动作

            state_str_arr=np.array(state)/maze.unit

            state_str=str(state_str_arr)

            action=rl.choose_action(state_str,avaliable_actions)#选择动作
            reward,state_next,is_success=maze.step(action)#获取环境奖励

            steps.append([state_str,action])#存储经历，后续学习

            state_next_str_arr=np.array(state_next)/maze.unit

            state_next_str=str(state_next_str_arr)

            rl.update(state_str,action,state_next_str,reward,is_success,steps)#更新状态
            maze.render()
            maze.write_weight(rl.state_table)

        print('run end {0}'.format(j))
        print(rl.state_table.round(2))
        time.sleep(2)

        # maze.write_weight(rl.state_table)
        #进行强制更新，更新全部路径的权重多次训练之后就能够得到优秀权重
        # rl.forceUpdate(steps,reward/10)
        print("forceUpdate")
        # print(rl.state_table.round(2))


if __name__=='__main__':
    maze=Maze(7,7,chif=9)
    rl=RLbrain(maze.get_all_action())#获取所有动作
    maze.after(100,render)
    maze.mainloop()
