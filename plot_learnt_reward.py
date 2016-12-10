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
	plt.axis('off')
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
