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

        self.Nf=3
        self.Nperiods=3
        
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
        Label(self.optionsFrame,text='Nf:').grid(column=0,row=0)
        Label(self.optionsFrame,text='Type').grid(column=0,row=1)
        
        self.Nfentry=Spinbox(self.optionsFrame,width=2,values=tuple(range(1,10)))
        for i in range(self.Nf-1):
            self.Nfentry.invoke('buttonup')
        self.Nfentry.grid(row=0,column=1)
            
        self.inputtype=StringVar()
        Type1=Radiobutton(self.optionsFrame,value='RI',variable=self.inputtype)
        Type1.grid(row=2,column=0)
        Label(self.optionsFrame,text='Real and imaginary part').grid(row=2,column=1)
        Type2=Radiobutton(self.optionsFrame,value='AP',variable=self.inputtype)
        Type2.grid(row=3,column=0)
        Label(self.optionsFrame,text='Amplitude and phase').grid(row=3,column=1)
        self.inputtype.set('RI')
        self.updateButton=Button(self.optionsFrame,text='Update',command=self.update)
        self.updateButton.grid(row=10,column=0)
        # self.
        self.update(self)        
        


        self.draw()
        tk.mainloop()
    def update(self,event=None):
        if self.inputtype.get()=='RI':
            self.setscalars(int(self.Nfentry.get()),'RI')
        else:
            self.setscalars(int(self.Nfentry.get()),'AP')
    def setscalars(self,Nf,type):
        self.Nf=Nf
        length=300
        res=0.05
        if self.slidersFrame is not None:
            self.slidersFrame.destroy()
        self.slidersFrame=Frame(self.top,padx=10,pady=10,borderwidth=2,relief='groove')
        self.slidersFrame.grid(row=1,column=0)        

        Ns=2*Nf+1
        self.scales=[]
        scalerframe=LabelFrame(self.slidersFrame,text='Time-avg')
        scalerframe.grid(row=0,column=0)
        self.scales.append(Scale(scalerframe,from_=2,to=-2,resolution=res,length=length,command=self.draw))
        self.scales[0].set(0.)
        self.scales[0].grid(row=0,column=0)

        for i in range(1,Nf+1):
            scalerframe=LabelFrame(self.slidersFrame,text='Freq. %g' %i)

            if type=='RI':
                self.scales.append(Scale(scalerframe,from_=2,to=-2,resolution=res,length=length,command=self.draw))
                self.scales.append(Scale(scalerframe,from_=2,to=-2,resolution=res,length=length,command=self.draw))
                Label(scalerframe,text='Re').grid(row=0,column=0)
                Label(scalerframe,text='Im').grid(row=0,column=1)
            else:    
                self.scales.append(Scale(scalerframe,from_=2,to=0,resolution=res,length=length,command=self.draw))
                self.scales.append(Scale(scalerframe,from_=180,to=-180,resolution=res,length=length,command=self.draw))
                Label(scalerframe,text='Amp').grid(row=0,column=0)
                Label(scalerframe,text='Phase').grid(row=0,column=1)
                
            self.scales[2*i-1].set(0.)
            self.scales[2*i].set(0.)


            self.scales[2*i-1].grid(row=1,column=0)
            self.scales[2*i].grid(row=1,column=1)
            scalerframe.grid(row=0,column=i)
        self.scales[1].set(1.0)

        
    def draw(self,event=None):
        Ns=2*self.Nf+1
        Nf=self.Nf
        # print("Redrawing...")
        points=500
        t=np.linspace(0,self.Nperiods,points)
        pt=np.zeros(points)
        # print(t)
        
        p=np.zeros(Ns,complex)
        p0=self.scales[0].get()
        pt+=p0
        if self.inputtype.get()=='RI':
            for i in range(1,Nf+1):
                p[i]=self.scales[2*i-1].get()+1j*self.scales[2*i].get()
                # print("p[%g]:%f"%(i,p[i]))
                pt+=(p[i]*np.exp(1j*i*2*np.pi*t)).real
        else:
            for i in range(1,Nf+1):
                p[i]=self.scales[2*i-1].get()*np.exp(1j*np.pi*self.scales[2*i].get()/180)
                # print("p[%g]:%f"%(i,p[i]))
                pt+=(p[i]*np.exp(1j*i*2*np.pi*t)).real
                
        self.ax.clear()
        self.ax.plot(t,pt)
        ylim([-3,3])
        self.canvas.draw()
        # print(pt)    
m=main()





