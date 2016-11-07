import numpy as np

def children(point, grid_dims, connectivity="four_conn"):
	# point is list [x,y], grid_dims is dict {x:n_1, y:n_2}
	# todo maybe it's better to have a grid data struct itself instead of passing dims
	children_list = []
	if connectivity=="four_conn":
		indices = [[1,0],[0,1],[-1,0],[0,-1]]
		for index in indices:
			curr_child = [point[0]+index[0], point[1]+index[1]]
			if 0<=curr_child[0]<grid_dims.x and 0<=curr_child[1]<grid_dims.y:
				children_list.append(curr_child)

	if connectivity=="eight_conn":
		indices = [[1,0],[0,1],[-1,0],[0,-1], [1,1],[-1,1],[1,-1],[-1,-1]]
		for index in indices:
			curr_child = [point[0]+index[0], point[1]+index[1]]
			if 0<=curr_child[0]<grid_dims.x and 0<=curr_child[1]<grid_dims.y:
				children_list.append(curr_child)

	return children_list

def heuristic_func(curr_point, target_point, type="manhattan"):
	# curr_point and target point are lists [x1,y1], [x2,y2]
	if type=="manhattan":
		return abs(curr_point[0]-target_point[0]) + abs(curr_point[1]-target_point[1])
	elif type=="euclidean":
		return numpy.linalg.norm(np.array(curr_point), np.array(target_point))

def a_star(start, goal, grid_dims):
	