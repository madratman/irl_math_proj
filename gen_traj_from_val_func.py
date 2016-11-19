import mdp_solvers
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt

# read and run python test_value_iteration before running this file. 

# load grid file generated from test_value_iteration.py
file = open("data/grid.pkl",'rb')
grid = pkl.load(file)
file.close()
grid.plot_cost_function_2d(show_plot=0, filename="data/0/costmap.png")
grid.plot_obstacles(filename="data/0/obstacles.png")

# load and plot opt value funciton generated from test_value_iteration.py
opt_val_func = np.load('data/opt_val_func.npy')
plt.imshow(opt_val_func)
ax = plt.subplot(111)
ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
# plt.show()
plt.axis('off')

# generate fake trajectories of "no_of_fake_traj" in number. specify minimum and maximum length via the traj_length_limits tuple
# note that mdp_solvers.gen_fake_expert_traj will choose a random starting point and random length of the synthetic expert traj 
# within the speified limits
all_traj = mdp_solvers.gen_fake_expert_traj(grid, opt_val_func,
						no_of_fake_traj=100, traj_length_limits=(100,1000), add_state_itself=0)

ctr=0
for curr_traj in all_traj:
	# plot starting point as a star
	ax.plot(curr_traj[0][1], curr_traj[0][0], marker='*', markersize=20, color="white")
	# plot rest of the points and join them via lines
	figure = plt.plot([point[1] for point in curr_traj], [point[0] for point in curr_traj])
	plt.setp(figure, 'linewidth', 3.0)
	curr_traj_feats = grid.get_feat_vect_traj(curr_traj)
	file = open("data/0/features/traj_"+str(ctr)+'.txt', 'w')
	for idx, state_feat in enumerate(curr_traj_feats):
		file.write(str(curr_traj[idx][0])+" "+str(curr_traj[idx][1])+" ")
		file.write(' '.join(str(each_feat) for each_feat in state_feat))
		file.write("\n")
	if ctr%5==0:
		print ctr
	ctr+=1

plt.show()

# save the fake expert trajectories in a file. We ll use this to recover the reward function
# file = open("data/fake_traj.pkl",'w')
# pkl.dump(all_traj, file)
# file.close()
