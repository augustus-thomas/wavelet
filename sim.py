import sys
import backend
print(dir())

def main():
    # Get the arguments
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
    my_reaction = backend.reactionBH.BZreaction(f=f, q=q, e1=e1, e2=e2, uExcited=uExcited, Du_c=Du_c, Dv=Dv, phi_c=phi_c)

    # step the reaction
    for i in range(int(steps)):
        my_reaction.step()
    
    # save the reaction to /static/sim.mp4

if __name__ == "__main__":
    main()