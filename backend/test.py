<<<<<<< test.py
=======
# Written by Daniel Cohen
#
# For Senior Independent Study Thesis
# The College of Wooster
#
# Feb. 27th 2023
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gui
import reaction
import variableSettings as vS
import time
import os

# -------------------------------------------------------------
#   Note: the order of object/function creation must be the 
#   following, or else it won't work properly: Functions,
#   BZ Reaction object, Figure animation, GUI object
# -------------------------------------------------------------

import matplotlib as mpl 
mpl.rcParams['animation.ffmpeg_path'] = 'C:/ffmpeg/bin/ffmpeg.exe'

dir_path = os.path.dirname(os.path.realpath(__file__))

start_time = time.time()

path = "C:/Users/augus/OneDrive/Desktop/gusJS/"
experiment_string = time.strftime("%Y-%m-%d") + "_" + str(vS.N) + "x" + str(int(vS.M))
experiment_save_file = path + experiment_string + ".mp4"
print("will attempt to save to: " + experiment_save_file)

# Select for view_animation:
#    0 -> Conduct one of the Experiments
#    1  -> View animation and play with GUI

view_animation = 1

# Create Reaction object
bzReact = reaction.BZreaction()
writervideo = animation.FFMpegWriter(fps=60)

if view_animation:

    # Update figure funtion
    def updatefig(*args):
        if bzReact.running:
            bzReact.step()
            writervideo.grab_frame()
        im.set_array(bzReact.getColors())
        return im, 

    # Create animation (must be done before GUI)
    fig = plt.figure(figsize=(10,10))
    z = bzReact.getColors()
    im = plt.imshow(z, animated=True, cmap='gnuplot2', vmin=0, vmax=1)
    f = experiment_save_file
    writervideo.setup(fig, f)
    # writergif = animation.PillowWriter(fps=30) 
    # writervideo = animation.FFMpegWriter(fps=60)
    ani = animation.FuncAnimation(
        fig, updatefig, interval=vS.T, blit=True, save_count=1000) #intervar T
    plt.show()

    # Create objects to use
    GUI = gui.reactionGUI(bzReact)
    print("Past GUI execution!")
    print("Writer created :]")
    print("Animation saving to " + experiment_save_file) 
    writervideo.finish()
else:
    
    #np.savetxt("DvsVdata.txt", bzReact.DvsVexperiment())
    #np.savetxt("Experimentdata1.txt", bzReact.experiment1())
    np.savetxt("Experimentdata2.txt", bzReact.experiment2())
    #np.savetxt("Experimentdata3.txt", bzReact.experiment3())

# Print out elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
h = int(elapsed_time/3600)
m = int((elapsed_time%3600)/60)
s = int((elapsed_time%3600)%60)

print("Elapsed time: ", h, "h  ", m, "m  ", s, "s")

>>>>>>> mainAni.py
