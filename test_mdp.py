from mdp import Obstacle, Gridworld

grid = Gridworld()

grid.add_obstacle(Obstacle(location=[20,30], semantic_class=1, zero_out_distance=25))
grid.add_obstacle(Obstacle(location=[60,40], semantic_class=2, zero_out_distance=20))
grid.add_obstacle(Obstacle(location=[70,85], semantic_class=1, zero_out_distance=30))

semantic_obstacle_weights = {}
semantic_obstacle_weights.update({1:0.5})
semantic_obstacle_weights.update({2:2})
semantic_obstacle_weights.update({3:4})

grid.add_semantic_obstacle_weights(semantic_obstacle_weights)
grid.make_simple_cost_function()
grid.plot_cost_function_2d()
grid.plot_cost_function_3d()