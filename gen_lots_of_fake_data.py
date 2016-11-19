from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from random import randint as randi

import mdp_solvers
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt


def do_value_iteration(data_dir, obstacles_dict, zero_out_dist_dict, semantic_obstacle_weights):
	# create object of grid_dims=(no_of_rows, no_of_cols), "four_conn" or "eight_conn", discount
	grid = Gridworld(grid_dims=(100,100), connectivity="eight_conn", discount=0.98)
	n_rows, n_cols = grid.grid_dims['rows'], grid.grid_dims['cols']

	# add this info to the grid object
	grid.add_semantic_obstacle_weights(semantic_obstacle_weights)

	# add the obstacles to the grid object
	for semantic_class_index, no_of_obstacles in obstacles_dict.iteritems():
		for obstacle_idx in range(no_of_obstacles):
			grid.add_obstacle(Obstacle(location=(randi(0,n_rows-1),randi(0,n_cols-1)),
									   semantic_class=semantic_class_index, 
									   zero_out_distance=zero_out_dist_dict[semantic_class_index]))

	# make cost function and save it to plots/cost_function.png.
	grid.make_simple_cost_function()
	# solve the grid mdp with obstacles with value iteration
	opt_val_func = mdp_solvers.value_iteration(grid,thresh=0.00001, max_iter=400)

	# plot and save the final values 
	final_value_plot = plt.imshow(opt_val_func)
	ax = plt.subplot(111)
	ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
	# plt.show()
	plt.axis('off')
	plt.savefig(data_dir+'/value_iteration.png', bbox_inches='tight')

	# save opt_val_func data so that we don't have to cmpute it again and again
	np.save(data_dir+'/opt_val_func.npy', opt_val_func)

	# save grid object
	file = open(data_dir+"/grid.pkl","wb")
	pkl.dump(grid,file)
	file.close()

def gen_traj_from_val_func(data_dir, no_of_fake_traj=100, traj_length_limits=(100,1000)):
	# load grid file generated from test_value_iteration.py
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()
	grid.plot_cost_function_2d(show_plot=0, filename=data_dir+"/costmap.png")
	grid.plot_obstacles(filename=data_dir+"/obstacles.png")

	# load and plot opt value funciton generated from test_value_iteration.py
	opt_val_func = np.load(data_dir+'/opt_val_func.npy')
	plt.imshow(opt_val_func)
	ax = plt.subplot(111)
	ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
	# plt.show()
	plt.axis('off')

	# generate fake trajectories of "no_of_fake_traj" in number. specify minimum and maximum length via the traj_length_limits tuple
	# note that mdp_solvers.gen_fake_expert_traj will choose a random starting point and random length of the synthetic expert traj 
	# within the speified limits
	all_traj = mdp_solvers.gen_fake_expert_traj(grid, opt_val_func,
							no_of_fake_traj=no_of_fake_traj, traj_length_limits=traj_length_limits, add_state_itself=1)

	ctr=0
	for curr_traj in all_traj:
		# plot starting point as a star
		ax.plot(curr_traj[0][1], curr_traj[0][0], marker='*', markersize=10, color="white")
		# plot rest of the points and join them via lines
		figure = plt.plot([point[1] for point in curr_traj], [point[0] for point in curr_traj])
		plt.setp(figure, 'linewidth', 2.0)
		curr_traj_feats = grid.get_feat_vect_traj(curr_traj)
		file = open(data_dir+"/features/traj_"+str(ctr)+'.txt', 'w')
		for idx, state_feat in enumerate(curr_traj_feats):
			file.write(str(curr_traj[idx][0])+" "+str(curr_traj[idx][1])+" ")
			file.write(' '.join(str(each_feat) for each_feat in state_feat))
			file.write("\n")
		if ctr%5==0:
			print ctr
		ctr+=1

	plt.show()

if __name__ == "__main__":
	# specify an obstacle dict in the form {semantic_class_index, number_of_obstacles to add of that class}
	obstacles_dict = {1:5, 2:10, 3:15}
	# specify the zero_out_distanceeo	s in the form {semantic_class_index, zero_out_distance of that class}
	zero_out_dist_dict = {1:25, 2:15, 3:10}
	# declare how much to weigh each obstacle of each class in the form {semantic_class_index, weight of obstacke of that class}
	semantic_obstacle_weights= {1:25, 2:17.5, 3:15}

	for idx in range(3):
		do_value_iteration("data/"+str(idx),obstacles_dict, zero_out_dist_dict, semantic_obstacle_weights)
		gen_traj_from_val_func("data/"+str(idx))
