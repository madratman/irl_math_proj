from mdp import Obstacle, Gridworld
import mdp_solvers
from random import randint as randi

grid = Gridworld()

# grid.add_obstacle(Obstacle(location=(20,30), semantic_class=1, zero_out_distance=25))
# grid.add_obstacle(Obstacle(location=(60,40), semantic_class=2, zero_out_distance=20))
# grid.add_obstacle(Obstacle(location=(70,85), semantic_class=1, zero_out_distance=30))

dim_y = grid.grid_dims['rows']
dim_x = grid.grid_dims['cols']
no_of_obstacles = 10
for i in range(no_of_obstacles):
	grid.add_obstacle(Obstacle(location=(randi(0,dim_y-1),randi(0,dim_x-1)),
						 semantic_class=1, zero_out_distance=25))

semantic_obstacle_weights = {}
semantic_obstacle_weights.update({1:0.5})
semantic_obstacle_weights.update({2:2})
semantic_obstacle_weights.update({3:4})

grid.add_semantic_obstacle_weights(semantic_obstacle_weights)
grid.make_simple_cost_function()
# grid.plot_cost_function_2d()
grid.plot_cost_function_3d()
