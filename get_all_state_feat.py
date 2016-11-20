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

	file = open(data_dir+"/all_state_feats.txt", 'w')

	for row in range(grid.grid_dims['rows']):
		for col in range(grid.grid_dims['cols']):
			# pass tuple of (row, col)
			curr_feat = grid.get_feat_vect_at_state((row, col))
			file.write(str(row)+" "+str(col)+" ")
			file.write(' '.join(str(each_feat) for each_feat in curr_feat))
			file.write("\n")

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
	for idx in range(10):
		print idx
		data_dir = "data/"+str(idx)
		get_all_feats(data_dir)

	for idx in range(10):
		save_only_obstacle_locs("data/"+str(idx))
		print idx

	for idx in range(10):
		print idx
		dump_reward_to_file("data/"+str(idx))
