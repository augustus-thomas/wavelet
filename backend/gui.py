# Written by Daniel Cohen
#
# For Senior Independent Study Thesis
# The College of Wooster
#
# Feb. 27th 2023

import tkinter as tk
from ttkthemes import ThemedStyle
from tkinter import ttk
import variableSettingsBH as vS
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from matplotlib.figure import Figure 

class reactionGUI:
    def __init__(self, obj, fig): # Initial GUI setup
        # Window aspect
        self.root = tk.Tk()
        self.root.title("BZ Reaction")
        self.root.geometry("800x1000")
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")

        # End GUI when window is closed
        def on_closing():
            self.root.quit()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # reaction object
        self.reaction = obj
        
        #Buttons
        self.pauseBt = ttk.Button(self.root, text="Play/Pause", command=self.pauseF, width=10)
        self.restartBt = ttk.Button(self.root, text="Restart", command=self.restartF, width=10)
        self.stepBt = ttk.Button(self.root, text="1 step", command=self.stepF, width=10)
        
        # Lables
        ttk.Label(self.root, text="\t").grid(row=0, column=1)
        ttk.Label(self.root, text=" Chemical parameters ", borderwidth=1, relief="solid").grid(row=1, column=1, columnspan=2)
        ttk.Label(self.root, text=" Obstacle parameters ", borderwidth=1, relief="solid").grid(row=1, column=3, columnspan=2)
        ttk.Label(self.root, text=" Simulation Parameters ", borderwidth=1, relief="solid").grid(row=1, column=5, columnspan=2)
        ttk.Label(self.root, text="\t").grid(row=0, column=1)
        ttk.Label(self.root, text="f : ", anchor="e").grid(row=2, column=1, sticky="e")
        ttk.Label(self.root, text="q : ", anchor="e").grid(row=3, column=1, sticky="e")
        ttk.Label(self.root, text="\u03B5 : ", anchor="e").grid(row=4, column=1, sticky="e") #epsilon
        ttk.Label(self.root, text="\tr : ", anchor="e").grid(row=2, column=3, sticky="e")
        ttk.Label(self.root, text="Dᵤ : ", anchor="e").grid(row=3, column=3, sticky="e")
        ttk.Label(self.root, text="φ: ", anchor="e").grid(row=4, column=3, sticky="e") 
        ttk.Label(self.root, text="\u0394t : ", anchor="e").grid(row=4, column=5, sticky="e") #Delta t

        
        # Entry lables
        self.eText = ttk.Entry(self.root, width=7)
        self.fText = ttk.Entry(self.root, width=7)
        self.qText = ttk.Entry(self.root, width=7)
        self.dtText = ttk.Entry(self.root, width=7)
        self.rText = ttk.Entry(self.root, width=7)
        self.DuText = ttk.Entry(self.root, width=7)
        self.phiText = ttk.Entry(self.root, width=7)
        
        # Initial values for entry labels
        self.eText.insert(0, str(vS.e1))
        self.fText.insert(0, str(vS.f))
        self.qText.insert(0, str(vS.q))
        self.dtText.insert(0, str(vS.dt))
        self.rText.insert(0, str(vS.r))
        self.DuText.insert(0, str(vS.Du))
        self.phiText.insert(0, str(vS.phi))
        
        # Location of widgets
        self.pauseBt.grid(row=1, column=0)
        self.restartBt.grid(row=2, column=0)
        self.stepBt.grid(row=4, column=0)
        self.eText.grid(row=4,column=2)
        self.fText.grid(row=2,column=2)
        self.qText.grid(row=3,column=2)
        self.phiText.grid(row=4,column=4)
        self.rText.grid(row=2,column=4)
        self.DuText.grid(row=3,column=4)
        self.dtText.grid(row=4,column=6)
        
        # Dropdown menu for obstacle
        options = [
            "Obstacle Type",
            "Uniform Diffuson",
            "Light Diode",
            "Gravitational Well"
        ]

        # Dropdown menu function to change obstacle and restart 
        def ObstacleCallback(selection):
            if (selection == "Uniform Diffuson"):
                self.reaction.setObstacle(0)
            elif (selection == "Light Diode"):
                self.reaction.setObstacle(1)
            elif (selection == "Gravitational Well"):
                self.reaction.setObstacle(2)
            else:
                print("Error selecting obstacle from dropdown menu. self.clicked.get() = ", selection)

            self.restartF()
          
        # datatype of menu text
        self.clicked = tk.StringVar()
          
        # initial menu text
        self.clicked.set( "No Obstacle" )
          
        # Create Dropdown menu
        drop = ttk.OptionMenu( self.root, self.clicked,  *options, command=ObstacleCallback)
        drop.grid(row=2,column=6)
        
        
        # Dropdown menu for source

        options2 = [
            "Source",
            "Line Wave",
            "Point Wave"
        ]

        # Dropdown menu function to change source and restart 
        def SourceCallback(selection):
            if (selection == "Line Wave"):
                self.reaction.setSource(0)
            elif (selection == "Point Wave"):
                self.reaction.setSource(1)
            else:
                print("Error selecting source from dropdown menu. self.clicked2.get() = ", selection)

            self.restartF()
          
        # datatype of menu text
        self.clicked2 = tk.StringVar()
          
        # initial menu text
        self.clicked2.set( "Source" )
          
        # Create Dropdown menu
        ttk.drop2 = ttk.OptionMenu( self.root, self.clicked2,  *options2, command=SourceCallback)
        ttk.drop2.grid(row=3,column=6)

        # Embed figure into the GUI
        canvas = FigureCanvasTkAgg(fig, 
                                master = self.root)   
        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=7)
    
                
        # MainLoop
        self.root.mainloop()

        return
    
    
    # GUI Fucntions
    
    def pauseF(self): # Pause button
        if self.reaction.running:
            self.reaction.running = False
        else:
            self.reaction.running = True
        return
    
    def restartF(self): # Restart Button
        
        # obtain parameters from GUI and plug into simulation
        vS.e1 = float(self.eText.get())
        vS.f = float(self.fText.get())
        vS.q = float(self.qText.get())
        vS.dt = float(self.dtText.get())
        vS.r = float(self.rText.get())
        vS.Du = float(self.DuText.get())
        vS.phi = float(self.phiText.get())
        
        self.reaction.reset()
        self.reaction.running = True
        
        return
    
    
    # Advance the reaction one step
    def stepF(self): # Pause button
        #for i in range(100):
        self.reaction.step()
        return
    
    