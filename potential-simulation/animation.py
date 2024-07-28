from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
from electrode import TElectrode
from trap import TTrap

class AnimationObject:
    fig=None
    ax=None
    fps=5
    trapping_sequence:[{}] = []

    def __init__(self,trap:TTrap,fps=5,figsize:()=(16,8)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.trap = trap
        self.fps=fps
        self.trapping_sequence = []
    
    def __animate(self,i):
        self.ax.clear()
        self.ax.set_ylim(-500,500)
        self.ax.set_xticks(self.trap.GetLabelPositions())
        self.ax.set_xticklabels(self.trap.GetElectrodeNames())
        self.ax.set_xticks(self.trap.GetMinorLabelPositions(),minor=True)
        self.ax.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
        self.ax.tick_params(which = "minor", bottom = False, left = False)
        plt.xticks(rotation=45)
        # self.ax.set_title(self.trapping_sequence[i]['name'])
        # self.ax.text(0,0,self.trapping_sequence[i]['name'])
        # print(f"{i}:{self.trapping_sequence[i]['name']}[{self.trapping_sequence[i]['iteration']}]")
        self.ax.set_xlabel("electrode")
        self.ax.set_ylabel("voltage [V]")
        line = self.ax.stairs(self.GetFrame(i))
        return line,

    def animate(self,show=True,save=False):
        # for i,val in enumerate(self.trapping_sequence):
        #     print(f"{i}->{val['name']}[{val['iteration']}]")
        ani = FuncAnimation(self.fig, self.__animate, interval=100, blit=True, repeat=True, frames=len(self.trapping_sequence),repeat_delay=500)
        if save:
            ani.save("potential.gif", dpi=150, writer=PillowWriter(fps=self.fps))
        if show:
            plt.show()
        return ani
        
    
    def add_sequence(self,handle_name:str):
        for i in range(self.trap.GetHandleDuration(handle_name)):
            sequence = {}
            sequence['name']=handle_name 
            sequence['iteration']=i
            self.trapping_sequence.append(sequence)


    def add_wait(self,frames=10):
        for i in range(frames):
            sequence = self.trapping_sequence[-1]
            self.trapping_sequence.append(sequence)



    def GetFrame(self,i):
        return self.trap.dma_playback(self.trapping_sequence[i]['iteration'],self.trapping_sequence[i]['name'])