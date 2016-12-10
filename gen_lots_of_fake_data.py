from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from random import randint as randi
import os

def make_grid(data_dir, obstacles_dict, zero_out_dist_dict, semantic_obstacle_weights):
	# create object of grid_dims=(no_of_rows, no_of_cols), "four_conn" or "eight_conn", discount
	# grid = Gridworld(grid_dims=(100,100), connectivity="eight_conn", discount=0.98)
	# n_rows, n_cols = grid.grid_dims['rows'], grid.grid_dims['cols']

	# # add this info to the grid object
	# grid.add_semantic_obstacle_weights(semantic_obstacle_weights)

	# # add the obstacles to the grid object
	# for semantic_class_index, no_of_obstacles in obstacles_dict.iteritems():
	# 	for obstacle_idx in range(no_of_obstacles):
	# 		grid.add_obstacle(Obstacle(location=(randi(0,n_rows-1),randi(0,n_cols-1)),
	# 								   semantic_class=semantic_class_index, 
	# 								   zero_out_distance=zero_out_dist_dict[semantic_class_index]))

	# # make cost function and save it to plots/cost_function.png.
	plt.close()
	# grid.make_simple_cost_function()
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()

	grid.plot_cost_function_2d(show_plot=0, filename=data_dir+"/costmap.png")
	grid.plot_obstacles(filename=data_dir+"/obstacles.png")
	plt.close()
	grid.plot_obstacles(filename=data_dir+"/obstacles_only.png")

	# save grid object
	# file = open(data_dir+"/grid.pkl","wb")
	# pkl.dump(grid,file)
	# file.close()

def do_value_iteration(data_dir):
	# load grid file generated from test_value_iteration.py
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()

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
		if not os.path.exists(data_dir+"/features"):
			os.makedirs(data_dir+"/features")
		file = open(data_dir+"/features/traj_"+str(ctr)+'.txt', 'w')
		for idx, state_feat in enumerate(curr_traj_feats):
			file.write(str(curr_traj[idx][0])+" "+str(curr_traj[idx][1])+" ")
			file.write(' '.join(str(each_feat) for each_feat in state_feat))
			file.write("\n")
		file.close()
		if ctr%5==0:
			print ctr
		ctr+=1

	plt.savefig(data_dir+'/fake_experts.png', bbox_inches='tight')
	plt.close()

def gen_astar(data_dir, no_of_fake_traj=1):
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()
	plt.close()
	# ax = plt.gca()
	ax = plt.subplot(111)
	grid.plot_cost_function_2d(show_plot=0)
	
	# start_point_list = []
	# goal_point_list = []

	# start_point_list.append((20, 20)) 
	# goal_point_list.append((50, 50))

	# start_point_list.append((50, 50)) 
	# goal_point_list.append((80, 80))

	# start_point_list.append((20, 80)) 
	# goal_point_list.append((50, 50))

	# start_point_list.append((80, 20)) 
	# goal_point_list.append((50, 50))

	# start_point_list.append((20, 80)) 
	# goal_point_list.append((80, 80))

	# start_point_list.append((80, 20)) 
	# goal_point_list.append((80, 80))

	# start_point_list.append((20, 20)) 
	# goal_point_list.append((20, 80)) 

	# start_point_list.append((20, 20)) 
	# goal_point_list.append((80, 20))

	# start_point_list.append((20, 50)) 
	# goal_point_list.append((50, 50))

	# start_point_list.append((50, 20)) 
	# goal_point_list.append((50, 50))

	for idx in range(no_of_fake_traj):
		start_point = (randi(0, grid.grid_dims['rows']-1), randi(0, grid.grid_dims['cols']-1))
		goal_point = (randi(0, grid.grid_dims['rows']-1), randi(0, grid.grid_dims['cols']-1))
		print data_dir, ", traj", idx, "of", no_of_fake_traj, ", start:", start_point, "goal:", goal_point

		came_from, cost_so_far = mdp_solvers.a_star(grid, start_point, goal_point)
		curr_traj = mdp_solvers.reconstruct_path(came_from, start_point, goal_point)
		# came_from, cost_so_far = mdp_solvers.a_star(grid, start_point_list[idx], goal_point_list[idx])
		# curr_traj = mdp_solvers.reconstruct_path(came_from, start_point_list[idx], goal_point_list[idx])
		# curr_traj = mdp_solvers.a_star_fast(grid, start_point, goal_point)
		# print "a_star done"
		if not os.path.exists(data_dir+"/features/closest_three_of_each_class"):
			os.makedirs(data_dir+"/features/closest_three_of_each_class")
		if not os.path.exists(data_dir+"/features/dist"):
			os.makedirs(data_dir+"/features/dist")
		if not os.path.exists(data_dir+"/features/dist_onehot"):
			os.makedirs(data_dir+"/features/dist_onehot")	
		if not os.path.exists(data_dir+"/features/angle_dist_onehot"):
			os.makedirs(data_dir+"/features/angle_dist_onehot")			

		file_1 = open(data_dir+"/features/closest_three_of_each_class/a_star_traj_"+str(idx).zfill(len(str(no_of_fake_traj)))+'.txt', 'w')
		file_2 = open(data_dir+"/features/dist/a_star_traj_"+str(idx).zfill(len(str(no_of_fake_traj)))+'.txt', 'w')
		file_3 = open(data_dir+"/features/dist_onehot/a_star_traj_"+str(idx).zfill(len(str(no_of_fake_traj)))+'.txt', 'w')
		file_4 = open(data_dir+"/features/angle_dist_onehot/a_star_traj_"+str(idx).zfill(len(str(no_of_fake_traj)))+'.txt', 'w')
		
		for idx in range(len(curr_traj)):
			curr_feats_closest_three_of_each_class = grid.get_feat_at_state_closest_three_of_each_class(curr_traj[idx])
			curr_feats_dist = grid.get_feat_at_state_dist_no_onehot(curr_traj[idx], no_of_closest_obstacles=5)
			curr_feats_dist_onehot = grid.get_feature_at_state_dist_onehot(curr_traj[idx], no_of_closest_obstacles=5)
			curr_feats_angle_dist_onehot = grid.get_feature_at_state_angle_dist_onehot(curr_traj[idx], no_of_closest_obstacles=5)

			file_1.write(str(curr_traj[idx][1])+" "+str(curr_traj[idx][0])+" ")
			file_1.write(' '.join(str(each_feat) for each_feat in curr_feats_closest_three_of_each_class))
			file_1.write("\n")

			file_2.write(str(curr_traj[idx][1])+" "+str(curr_traj[idx][0])+" ")
			file_2.write(' '.join(str(each_feat) for each_feat in curr_feats_dist))
			file_2.write("\n")			

			file_3.write(str(curr_traj[idx][1])+" "+str(curr_traj[idx][0])+" ")
			file_3.write(' '.join(str(each_feat) for each_feat in curr_feats_dist_onehot))
			file_3.write("\n")

			file_4.write(str(curr_traj[idx][1])+" "+str(curr_traj[idx][0])+" ")
			file_4.write(' '.join(str(each_feat) for each_feat in curr_feats_angle_dist_onehot))
			file_4.write("\n")

		file_1.close()
		file_2.close()
		file_3.close()
		file_4.close()

		# plot starting point as a star
		ax.plot(curr_traj[0][1], curr_traj[0][0], marker='*', markersize=10, color="green")
		# plot ending point as a star
		ax.plot(curr_traj[-1][1], curr_traj[-1][0], marker='*', markersize=10, color="red")
		# plot rest of the points and join them via lines

		figure = plt.plot([point[1] for point in curr_traj], [point[0] for point in curr_traj])
		plt.setp(figure, 'linewidth', 2.0)

	plt.gca().invert_yaxis()
	plt.savefig(data_dir+'/a_star_fake_experts.png', bbox_inches='tight')
	plt.close()

def plot_test_traj(idx, no_of_fake_traj=1):
	dir_c = '/home/ratneshmadaan/temp_2'
	from numpy import genfromtxt
	grid = Gridworld(grid_dims=(100,100), connectivity="eight_conn", discount=0.98)
	grid.cost_function = genfromtxt(dir_c+'/cost_map_'+str(idx+1)+'.csv', delimiter=',')
	grid.cost_function = -grid.cost_function
	plt.close()
	ax = plt.subplot(111)
	# http://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
	rotated = zip(*grid.cost_function[::-1])

	plt.imshow(rotated)
	# ax.imshow(grid.cost_function, extent=[0,1,0,1])
	ax.axis('off')
	# ax = plt.gca

	# for traj_idx in range(no_of_fake_traj):
	# 	start_point = (randi(0, grid.grid_dims['rows']-1), randi(0, grid.grid_dims['cols']-1))
	# 	goal_point = (randi(0, grid.grid_dims['rows']-1), randi(0, grid.grid_dims['cols']-1))
	# 	print "costmap", idx, ", traj", traj_idx, "of", no_of_fake_traj, ", start:", start_point, "goal:", goal_point

	# 	came_from, cost_so_far = mdp_solvers.a_star(grid, start_point, goal_point)
	# 	curr_traj = mdp_solvers.reconstruct_path(came_from, start_point, goal_point)
		
	# 	figure = plt.plot([point[1] for point in curr_traj], [point[0] for point in curr_traj])
	# 	plt.setp(figure, 'linewidth', 2.0, color='w')
	# 	ax.plot(curr_traj[0][1], curr_traj[0][0], marker='*', markersize=15, color="green")
	# 	ax.plot(curr_traj[-1][1], curr_traj[-1][0], marker='*', markersize=15, color="red")

	plt.gca().invert_xaxis()
	# plt.savefig(str(idx)+'_a_star_fake_experts.png', bbox_inches='tight')
	plt.savefig(str(idx)+'_costmap.png', bbox_inches='tight')
	plt.close()

def recompute_single_feature_thanks_to_bug(data_dir, no_of_fake_traj=1):
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()
	plt.close()
	# ax = plt.gca()
	ax = plt.subplot(111)
	grid.plot_cost_function_2d(show_plot=0)

	for idx in range(no_of_fake_traj):
		file_done = data_dir+"/features/dist/a_star_traj_"+str(idx).zfill(len(str(no_of_fake_traj)))+'.txt'
		list_of_lists = []
		
		with open(file_done) as f:
		    for line in f:
		        inner_list = [elt.strip() for elt in line.split(' ')]
		        list_of_lists.append(inner_list)
		
		curr_traj = []
		for listicle in list_of_lists:
			# file is x,y. but state is (y,x) or (row, col)
			curr_traj.append((int(listicle[1]), int(listicle[0]))) 
			
		if not os.path.exists(data_dir+"/features/final"):
			os.makedirs(data_dir+"/features/final")			

		file_4 = open(data_dir+"/features/final/a_star_traj_"+str(idx).zfill(len(str(no_of_fake_traj)))+'.txt', 'w')
		
		for idx in range(len(curr_traj)):
			curr_feat = grid.get_feature_at_state_dist_onehot(curr_traj[idx], no_of_closest_obstacles=5)

			file_4.write(str(curr_traj[idx][1])+" "+str(curr_traj[idx][0])+" ")
			file_4.write(' '.join(str(each_feat) for each_feat in curr_feat))
			file_4.write("\n")

		file_4.close()

if __name__ == "__main__":
	# specify an obstacle dict in the form {semantic_class_index, number_of_obstacles to add of that class}
	obstacles_dict = {1:15, 2:15, 3:15}
	# specify the zero_out_distanceeo	s in the form {semantic_class_index, zero_out_distance of that class}
	zero_out_dist_dict = {1:20, 2:15, 3:25}
	# declare how much to weigh each obstacle of each class in the form {semantic_class_index, weight of obstacke of that class}
	semantic_obstacle_weights= {1:0.6, 2:0.4, 3:0.2}

	no_of_gridworlds = 10

	make_grid( "data/"+str(8).zfill(len(str(no_of_gridworlds))),obstacles_dict, zero_out_dist_dict, semantic_obstacle_weights)
	# for idx in range(no_of_gridworlds):
		# curr_data_dir = "data/"+str(idx).zfill(len(str(no_of_gridworlds)))
		# if not os.path.exists(curr_data_dir):
		# 	os.makedirs(curr_data_dir)
		# do_value_iteration(curr_data_dir)
		# gen_traj_from_val_func(curr_data_dir, no_of_fake_traj=500, traj_length_limits=(50,200))
		# gen_astar(curr_data_dir, no_of_fake_traj=35)
		# recompute_single_feature_thanks_to_bug(curr_data_dir, no_of_fake_traj=35)
		# plot_test_traj(idx, no_of_fake_traj = 5)

	no_of_gridworlds_test = 5
	obstacles_dict_test = {1:5, 2:5, 3:5}
	zero_out_dist_dict_test = {1:20, 2:15, 3:25}
	semantic_obstacle_weights_test = {1:0.6, 2:0.4, 3:0.2}

	# for idx in range(no_of_gridworlds_test):
		# curr_data_dir = "data_test/"+str(idx).zfill(len(str(no_of_gridworlds_test)))
	# 	if not os.path.exists(curr_data_dir):
	# 		os.makedirs(curr_data_dir)
		# make_grid(curr_data_dir, obstacles_dict_test, zero_out_dist_dict_test, semantic_obstacle_weights_test)

	# 	print idx