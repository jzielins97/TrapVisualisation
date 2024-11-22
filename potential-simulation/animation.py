import matplotlib as mpl
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
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
        self.fig.set_animated=True
        self.trap = trap
        self.fps=fps
        self.trapping_sequence = []
        self.labels_positions = self.trap.GetLabelPositions()
        self.labels = self.trap.GetElectrodeNames()
        self.minor_labels_positions = self.trap.GetMinorLabelPositions()
        self.title = self.ax.text(0.5,0.85, "") # , bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, ha="center"
    
    def __animate(self,i):
        # turn off all voltages
        if i==0:
            self.trap.SetEverythingToZero()
        # self.fig.clear()
        self.ax.clear()
        
        # self.ax.text(0,0,self.trapping_sequence[i]['name'])
        # print(f"{i}:{self.trapping_sequence[i]['name']}[{self.trapping_sequence[i]['iteration']}]")

        self.ax.set_xticks(self.labels_positions)
        self.ax.set_xticklabels(self.labels)
        self.ax.set_xticks(self.minor_labels_positions,minor=True)
        self.ax.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
        self.ax.tick_params(which = "minor", bottom = False, left = False)
        self.ax.set_xlabel("electrode")
        self.ax.set_ylabel("voltage [V]") 
        self.ax.set_ylim(-500,500)
        # self.title.set_text()
        title = self.ax.text(1000,450, f"{i}:{self.trapping_sequence[i]['iteration']}:{self.trapping_sequence[i]['name']}")
        # self.ax.set_title()
        line = self.ax.stairs(self.GetFrame(i))
        plt.xticks(rotation=45)  

        return line, title,

    def animate(self,show=True,save=False,file='potential'):
        mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\jzielins\\ffmpeg\\bin\\ffmpeg.exe'
        # for i,val in enumerate(self.trapping_sequence):
        #     print(f"{i}->{val['name']}[{val['iteration']}]")
        ani = FuncAnimation(self.fig, self.__animate, interval=1000/self.fps, blit=True, repeat=True, frames=len(self.trapping_sequence),repeat_delay=500)
        if save: 
            print('Saving as mp4...')
            ani.save(file+'.mp4', dpi=150, writer=FFMpegWriter(fps=60))
            print('DONE')
            print('Saving as gif...')
            ani.save(file+'.gif', dpi=150, writer=PillowWriter(fps=self.fps))
            print('DONE')
        if show:
            plt.show()
        return ani
    
    def plot_current_state(self):
        self.ax.clear()
        self.ax.set_xticks(self.labels_positions)
        self.ax.set_xticklabels(self.labels)
        self.ax.set_xticks(self.minor_labels_positions,minor=True)
        self.ax.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
        self.ax.tick_params(which = "minor", bottom = False, left = False)
        self.ax.set_xlabel("electrode")
        self.ax.set_ylabel("voltage [V]") 
        self.ax.set_ylim(-500,500)
        # self.title.set_text()
        # self.ax.text(1000,450, f"{i}:{self.trapping_sequence[i]['iteration']}:{self.trapping_sequence[i]['name']}")
        # self.ax.set_title()
        self.ax.stairs(self.trap.get_final_V())
        plt.xticks(rotation=45)  

        plt.show()
        
    
    def add_sequence(self,handle_name:str):
        self.trapping_sequence =  self.trapping_sequence + [{'name':handle_name,'iteration':i} for i in range(self.trap.GetHandleDuration(handle_name))]


    def add_wait(self,seconds=1):
        self.trapping_sequence =  self.trapping_sequence + [self.trapping_sequence[-1] for i in range(seconds * self.fps)]


    def GetFrame(self,i):
        return self.trap.dma_playback(self.trapping_sequence[i]['iteration'],self.trapping_sequence[i]['name'])