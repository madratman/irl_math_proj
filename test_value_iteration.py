from mdp import Obstacle, Gridworld
import mdp_solvers
import matplotlib.pyplot as plt

grid = Gridworld()

grid.add_obstacle(Obstacle(location=(20,30), semantic_class=1, zero_out_distance=25))
grid.add_obstacle(Obstacle(location=(60,40), semantic_class=2, zero_out_distance=20))
grid.add_obstacle(Obstacle(location=(70,85), semantic_class=1, zero_out_distance=30))

semantic_obstacle_weights = {}
semantic_obstacle_weights.update({1:0.5})
semantic_obstacle_weights.update({2:2})
semantic_obstacle_weights.update({3:4})

grid.add_semantic_obstacle_weights(semantic_obstacle_weights)
grid.make_simple_cost_function()

final_value = mdp_solvers.value_iteration(grid)
final_value_plot = plt.imshow(final_value)
ax = plt.subplot(111)
ax.imshow(final_value, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
plt.show()