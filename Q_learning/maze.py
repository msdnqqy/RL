"""
    Q_learning环境
"""
import tkinter as tk
import pandas as pd;
import numpy as np;
import time;

class Maze(tk.Tk,object):

    """
        1.初始化画布宽高
        2.初始化目标位置（只有一个）
        3.初始化陷阱个数和位置
    """
    def __init__(self,width=8,height=10,target=None,chif=9):
        super(Maze,self).__init__()
        self.title('my Maze')
        
        self.maze_width=width
        self.maze_height=height
        self.unit=80#每个格子的大小

        #初始化目标位置坐标
        target= target if (target !=None) else [np.random.randint(0,self.maze_width,size=1)[0],np.random.randint(0,self.maze_height,size=1)[0]]
        self.target=target

        #初始化陷阱坐标
        chif_x=np.random.randint(0,self.maze_width,size=(chif,1))
        chif_y=np.random.randint(0,self.maze_height,size=(chif,1))

        #合并横纵坐标
        self.chif=chif
        self.chif_xy=np.hstack([chif_x,chif_y])

        self.geometry('{0}x{1}'.format((self.maze_width)*self.unit,(self.maze_height)*self.unit))
        self.build()
        self.reset()

    """
        根据初始化内容画UI
    """
    def build(self):
        self.canvas=tk.Canvas(self,bg='white',height=self.maze_height*self.unit,width=self.maze_width*self.unit)
        
        #画竖线
        for i in range(self.maze_width):
            self.canvas.create_line(i*self.unit,0,i*self.unit,self.unit*self.maze_height,fill='green',width=1)
        
        #画横线
        for i in range(self.maze_height):
            self.canvas.create_line(0,i*self.unit,self.unit*self.maze_width,i*self.unit,fill='green',width=1)
        
        for i in range(self.maze_width):
            for j in range(self.maze_height):
                self.canvas.create_text(self.unit*(0.5+i),self.unit*(0.5+j),text="({0},{1})".format(i,j))
        #画陷阱
        chif_arr=[]
        for ｉ in range(len(self.chif_xy)):
            x=self.chif_xy[i][0]
            y=self.chif_xy[i][1]

            length=self.unit
            item=self.canvas.create_rectangle(x*length,y*length,(x+1)*length,(y+1)*length,fill="black")
            chif_arr.append(self.canvas.coords(item))

        self.chif_arr=chif_arr
        #画目标

        x=self.target[0]
        y=self.target[1]
        item=self.canvas.create_oval(x*length,y*length,(x+1)*length,(y+1)*length,fill='yellow')
        self.target_arr=[self.canvas.coords(item)]

        self.canvas.pack()
        # self.mainloop()
    
    """
        渲染uI变化
    """
    def render(self):
        time.sleep(0.03)
        self.update()

    def get_avaliable_action(self):
        role_position=np.array(self.canvas.coords(self.role))
        role_position/=self.unit

        direction=np.array(['up','down','right','left'])
        direction_able=np.array([True,True,True,True])

        #目标无法超越边界
        if role_position[0]==0:
            direction_able[3]=False
        if role_position[0]==(self.maze_width-1):
            direction_able[2]=False
        if role_position[1]==0:
            direction_able[0]=False
        if role_position[1]==(self.maze_height-1):
            direction_able[1]=False
        
        return direction[direction_able],self.unit*role_position


    def get_all_action(self):
        return ['right','up','left','down']

    """
        步进环境,
        返回奖励，状态
    """
    def step(self,action):
        x=0
        y=0
        if action=='right':
            x=self.unit
        elif action=='left':
            x=-self.unit
        elif action=='up':
            y=-self.unit
        elif action=='down':
            y=self.unit

        #移动role
        self.canvas.move(self.role,x,y)
        #获取role的新坐标
        role_position_next=self.canvas.coords(self.role)

        #计算奖励
        is_success=False
        if role_position_next in self.target_arr:
            reward=100
            is_success=True
        elif role_position_next in self.chif_arr:
            reward=-100
        else:
            reward=0
        
        return reward,role_position_next,is_success

    """
        重置人物位置，返回人物当前坐标
    """
    def reset(self,position=None):
        try:
            self.canvas.delete(self.role)
        except:
            print('no role')
        if position!=None:
            role_position=self.unit*np.array([position[0],position[1]])
        else:
            role_position=self.unit*np.array([np.random.randint(0,self.maze_width,size=1)[0],np.random.randint(0,self.maze_height,size=1)[0]])
        
        self.role=self.canvas.create_rectangle(role_position[0],role_position[1],role_position[0]+self.unit,role_position[1]+self.unit,fill='red')
        self.update()
        return self.canvas.coords(self.role)

def render():
    # action='right'
    for j in range(20):
        time.sleep(2)
        maze.reset([2,3])
        for i in range(4):
            action=np.random.choice(maze.get_avaliable_action()[0],size=1)[0]
            maze.step(action)
            maze.render()
        

if __name__=='__main__':
    maze=Maze()
    maze.after(100,render)
    maze.mainloop()