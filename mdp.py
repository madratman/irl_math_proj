import numpy as np 
from scipy import ndimage
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
# from __future__ import division

waypoints=300;

length_x = 100
length_y = 100

gridworld = np.zeros([length_y, length_x])

# todo make a dict and specify type of obstacle class 
obstacles = []
obstacles.append([20,30])
obstacles.append([60,40])
obstacles.append([70,85])

epsilon = [25, 20, 30]
obs_cost = np.zeros_like(gridworld)

for i in range(len(obstacles)):
	t = np.zeros_like(gridworld)	
	t[obstacles[i][0],obstacles[i][1]] = 1 # point obstacles
	# this is matlab's bwdist in python(1-t)
	# http://stackoverflow.com/questions/5260232/matlab-octave-bwdist-in-python-or-c
	t_cost = ndimage.morphology.distance_transform_edt(1-t) 
	t_cost[t_cost>epsilon[i]]= epsilon[i];
	t_cost = (1.0/(2*epsilon[i]))*((t_cost-epsilon[i])**2);
	obs_cost += t_cost

cost_2d_plot = plt.imshow(obs_cost)
ax = plt.subplot(111)
ax.imshow(obs_cost, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
plt.show()

# surface plot
cost_3d_plot = plt.figure()
ax = cost_3d_plot.add_subplot(111, projection='3d')
x = np.arange(0, length_x, 1.0)
y = np.arange(0, length_y, 1.0)
X, Y = np.meshgrid(x, y)
print X.shape, Y.shape, obs_cost.shape
ax.plot_surface(X, Y, obs_cost,cmap = cm.coolwarm)
plt.show()
