import numpy as np;
import pandas as pd;
import time;
from maze import Maze;
from RLbrain import RLbrain;

def render():
    for j in range(200):
        maze.reset()
        is_success=False

        while not is_success:
            avaliable_actions,state=maze.get_avaliable_action()#获取当前所有能执行的动作

            state_str_arr=[str(x) for x in state]
            state_str=",".join(state_str_arr)

            action=rl.choose_action(state_str,avaliable_actions)#选择动作
            reward,state_next,is_success=maze.step(action)#获取环境奖励

            state_next_str_arr=[str(x) for x in state_next]
            state_next_str=",".join(state_next_str_arr)

            rl.update(state_str,action,state_next_str,reward,is_success)#更新状态
            maze.render()

        print('run end {0}'.format(j))
        print(rl.state_table)
        time.sleep(2)
        maze.reset([1,1])


if __name__=='__main__':
    maze=Maze(4,4,chif=2)
    rl=RLbrain(maze.get_all_action())#获取所有动作
    maze.after(100,render)
    maze.mainloop()
