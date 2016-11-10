import mdp_solvers
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt

file = open("data/grid.pkl",'rb')
grid = pkl.load(file)
file.close()

opt_val_func = np.load('data/opt_val_func.npy')
plt.imshow(opt_val_func)
ax = plt.subplot(111)
ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
# plt.show()
plt.axis('off')

all_traj = mdp_solvers.gen_fake_expert_traj(grid, opt_val_func,
						no_of_fake_traj=50, traj_length_limits=(500,1000))
for each_traj in all_traj:
	print len(each_traj)
	# plot starting point
	ax.plot(each_traj[0][0], each_traj[0][1], marker='*', markersize=20, color="white")
	figure = plt.plot([point[0] for point in each_traj], [point[1] for point in each_traj])
	plt.setp(figure, 'linewidth', 3.0)
	
plt.show()
