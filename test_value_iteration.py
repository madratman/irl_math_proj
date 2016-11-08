from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt

grid = Gridworld()

grid.add_obstacle(Obstacle(location=(20,30), semantic_class=1, zero_out_distance=25))
grid.add_obstacle(Obstacle(location=(60,40), semantic_class=2, zero_out_distance=20))
grid.add_obstacle(Obstacle(location=(70,85), semantic_class=1, zero_out_distance=30))

semantic_obstacle_weights = {}
semantic_obstacle_weights.update({1:5})
semantic_obstacle_weights.update({2:2})

# grid.add_goal((40,40))

grid.add_semantic_obstacle_weights(semantic_obstacle_weights)
grid.make_simple_cost_function()

opt_val_func = mdp_solvers.value_iteration(grid)
final_value_plot = plt.imshow(opt_val_func)
ax = plt.subplot(111)
ax.imshow(opt_val_func, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
# plt.show()
plt.axis('off')
plt.savefig('plots/value_iteration.png', bbox_inches='tight')

all_traj = mdp_solvers.gen_fake_expert_traj(grid, opt_val_func, no_of_fake_traj=10, traj_length_limits=(10,40))
for each_traj in all_traj:
	print each_traj