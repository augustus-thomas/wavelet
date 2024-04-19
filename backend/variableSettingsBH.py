# Written by Daniel Cohen
#
# For Senior Independent Study Thesis
# The College of Wooster
#
# Feb. 27th 2023

# Simulation parameters
# constants

def __init__():
	pass
N = 150 # Grid size, originally 81
delta = 0.1 # Boundary layer # 1e-4 originally
t = 0 # time, must start with this value
T = 30 # frame rate
# computed
L = int(N/2)
dt = L**2/(5*(N-1)**2) # Time step 0.05
h = L / (N - 1)
D = dt / h**2 # Diffusion Constant

# Chemical parameters
f = 2.5 # 3.0
q = 0.0001 # 0.001
e1 = 0.0317 #0.03
e2 = e1/500 #0.03
uExcited = 1.2 # value of excited u, initially 0.8

# Obstacle

Du = 1 # HBrO3(activator) diffusion coefficient (percentage of diffusion to use)
Dv = 1 # 0 - 1 value; catalyst diffusion coefficient (percentage of diffusion to use)
Dw = Du # Br- (inhibitor) diffusion coefficient (percentage of diffusion to use)
m = 1 # Mass of the obstacle
r = N/4 # obstacle radius
phi = 0.07
