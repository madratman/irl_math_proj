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

class Node:
    def __init__(self, point):
        # self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

def a_star_fast(grid, start_point, goal_point):
	# http://stackoverflow.com/questions/4159331/python-speed-up-an-a-star-pathfinding-algorithm
	# https://gist.github.com/jamiees2/5531924s
	open_set = set()
	closed_set = set()
	open_heap = []

	def retrace_path(c):
		path = [c.point]
		while c.parent is not None:
			c = c.parent
			path.append(c.point)
		path.reverse
		return path

	curr_point = start_point
	open_set.add(curr_point)
	open_heap.append((0,curr_point))
	ctr = 0
	while open_set:
		ctr += 1
		if not ctr%5000:
			print ctr
		# by popping heap, we're finding the element in the openset with lowest G+H
		curr_point = heapq.heappop(open_heap)[1]
		# print curr_point.point
		if curr_point == goal_point:
			return retrace_path(curr_point)	
		
		# remove from open set and add to closed
		open_set.remove(curr_point)
		closed_set.add(curr_point)

		for child in grid.get_children(curr_point):
			# node = Node(child)

			# if already in closed set, we skip it
			if curr_point in closed_set:
				continue

			# else if it's in open, check if we beat the G score 	
			if curr_point in open_set:
				new_g = curr_point.G + grid.get_cost_at_point(curr_point)
				if node.G > new_g:
					node.G = new_g
					node.parent = curr_point
			else:
				node.G = curr_point.G + grid.get_cost_at_point(node.point)
				node.H = heuristic_func(node.point, goal_point.point)
				node.parent = curr_point
				open_set.add(node)
				heapq.heappush(open_heap, (node.G+node.H, node))

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# todo add as member of mdp class?
def value_iteration(grid, thresh=0.01, max_iter=100):
	value_func = np.zeros([grid.grid_dims['rows'], grid.grid_dims['cols']]) #1d array
	reward = grid.reward #2d array
	ctr=0
	delta=float("inf")
	while delta>thresh and ctr<max_iter:
		delta = 0
		for state_idx in range(value_func.size):
			# convert to 2D indices from 1D
			state_idx_2d = np.unravel_index(state_idx, (grid.grid_dims['rows'], grid.grid_dims['cols']))
			old_value = value_func[state_idx_2d]
			successor_states = grid.get_children(state_idx_2d)
			# bellman backup 
			#todo
			# value_func[state_idx_2d] = max(map(lambda x:reward[x]+(grid.discount*value_func[x]), successor_states))
			value_func[state_idx_2d] = reward[state_idx_2d]+max(map(lambda x:(grid.discount*value_func[x]), successor_states))
			delta = max(delta, abs(old_value - value_func[state_idx_2d]))
		ctr+=1
		if not ctr%10:
			print "ctr=", ctr, "delta=",delta
	return value_func

def gen_fake_expert_traj(grid, value_func, no_of_fake_traj, add_state_itself=0, traj_length_limits=(100,100)):
	from random import randint as randi
	import operator
	all_traj = []

	for traj_idx in range(no_of_fake_traj):
		# starting point of each trajectory is random
		curr_point = (randi(0, grid.grid_dims['rows']-1), randi(0, grid.grid_dims['cols']-1))
		# length of traj is random, between the limits specified in the argument traj_length_limits
		traj_length = randi(traj_length_limits[0], traj_length_limits[1])
		curr_traj = []

		# we keep on appending the next point with highest value amongst it's neighbours
		# TODO this might lead to stupid trajectories that keep on looping
		for pt_idx in range(traj_length):
			curr_traj.append(curr_point)
			# get the neighbours of curr_point
			successor_states = grid.get_children(curr_point)
			# add curr point to stop
			if add_state_itself:
				successor_states.append(curr_point)
			# get value for each neighbouring states
			successor_values = map(lambda x:grid.get_reward_at_point(x), successor_states)
			# find max value. not we need the index of the neifghbouring states 
			max_index, max_value = max(enumerate(successor_values), key=operator.itemgetter(1))
			# print "successor_values", successor_values
			# print "max_index", max_index, "max_value", max_value, "\n"
			curr_point = successor_states[max_index]
			successor_states, successor_values, max_value, max_index = ([] for i in range(4))

			# print curr_point, max_value

		all_traj.append(curr_traj)

	return all_traj

# def plot_traj(list_of_traj):
