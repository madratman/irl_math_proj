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
	def __init__(self, grid_dims=(100,100), connectivity="four_conn", discount=0.98):		
		self.grid_dims = {'rows':grid_dims[0], 'cols':grid_dims[1]}
		self.connectivity = connectivity
		self.obstacles = []
		self.semantic_obstacle_weights = {} #todo add default or make param?
		self.cost_function = []
		self.reward = []
		self.discount = discount
		self.goals = []

	def add_obstacle(self, obstacle):
		# pass objects of Obstacle class
		self.obstacles.append(obstacle)

	def add_semantic_obstacle_weights(self,weight_dict):
		# pass something like {1:w_1, 2:w_2, 3:w_3....}
		self.semantic_obstacle_weights = weight_dict

	def make_simple_cost_function(self):
		cost_iter_arr = np.zeros([self.grid_dims['rows'], self.grid_dims['cols']])
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
		self.reward = -obs_cost
		for goal in self.goals:
			self.reward[goal]=5

	def get_cost_at_point(self, point):
		# we'll use this function in MDP solvers like A-star
		return self.cost_function[point]

	def get_reward_at_point(self, point):
		return self.reward[point]

	def plot_cost_function_2d(self, show_plot=0, **kwargs):
		cost_2d_plot = plt.imshow(self.cost_function)
		ax = plt.subplot(111)
		ax.imshow(self.cost_function, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
		if show_plot:
			plt.show()
		else:
			plt.axis('off')
			if ('filename' in kwargs):
				plt.savefig(kwargs['filename'], bbox_inches='tight')
			else:
				plt.savefig('plots/costmap.png', bbox_inches='tight')

	def plot_cost_function_3d(self):
		cost_3d_plot = plt.figure()
		ax = cost_3d_plot.add_subplot(111, projection='3d')
		nx, ny = (self.grid_dims['cols'], self.grid_dims['rows'])
		x = np.linspace(0, 1.0, nx)
		y = np.linspace(0, 1.0, ny)
		X,Y = np.meshgrid(x, y)
		# print X.shape, Y.shape, self.cost_function.shape
		ax.plot_surface(X, Y, self.cost_function, cmap = cm.coolwarm)
		plt.show()

	def plot_obstacles(self, **kwargs):
		# fig = plt.figure()
		# ax = fig.add_subplot(111)
		# cost_2d_plot = plt.imshow(self.cost_function)
		ax = plt.subplot(111)
		# ax.imshow(self.cost_function, extent=[0,1,0,1], aspect='auto') # this has been transposed in the math hw
		class_color_mapping = {1:"red", 2:"orange", 3:"green"}
		# plt.xticks(np.arange(0, self.grid_dims['cols'], self.grid_dims['cols']/5))
		# plt.yticks(np.arange(0, self.grid_dims['rows'], self.grid_dims['rows']/5))
		for obstacle in self.obstacles:
			plt.plot(obstacle.location[1], obstacle.location[0], marker='*', markersize=20, color=class_color_mapping[obstacle.semantic_class])
		plt.axis('off')
		ax = plt.gca()
		ax.invert_yaxis()
		if ('filename' in kwargs):
			plt.savefig(kwargs['filename'], bbox_inches='tight')
		else:
			plt.savefig('plots/obstacles.png', bbox_inches="tight")
		plt.close()

	def get_children(self, point):
		# point is list [x,y]
		children_list = []
		if self.connectivity=="four_conn":
			indices = [[1,0],[0,1],[-1,0],[0,-1]]
			for index in indices:
				curr_child = (point[0]+index[0], point[1]+index[1])
				if 0<=curr_child[0]<self.grid_dims['rows'] and 0<=curr_child[1]<self.grid_dims['cols']:
					children_list.append(curr_child)
		if self.connectivity=="eight_conn":
			indices = [[1,0],[0,1],[-1,0],[0,-1], [1,1],[-1,1],[1,-1],[-1,-1]]
			for index in indices:
				curr_child = (point[0]+index[0], point[1]+index[1])
				if 0<=curr_child[0]<self.grid_dims['rows'] and 0<=curr_child[1]<self.grid_dims['cols']:
					children_list.append(curr_child)
		return children_list

	def add_goal(self, location):
		self.goals.append(location)

	def get_feat_vect_at_state(self, state_location):
		# for each obstacle in the grid object, find the euclidean distance from state_location
		obs_dist_list = [np.linalg.norm(np.asarray(state_location)-np.asarray(each_obs.location)) for each_obs in self.obstacles]
		# find the class of each obstacle
		obs_class_list = [each_obs.semantic_class for each_obs in self.obstacles]
		# sort the list which contains the distances
		sorted_obs_dist = sorted(obs_dist_list)
		sorted_classes = [obs_class for (obs_dist, obs_class) in sorted(zip(obs_dist_list, obs_class_list))]
		
		# find closest obstacles' indices of each class
		# http://codereview.stackexchange.com/questions/24126/retrieving-the-first-occurrence-of-every-unique-value-from-a-csv-column
	 	temp_dict = {obs_class:idx for idx,obs_class in reversed(list(enumerate(sorted_classes)))}
	 	indices = temp_dict.values() 
	 	feature_vector = [sorted_obs_dist[index] for index in indices]
	 	return feature_vector

	def get_feat_vect_traj(self, trajectory):
		all_feats = []
		for idx in range(len(trajectory)):
			curr_feature = self.get_feat_vect_at_state(trajectory[idx])
			all_feats.append(curr_feature)
		return all_feats