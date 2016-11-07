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
grid.plot_cost_function_2d()
# grid.plot_cost_function_3d()

print "a_star begin"
start_point = (1, 4)
goal_point = (10, 14)
came_from, cost_so_far = mdp_solvers.a_star(grid, start_point, goal_point)
print "astart done"

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    # path.append(start) # optional
    path.reverse() # optional
    return path

final_path = reconstruct_path(came_from, start_point, goal_point)

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