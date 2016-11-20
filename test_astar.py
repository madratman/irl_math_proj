from mdp import Obstacle, Gridworld
import mdp_solvers
from random import randint as randi
import pickle as pkl 

# grid = Gridworld(grid_dims=(100,100), connectivity="eight_conn", discount=0.98)
# n_rows, n_cols = grid.grid_dims['rows'], grid.grid_dims['cols']

# # specify an obstacle dict in the form {semantic_class_index, number_of_obstacles to add of that class}
# obstacles_dict = {1:5, 2:20, 3:45}
# # specify the zero_out_distanceeo	s in the form {semantic_class_index, zero_out_distance of that class}
# zero_out_dist_dict = {1:10, 2:30, 3:10}
# # declare how much to weigh each obstacle of each class in the form {semantic_class_index, weight of obstacke of that class}
# semantic_obstacle_weights= {1:25, 2:17.5, 3:15}
# grid.add_semantic_obstacle_weights(semantic_obstacle_weights)

# # add the obstacles to the grid object
# for semantic_class_index, no_of_obstacles in obstacles_dict.iteritems():
# 	for obstacle_idx in range(no_of_obstacles):
# 		grid.add_obstacle(Obstacle(location=(randi(0,n_rows-1),randi(0,n_cols-1)),
# 								   semantic_class=semantic_class_index, 
# 								   zero_out_distance=zero_out_dist_dict[semantic_class_index]))
# grid.make_simple_cost_function()

file = open("data/grid.pkl",'rb')
grid = pkl.load(file)
file.close()
print "a_star begin"
start_point = (25, 25)
goal_point = (40, 40)
final_path = mdp_solvers.a_star_fast(grid, start_point, goal_point)
# came_from, cost_so_far = mdp_solvers.a_star(grid, start_point, goal_point)
# final_path = mdp_solvers.reconstruct_path(came_from, start_point, goal_point)
print "a_star done"


import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111)

# final_path = tuple([[coord/100. for coord in point] for point in final_path]) 
grid.plot_cost_function_2d(show_plot=0)
plt.plot([point[1] for point in final_path], [point[0] for point in final_path], 'ro')
plt.show()
