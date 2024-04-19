import sys
sys.path.append('../backend')
import backend
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def __init__():
    pass
def main():
    # Get the arguments from script call
    f = sys.argv[1]
    q = sys.argv[2]
    e1 = sys.argv[3]
    e2 = sys.argv[4]
    uExcited = sys.argv[5]
    Du_c = sys.argv[6]
    Dv = sys.argv[7]
    phi_c = sys.argv[8]
    steps = sys.argv[9]

    # initialize reaction with arguments
    bzReact = backend.reactionBH.BZreaction(f=f, q=q, e1=e1, e2=e2, uExcited=uExcited, Du_c=Du_c, Dv=Dv, phi_c=phi_c)

    # not sure how this scope should work, but this is for plots
    import matplotlib as mpl
    # set the ffmpeg binary path for saving with that script
    mpl.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

    # video file save location
    dir_name = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_name, 'static', 'sim.mp4')

    # create writer object
    writervideo = animation.FFMpegWriter(fps=1)

    # update figure function
    def updatefig(*args):
        bzReact.step()
        writervideo.grab_frame()
        im.set_array(bzReact.getColors())
        return im, 

    # create animation
    fig = plt.figure(figsize=(5,5))
    z = bzReact.getColors()
    plt.axis('off')
    im = plt.imshow(z, animated=True, cmap='gnuplot2', vmin=0, vmax=1)
    f = path
    writervideo.setup(fig, f)
    # run animation
    ani = animation.FuncAnimation(
        fig, updatefig, interval=backend.variableSettingsBH.T, blit=True, save_count=int(steps))

    # finsh writing the video stream
    # save the reaction to /static/sim.mp4
    writervideo.finish()

    return True
if __name__ == "__main__":
    main()