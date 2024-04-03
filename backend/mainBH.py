
# Written by Daniel Cohen
#
# For Senior Independent Study Thesis
# The College of Wooster
#
# Feb. 27th 2023

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gui
import reactionBH
import variableSettingsBH as vS
import time

start_time = time.time()

# Select for view_animation:
#    0 -> Conduct one of the Experiments
#    1  -> View animation and play with GUI

view_animation = 1

# Create Reaction object
bzReact = reactionBH.BZreaction()


if view_animation:

    # Update figure funtion
    def updatefig(*args):
        if bzReact.running: 
            bzReact.step()
        im.set_array(bzReact.getColors())
        return im,

    # Create animation
    fig = plt.figure(figsize=(5,5))
    z = bzReact.getColors()
    im = plt.imshow(z, animated=True, cmap='gnuplot2', vmin=0, vmax=1, interpolation='bilinear')
    plt.axis('off')
    ani = animation.FuncAnimation( fig, updatefig, interval=vS.T, blit=True, cache_frame_data=False)

    # Create GUI
    GUI = gui.reactionGUI(bzReact, fig)

#else:
    # Run experiments here disableing the GUI for faster data collection

# Print out elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
h = int(elapsed_time/3600)
m = int((elapsed_time%3600)/60)
s = int((elapsed_time%3600)%60)

print("Elapsed time: ", h, "h  ", m, "m  ", s, "s")
