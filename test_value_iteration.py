from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from random import randint as randi

# create object of grid_dims=(no_of_rows, no_of_cols), "four_conn" or "eight_conn", discount
grid = Gridworld(grid_dims=(100,100), connectivity="eight_conn", discount=0.98)
n_rows, n_cols = grid.grid_dims['rows'], grid.grid_dims['cols']

# specify an obstacle dict in the form {semantic_class_index, number_of_obstacles to add of that class}
obstacles_dict = {1:5, 2:10, 3:15}
# specify the zero_out_distanceeo	s in the form {semantic_class_index, zero_out_distance of that class}
zero_out_dist_dict = {1:25, 2:15, 3:10}
# declare how much to weigh each obstacle of each class in the form {semantic_class_index, weight of obstacke of that class}
semantic_obstacle_weights= {1:25, 2:17.5, 3:15}

# add this info to the grid object
grid.add_semantic_obstacle_weights(semantic_obstacle_weights)

# add the obstacles to the grid object
for semantic_class_index, no_of_obstacles in obstacles_dict.iteritems():
	for obstacle_idx in range(no_of_obstacles):
		grid.add_obstacle(Obstacle(location=(randi(0,n_rows-1),randi(0,n_cols-1)),
								   semantic_class=semantic_class_index, 
								   zero_out_distance=zero_out_dist_dict[semantic_class_index]))

grid.add_goal((40,40))

# make cost function and save it to plots/cost_function.png.
grid.make_simple_cost_function()
grid.plot_obstacles()
grid.plot_cost_function_2d(show_plot=0)
# solve the grid mdp with obstacles with value iteration
opt_val_func = mdp_solvers.value_iteration(grid,thresh=0.00001, max_iter=400)

# plot and save the final values 
final_value_plot = plt.imshow(opt_val_func)
ax = plt.subplot(111)
ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
# plt.show()
plt.axis('off')
plt.savefig('plots/value_iteration.png', bbox_inches='tight')

# save opt_val_func data so that we don't have to cmpute it again and again
np.save('data/opt_val_func.npy', opt_val_func)

# save grid object
file = open("data/grid.pkl","wb")
pkl.dump(grid,file)
file.close()

