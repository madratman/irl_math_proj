import matplotlib.pyplot as plt
import pickle as pkl
import argparse
import os
import numpy as np

no_of_gridworlds = 10

dir_learnt_params = '' # todo

def get_reward(params_file, feat_file, **kwargs):
	params = np.loadtxt(params_file)

	print "loading features ..."
	feat_file = open(feat_file, 'rb')
	all_feats = pkl.load(feat_file)
	feat_file.close()
	print "loaded features \n"

	no_of_rows = no_of_cols = 100
	reward = np.zeros((no_of_rows, no_of_cols))

	file = open('data/00/grid.pkl')
	grid = pkl.load(file)
	file.close()
	for row in range(100):
		for col in range(100):
			reward[row,col] = np.dot(params, np.asarray(all_feats[row][col]))

	plt.imshow(reward)
	if ('idx' in kwargs):
		plt.savefig('reward_learnt_'+kwargs['idx']+'.png', bbox_inches='tight')
		np.save('reward_learnt_'+kwargs['idx']+'.npy', reward)
	else:
		plt.savefig('reward_learnt.png', bbox_inches='tight')
		np.save('reward_learnt.npy', reward)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("param_file")
	parser.add_argument("feat_file")
	args = parser.parse_args()
	cwd = os.getcwd()
	print "param_file :", os.path.join(cwd, args.param_file)
	print "feat_file :" , os.path.join(cwd, args.feat_file)

	get_reward(os.path.join(cwd, args.param_file), os.path.join(cwd, args.feat_file))

	no_of_gridworlds = 10
	# for idx in range(no_of_gridworlds) 

# for idx in range(no_of_gridworlds):
# 	print idx
# 	data_dir = "data/"+str(idx).zfill(len(str(no_of_gridworlds)))

# 	# load features
# 	file_1 = open(data_dir+"/all_closest_three_of_each_class.pkl", "rb")
# 	file_2 = open(data_dir+"/all_dist.pkl", "rb")
# 	file_3 = open(data_dir+"/all_dist_onehot.pkl", "rb")
# 	file_4 = open(data_dir+"/all_angle_dist_onehot.pkl", "rb")

# 	all_feats_closest_three_of_each_class = pkl.load(file_1)
# 	all_feats_dist = pkl.load(file_2)
# 	all_feats_dist_onehot = pkl.load(file_3)
# 	all_feats_angle_dist_onehot = pkl.load(file_4)

# 	file_1.close()
# 	file_2.close()
# 	file_3.close()
# 	file_4.close()

# 	# load learned params
# 	all_closest_three_of_each_class = np.loadtxt(data_dir+"/all_closest_three_of_each_class.txt")
# 	all_dist = np.loadtxt(data_dir+"/all_dist.txt")
# 	all_dist_onehot = np.loadtxt(data_dir+"/all_dist_onehot.txt")
# 	all_angle_dist_onehot = np.loadtxt(data_dir+"/all_angle_dist_onehot.txt")

# 	# take dot
# 	# todo vectorize. take dot of feat's "3d" array and repmat the params over each pixel in 2d grid
# 	for row in range(grid.grid_dims['rows']):
# 		temp_1 = temp_2 = temp_3 = temp_4 =[]
# 		for col in range(grid.grid_dims['cols']):
# 			reward_closest_three_of_each_class = np.dot(learnt_params[idx], all_closest_three_of_each_class[idx])
# 			reward_dist = np.dot(learnt_params[idx], all_dist[idx])
# 			reward_dist_onehot = np.dot(learnt_params[idx], all_dist_onehot[idx])
# 			reward_angle_dist_onehot = np.dot(learnt_params[idx], all_angle_dist_onehot[idx])

# 	plt.imshow(reward_closest_three_of_each_class)
# 	plt.savefig('results/closest_three_of_each_class.png', bbox_inches='tight')

# 	plt.imshow(reward_dist)
# 	plt.savefig('results/dist.png', bbox_inches='tight')
	
# 	plt.imshow(reward_dist_onehot)
# 	plt.savefig('results/reward_dist_onehot.png', bbox_inches='tight')

# 	plt.imshow(reward_angle_dist_onehot)
# 	plt.savefig('results/angle_dist_onehot.png', bbox_inches='tight')


