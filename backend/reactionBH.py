# Written by Daniel Cohen
#
# For Senior Independent Study Thesis
# The College of Wooster
#
# Feb. 27th 2023

import numpy as np
import variableSettingsBH as vS
from math import sqrt, tan, atan, acos


class BZreaction:
    # --------------------------------------------------------------------------
    #                            Constructor
    # --------------------------------------------------------------------------
    def __init__(self):

        # Define initial parameters

        self.t = 0.1
        self.u = np.zeros((vS.N + 1, vS.N + 1), float)
        self.v = np.zeros((vS.N + 1, vS.N + 1), float)
        self.phi = np.zeros((vS.N + 1, vS.N + 1), float)
        self.lap = np.zeros((2, vS.N + 2, vS.N + 2), float)
        self.dudDu = np.zeros((2, vS.N + 2, vS.N + 2), float) # For variable diffusion correction term
        self.obstacles = np.full((vS.N + 1, vS.N + 1), False)
        self.k = 0
        self.kprm = 1
        self.Du = np.zeros((vS.N + 1, vS.N + 1), float)
        #self.obstacleMode = 0  # No obstacle
        self.obstacleMode = 1  # Light Diode
        #self.sourceMode = 0  # Line wave
        self.sourceMode = 1 # Point wave
        #self.sourceMode = 2 # inverted circle
        self.rs = 2 * vS.m # Set G = c = 1 
        self.u_th = 0

        # Reset array
        self.reset()
        self.running = True

        return

    # --------------------------------------------------------------------------
    #                          Pause/Reset reaction
    # --------------------------------------------------------------------------
    def pause(self):
        if self.running:
            self.running = False
        else:
            self.running = True
        return

    def reset(self):
        self.k = 0
        self.kprm = 1
        self.t = 0.1

        # reset arrays
        for i in range(vS.N + 1):
            for j in range(vS.N + 1):
                self.u[i, j] = 0.0
                self.v[i, j] = 0.0

                self.lap[0, i, j] = 0.0
                self.lap[1, i, j] = 0.0

        # Create obstacle position arrays
        self.createObstacle()

        # Create wavefronts on array
        self.initWaveFront()

        self.setObstacle(self.obstacleMode)
        return
    
    # --------------------------------------------------------------------------
    #                            Obstacle Functions
    # --------------------------------------------------------------------------

    # Create a wavefront in the reaction
    def initWaveFront(self):

        if self.sourceMode == 0: # Line source
            for i in range(1, vS.N + 1):
                self.u[i, 1] = vS.uExcited
                self.v[i, 1] = 0.0
        elif self.sourceMode == 1: # Point source
            if self.obstacleMode == 1:
                self.u[vS.L, vS.L] = vS.uExcited
                self.v[vS.L, 1] = 0.0
        elif self.sourceMode == 2: # Inverted circle
            
        else:
            self.u[vS.L, 1] = vS.uExcited
            self.v[vS.L, 1] = 0.0
            
        else:
            print("Error selecting the source in initWaveFront()")

        return


    def createObstacle(self):
        #   ---------------------------------------------
        #       0 -> Uniform diffuson
        #       1 -> Light Diode
        #       2 -> Gravitational Well
        #   ---------------------------------------------

        if self.obstacleMode == 0: # Uniform Diffusion
            for i in range(vS.N + 1):
                for j in range(vS.N + 1):
                    self.obstacles[i, j] = True
                    self.Du[i, j] = vS.Du * vS.D
                    self.phi[i, j] = 0.0


        elif self.obstacleMode == 1: # Light Diode
            for i in range(vS.N + 1):
                for j in range(vS.N + 1):

                    d = sqrt((i - vS.L) ** 2 + (j - vS.L) ** 2)

                    if vS.r <= d:
                        self.phi[i, j] = 0
                    else:
                        self.phi[i, j] = vS.phi * d / vS.r

                    self.obstacles[i, j] = True
                    self.Du[i, j] = vS.Du * vS.D

        else: # Gravtiataional Well Obstacle
            for i in range(vS.N + 1):
                for j in range(vS.N + 1):
                    self.phi[i, j] = 0.0

                    d = sqrt((i - vS.L) ** 2 + (j - vS.L) ** 2)

                    if self.rs >= d:
                        self.Du[i, j] = 0
                    else:
                        self.Du[i, j] = vS.D * (1 - 2 * self.rs / d)
        return

    def setObstacle(self, i):

        #   ---------------------------------------------
        #       0 -> Uniform diffuson
        #       1 -> Light Diode
        #       2 -> Gravitational Well 
        #   ---------------------------------------------
        self.obstacleMode = i
        if i < 0 or i > 2:
            print("Error: Selected wrong obstacle")

        # For GL obstacle
        self.rs = 2 * vS.m

        return

    def setSource(self, i):
        # Options for source
        #   ---------------------------------------------
        #       0 -> Line wave
        #       1 -> Point wave
        #   ---------------------------------------------

        if not (i != 0 or i != 1):
            print("Error! tried to set wrong source")
            return

        self.sourceMode = i

        return

    # --------------------------------------------------------------------------
    #                                  Evolution
    # --------------------------------------------------------------------------

    def step(self):
        
        # Uncomment for wave train
        #vS.t += 1
        #if vS.t % 75 == 0:
        #    self.initWaveFront()
            
        # Interchange k and k' 
        ktmp = self.kprm
        self.kprm = self.k
        self.k = ktmp

        # main loop
        for i in range(1, vS.N + 1):
            for j in range(1, vS.N + 1):

                if self.u[i, j] < vS.delta:
                    self.u[i, j] = self.Du[i, j] * self.lap[self.k, i, j] / 6 
                    self.v[i, j] = (1 - vS.dt) * self.v[i, j]
                else:

                    F_u = self.u[i,j] * (1.0 - self.u[i,j]) - (vS.f * self.v[i,j] + self.phi[i,j]) * ((self.u[i,j]-vS.q) / (self.u[i,j] + vS.q))
                    F_u /= vS.e1
                    du_dt = F_u + self.Du[i, j] * self.lap[self.k, i, j] / 6 + self.dudDu[self.k, i, j]
                    
                    # Update activator
                    # W. Jahnke, W. Skaggs, A. Winfree, J. Phys. Chem. 93 (2) (1989) 740–749.
                    self.u[i, j] = max(self.u[i,j] + du_dt * vS.dt, vS.q)

                    # Update inhibitor
                    self.v[i, j] += vS.dt * (self.u[i, j] - self.v[i, j])

                    #           Finite difference Laplacian
                    self.lap[self.kprm, i, j] -= 24 * self.u[i, j]
                    # Horizontal and vertical pixels
                    self.lap[self.kprm, i + 1, j] += 4 * self.u[i, j]
                    self.lap[self.kprm, i - 1, j] += 4 * self.u[i, j]
                    self.lap[self.kprm, i, j + 1] += 4 * self.u[i, j]
                    self.lap[self.kprm, i, j - 1] += 4 * self.u[i, j]
                    # Diagonal pixels
                    self.lap[self.kprm, i + 1, j + 1] += 2 * self.u[i, j]
                    self.lap[self.kprm, i - 1, j + 1] += 2 * self.u[i, j]
                    self.lap[self.kprm, i - 1, j - 1] += 2 * self.u[i, j]
                    self.lap[self.kprm, i + 1, j - 1] += 2 * self.u[i, j]

                self.lap[self.k, i, j] = 0
                self.dudDu[self.k, i, j] = 0


        # Variable Diffusion term
        for i in range(1, vS.N):
            for j in range(1, vS.N):
                self.dudDu[self.kprm, i, j] += 0.25*(self.u[i-1,j] - self.u[i+1,j]) * (self.Du[i-1,j] - self.Du[i+1,j])
                self.dudDu[self.kprm, i, j] += 0.25*(self.u[i,j-1] - self.u[i,j+1]) * (self.Du[i,j-1] - self.Du[i,j+1])

        # impose no-flux boundary conditions
        for i in range(1, vS.N + 1):
            #           Laplacian
            self.lap[self.kprm, i, 1] += 6 * self.u[i, 2]
            self.lap[self.kprm, 1, i] += 6 * self.u[2, i]
            self.lap[self.kprm, i, vS.N] += 6 * self.u[i, vS.N - 1]
            self.lap[self.kprm, vS.N, i] += 6 * self.u[vS.N - 1, i]

            #        Variable Diffusion Term
            self.dudDu[self.kprm, i, 1] += 0
            self.dudDu[self.kprm, 1, i] += 0
            self.dudDu[self.kprm, i, vS.N] += 0
            self.dudDu[self.kprm, vS.N, i] += 0


        return
    

    # --------------------------------------------------------------------------
    #                        Return current state of reaction
    # --------------------------------------------------------------------------

    def getColors(self):
        # Create colors using u and v
        
        if self.obstacleMode == 0 or self.obstacleMode == 1: # No obstacle includes the inhibitor tail
            #return (self.u/np.max(self.u)) + self.v
            return (self.u/vS.uExcited) + 0.2 * self.phi / vS.phi + self.v
        else: # Obstacle is present
            return (self.u/np.max(self.u)) + 0.5 * (self.Du / vS.D)

    # --------------------------------------------------------------------------
    #                               Experiments
    # --------------------------------------------------------------------------

    def trial(self):

        # Evolve the wave until it reaches the end of the reaction space or it dies
        #
        #

        self.reset()

        wee = 0
        looking = True
        while looking:  # update until wave reaches the end of the reaction space
            for i in range(0, vS.L):
                if self.u[i, vS.N - 1] > 0.6:
                    looking = False
            self.step()
            wee += 1

            if wee > 20 * vS.N:  # If there is no wave
                print('Took too long! mass =', vS.m)
                break

        return


