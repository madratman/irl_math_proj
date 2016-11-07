import numpy as np 
from scipy import ndimage
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# from __future__ import division

class Obstacle:
	def __init__(self, location, semantic_class, zero_out_distance):
		self.location = location
		self.semantic_class = semantic_class
		self.zero_out_distance = zero_out_distance

class Gridworld:
	def __init__(self, grid_dims=[100,100], connectivity="four_conn"):		
		self.grid_dims = {'x':grid_dims[0], 'y':grid_dims[1]}
		self.connectivity = connectivity
		self.obstacles = []
		self.semantic_obstacle_weights = {} #todo add default or make param?
		self.cost_function = []

	def add_obstacle(self, obstacle):
		# pass objects of Obstacle class
		self.obstacles.append(obstacle)

	def add_semantic_obstacle_weights(self,weight_dict):
		# pass something like {1:w_1, 2:w_2, 3:w_3....}
		self.semantic_obstacle_weights = weight_dict

	def make_simple_cost_function(self):
		cost_iter_arr = np.zeros([self.grid_dims['y'], self.grid_dims['x']])
		obs_cost = np.zeros_like(cost_iter_arr)
		for i in range(len(self.obstacles)):
			cost_iter_arr[self.obstacles[i].location[0], self.obstacles[i].location[1]] = 1 # point obstacles
			# this is matlab's bwdist in python(1-t)
			# http://stackoverflow.com/questions/5260232/matlab-octave-bwdist-in-python-or-c
			cost_iter_arr = ndimage.morphology.distance_transform_edt(1-cost_iter_arr) 
			cost_iter_arr[cost_iter_arr>self.obstacles[i].zero_out_distance] = self.obstacles[i].zero_out_distance;
			cost_iter_arr = (1.0/(2*self.obstacles[i].zero_out_distance))*((cost_iter_arr-self.obstacles[i].zero_out_distance)**2);
			curr_obstacle_class = self.obstacles[i].semantic_class
			curr_semantic_class_weight = self.semantic_obstacle_weights[curr_obstacle_class]
			curr_obstacle_class *= curr_semantic_class_weight
			obs_cost += cost_iter_arr
		self.cost_function = obs_cost

	def get_cost_at_point(self, point):
		# we'll use this function in MDP solvers like A-star
		return self.cost_function[point[0], point[1]]

	def plot_cost_function_2d(self):
		cost_2d_plot = plt.imshow(self.cost_function)
		ax = plt.subplot(111)
		ax.imshow(self.cost_function, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
		plt.show()

	def plot_cost_function_3d(self):
		cost_3d_plot = plt.figure()
		ax = cost_3d_plot.add_subplot(111, projection='3d')
		x = np.arange(0, self.grid_dims['x'], 1.0)
		y = np.arange(0, self.grid_dims['y'], 1.0)
		X,Y = np.meshgrid(x, y)
		# print X.shape, Y.shape, self.cost_function.shape
		ax.plot_surface(X, Y, self.cost_function, cmap = cm.coolwarm)
		plt.show()

	def get_children(self, point):
		# point is list [x,y]
		children_list = []
		if self.connectivity=="four_conn":
			indices = [[1,0],[0,1],[-1,0],[0,-1]]
			for index in indices:
				curr_child = (point[0]+index[0], point[1]+index[1])
				if 0<=curr_child[0]<self.grid_dims['x'] and 0<=curr_child[1]<self.grid_dims['y']:
					children_list.append(curr_child)
		if self.connectivity=="eight_conn":
			indices = [[1,0],[0,1],[-1,0],[0,-1], [1,1],[-1,1],[1,-1],[-1,-1]]
			for index in indices:
				curr_child = (point[0]+index[0], point[1]+index[1])
				if 0<=curr_child[0]<self.grid_dims['x'] and 0<=curr_child[1]<self.grid_dims['y']:
					children_list.append(curr_child)
		return children_list

	# def get_feat_vect_at_pt(self, state_location):

	# def get_feat_expect_traj(self, trajectory):

