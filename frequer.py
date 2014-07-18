#!/usr/bin/python
from tkinter import *
import Pmw
import numpy as np
from matplotlib.pyplot import figure,ylim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Frequer: a small application to interactively show what happens to a
#wave when more harmonics are added.
x=np.linspace(0,10,10)

def quit(event=None):
    tk.quit()
    tk.destroy()

tk=Tk()
tk.configure(background='gray')
tk.title('Frequer')
Pmw.initialise(tk)
tk.bind('<q>', quit)

class main(object):
    def __init__(self):
        self.top=Frame(tk,borderwidth=2,relief='groove')
        self.top.grid(row=0,column=0)
        self.slidersFrame=None


        #Creating the plotframe    
        self.plotframe=Frame(self.top,padx=10,pady=10,borderwidth=2,relief='groove')
        fig=figure(figsize=(8,3))
        self.canvas = FigureCanvasTkAgg(fig, master=self.top)
        self.canvas.draw()
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0,column=0,sticky=NSEW)
        self.ax=fig.add_subplot(111)

        #Creating side options:
        self.optionsFrame=Frame(self.top,padx=10,pady=10,borderwidth=2,relief='groove')
        self.optionsFrame.grid(column=1,row=0)
        w=Label(self.optionsFrame,text='Nf:')
        w.grid(column=0,row=0)
        # self.

        
        self.Nf=4
        self.setscalers(4)
        self.draw()
        tk.mainloop()

    def setscalers(self,Nf):
        if self.slidersFrame is not None:
            self.slidersFrame.destroy()
        self.slidersFrame=Frame(self.top,padx=10,pady=10,borderwidth=2,relief='groove')
        self.slidersFrame.grid(row=1,column=0)        

        Ns=2*Nf+1
        self.scales=[]
        scalerframe=LabelFrame(self.slidersFrame,text='Time-avg')
        scalerframe.grid(row=0,column=0)
        self.scales.append(Scale(scalerframe,from_=2,to=-2,resolution=0.1,command=self.draw))
        self.scales[0].set(0.)
        self.scales[0].grid(row=0,column=0)

        for i in range(1,Nf+1):
            scalerframe=LabelFrame(self.slidersFrame,text='Freq. %g' %i)
            self.scales.append(Scale(scalerframe,from_=2,to=-2,resolution=0.1,command=self.draw))
            self.scales.append(Scale(scalerframe,from_=2,to=-2,resolution=0.1,command=self.draw))
            self.scales[2*i-1].set(0.)
            self.scales[2*i].set(0.)
            Label(scalerframe,text='Re').grid(row=0,column=0)
            Label(scalerframe,text='Im').grid(row=0,column=1)
            self.scales[2*i-1].grid(row=1,column=0)
            self.scales[2*i].grid(row=1,column=1)
            scalerframe.grid(row=0,column=i)
        self.scales[1].set(1.0)

        
    def draw(self,event=None):
        Ns=2*self.Nf+1
        Nf=self.Nf
        # print("Redrawing...")
        points=500
        t=np.linspace(0,3,points)
        pt=np.zeros(points)
        # print(t)
        
        p=np.zeros(Ns,complex)
        p0=self.scales[0].get()
        pt+=p0
        for i in range(1,Nf+1):
            p[i]=self.scales[2*i-1].get()+1j*self.scales[2*i].get()
            # print("p[%g]:%f"%(i,p[i]))

            pt+=(p[i]*np.exp(1j*i*2*np.pi*t)).real
        self.ax.clear()
        self.ax.plot(t,pt)
        ylim([-3,3])
        self.canvas.draw()
        # print(pt)    
m=main()
