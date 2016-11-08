import numpy as np
import heapq

# adapted from http://www.redblobgames.com/pathfinding/a-star/implementation.html
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic_func(curr_point, target_point, type="manhattan"):
	# curr_point and target point are lists [x1,y1], [x2,y2]
	if type=="manhattan":
		return abs(curr_point[0]-target_point[0]) + abs(curr_point[1]-target_point[1])
	elif type=="euclidean":
		return numpy.linalg.norm(np.array(curr_point), np.array(target_point))

def a_star(grid, start_point, goal_point):
	# grid is obj of class Gridworld. start_point and goal_point are lists [x,y]
	frontier = PriorityQueue()
	frontier.put(start_point,0)
	came_from = {}
	cost_so_far = {}
	came_from[start_point] = None
	cost_so_far[start_point] = 0

	while not frontier.empty():
		curr_point = frontier.get()

		if curr_point==goal_point:
			break

		for next_point in grid.get_children(curr_point):
			new_cost = cost_so_far[curr_point] + grid.get_cost_at_point(next_point)
			if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
				cost_so_far[next_point] = new_cost
				priority = new_cost + heuristic_func(next_point, goal_point)
				frontier.put(next_point, priority)
				came_from[next_point] = curr_point

	return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def value_iteration(grid, thresh=0.01, max_iter=100):
	value_func = np.zeros([grid.grid_dims['y'], grid.grid_dims['x']]) #1d array
	reward = grid.cost_function #2d array
	ctr=0
	delta=float("inf")
	while delta>thresh and ctr<max_iter:
		delta = 0
		for state_idx in range(value_func.size):
			# convert to 2D indices from 1D
			state_idx_2d = np.unravel_index(state_idx, (grid.grid_dims['y'], grid.grid_dims['x']))
			old_value = value_func[state_idx_2d]
			successor_states = grid.get_children(state_idx_2d)
			# bellman backup 
			value_func[state_idx_2d] = max(map(lambda x:reward[x]+(grid.discount*value_func[x]), successor_states))
			delta = max(delta, abs(old_value - value_func[state_idx_2d]))
		ctr+=1
		print ctr
	return value_func