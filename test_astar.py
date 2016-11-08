from mdp import Obstacle, Gridworld
import mdp_solvers

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

print "a_star begin"
start_point = (1, 1)
goal_point = (25, 25)
came_from, cost_so_far = mdp_solvers.a_star(grid, start_point, goal_point)
print "astart done"

final_path = mdp_solvers.reconstruct_path(came_from, start_point, goal_point)

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111)

codes = [Path.MOVETO]
for i in range(len(final_path)-1):
	codes.append(Path.LINETO)

final_path = tuple([[coord/100. for coord in point] for point in final_path]) 
plt.plot([point[0] for point in final_path], [point[1] for point in final_path], 'ro')
plt.show()
