from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from random import randint as randi

grid = Gridworld()
dim_y = grid.grid_dims['y']
dim_x = grid.grid_dims['x']
no_of_obstacles = 35
for i in range(no_of_obstacles):
	grid.add_obstacle(Obstacle(location=(randi(0,dim_y-1),randi(0,dim_x-1)),
						 semantic_class=1, zero_out_distance=25))


semantic_obstacle_weights = {}
semantic_obstacle_weights.update({1:5})
semantic_obstacle_weights.update({2:2})

# grid.add_goal((40,40))

grid.add_semantic_obstacle_weights(semantic_obstacle_weights)
grid.make_simple_cost_function()
grid.plot_cost_function_2d()

opt_val_func = mdp_solvers.value_iteration(grid)
final_value_plot = plt.imshow(opt_val_func)
ax = plt.subplot(111)
ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
# plt.show()
plt.axis('off')
plt.savefig('plots/value_iteration.png', bbox_inches='tight')
np.save('data/opt_val_func.npy', opt_val_func)

file = open("data/grid.pkl","wb")
pkl.dump(grid,file)
file.close()

open