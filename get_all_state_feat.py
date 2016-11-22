from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from random import randint as randi
import os

def get_all_feats(data_dir):
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()

	file_1 = open(data_dir+"/all_closest_three_of_each_class.txt", 'w')
	file_2 = open(data_dir+"/all_dist.txt", 'w')
	file_3 = open(data_dir+"/all_dist_onehot.txt", 'w')
	file_4 = open(data_dir+"/all_angle_dist_onehot.txt", 'w')
		
	for row in range(grid.grid_dims['rows']):
		for col in range(grid.grid_dims['cols']):
			# pass tuple of (row, col)
			curr_feats_closest_three_of_each_class = grid.get_feat_at_state_closest_three_of_each_class((row, col))
			curr_feats_dist = grid.get_feat_at_state_dist_no_onehot((row, col), no_of_closest_obstacles=5)
			curr_feats_dist_onehot = grid.get_feature_at_state_dist_onehot((row, col), no_of_closest_obstacles=5)
			curr_feats_angle_dist_onehot = grid.get_feature_at_state_angle_dist_onehot((row, col), no_of_closest_obstacles=5)

			file_1.write(str(row)+" "+str(col)+" ")
			file_1.write(' '.join(str(each_feat) for each_feat in curr_feats_closest_three_of_each_class))
			file_1.write("\n")

			file_2.write(str(row)+" "+str(col)+" ")
			file_2.write(' '.join(str(each_feat) for each_feat in curr_feats_dist))
			file_2.write("\n")			

			file_3.write(str(row)+" "+str(col)+" ")
			file_3.write(' '.join(str(each_feat) for each_feat in curr_feats_dist_onehot))
			file_3.write("\n")

			file_4.write(str(row)+" "+str(col)+" ")
			file_4.write(' '.join(str(each_feat) for each_feat in curr_feats_angle_dist_onehot))
			file_4.write("\n")
	file_1.close()
	file_2.close()
	file_3.close()
	file_4.close()

def save_only_obstacle_locs(data_dir):
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()
	grid.plot_obstacles(filename=data_dir+"/obstacles_only.png")

def dump_reward_to_file(data_dir):
	file = open(data_dir+"/grid.pkl",'rb')
	grid = pkl.load(file)
	file.close()
	# print(np.array2string(grid.reward, separator=', '))
	np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # turn off summarization, line-wrapping
	file = open(data_dir+"/reward.txt", 'w')
	# np.savetxt(file,grid.reward, fmt='%1.4e')
	np.savetxt(file,grid.reward, fmt='%1.1f')
	# with open(file, 'w') as f:
		# f.write(np.array2string(grid.reward, separator=', '))

if __name__ == "__main__":
	no_of_gridworlds = 10

	for idx in range(10):
		print idx
		curr_data_dir = "data/"+str(idx).zfill(len(str(no_of_gridworlds)))
		get_all_feats(curr_data_dir)

	# for idx in range(10):
	# 	save_only_obstacle_locs("data/"+str(idx))
	# 	print idx

	# for idx in range(10):
	# 	print idx
	# 	dump_reward_to_file("data/"+str(idx))
