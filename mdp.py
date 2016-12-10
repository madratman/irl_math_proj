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
			# curr_obstacle_class *= curr_semantic_class_weight
			obs_cost += cost_iter_arr*curr_semantic_class_weight
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
			plt.savefig('plots/obstacles.png', bbox_inches='tight')

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

	def get_feat_at_state_closest_three_of_each_class(self, state_location):
		# for each obstacle in the grid object, find the euclidean distance from state_location
		obs_dist_list = [np.linalg.norm(np.asarray(state_location)-np.asarray(each_obs.location)) for each_obs in self.obstacles]
		
		# find the class of each obstacle
		obs_class_list = [each_obs.semantic_class for each_obs in self.obstacles]
		
		# sort the list which contains the distances. DO NOT sort obs_dist_list before !!!
		obs_class_list = [obs_class for (obs_dist, obs_class) in sorted(zip(obs_dist_list, obs_class_list))]
		obs_dist_list = sorted(obs_dist_list)
		
		# find closest obstacles' indices of each class
		# http://codereview.stackexchange.com/questions/24126/retrieving-the-first-occurrence-of-every-unique-value-from-a-csv-column
		temp_dict = {obs_class:idx for idx,obs_class in reversed(list(enumerate(obs_class_list)))}
		indices = temp_dict.values() 
		feature_vector = [obs_dist_list[index] for index in indices]
		feature_vector = [1./((x+1)**2) for x in feature_vector] # feature is 1/(dist^2) where dist = distance from obstacle
		return feature_vector

	def get_feature_at_state_angle_dist_onehot(self, state_location, no_of_closest_obstacles=5):
		# for each obstacle in the grid object, find the euclidean distance from state_location
		obs_dist_list = [np.linalg.norm(np.asarray(state_location)-np.asarray(each_obs.location)) for each_obs in self.obstacles]
		# find the class of each obstacle
		obs_class_list = [each_obs.semantic_class for each_obs in self.obstacles]
		# state is (row,col)==(y,x) .arctan2(y2-y1,x2-x1)
		obs_angle_list = [np.arctan2(each_obs.location[0]-state_location[0], each_obs.location[1]-state_location[1]) for each_obs in self.obstacles]
		obs_angle_list = [angle+np.pi for angle in obs_angle_list]
		# only consider obstacles in a certain radius
		# indices_to_filter = [i for i,x in enumerate(sorted_obs_dist) if x>dist_thresh]
		# # http://stackoverflow.com/questions/497426/deleting-multiple-elements-from-a-list
		# obs_dist_list = [i for j, i in enumerate(obs_dist_list) if j not in indices_to_filter]
		# obs_class_list = [i for j, i in enumerate(obs_class_list) if j not in indices_to_filter]

		# sort the list which contains the distances
		obs_class_list = [obs_class for (obs_dist, obs_class) in sorted(zip(obs_dist_list, obs_class_list))]
		obs_angle_list = [obs_angle for (obs_dist, obs_angle) in sorted(zip(obs_dist_list, obs_angle_list))]
		obs_dist_list = sorted(obs_dist_list)
		
		# only consider first no_of_closest_obstacles elements
		obs_dist_list = obs_dist_list[:no_of_closest_obstacles]
		obs_class_list = obs_class_list[:no_of_closest_obstacles]
		obs_angle_list = obs_angle_list[:no_of_closest_obstacles]

		obs_dist_list = [1./((x+1)**2) for x in obs_dist_list] # feature is 1/(dist^2) where dist = distance from obstacle
		# bring to range [0,2*pi] (np.arctan2 is [-pi,pi])
		one_hot_vecs = np.eye(len(self.semantic_obstacle_weights))

		feature_vector = []
		for idx in range(len(obs_dist_list)):
			feature_vector.append(obs_angle_list[idx])
			feature_vector.append(one_hot_vecs[obs_class_list[idx]-1].tolist()) # obstacle classes are 1 indexed.
			feature_vector.append(obs_dist_list[idx])

		return flatten_list(feature_vector)

	def get_feature_at_state_bias_dist_onehot(self, state_location, no_of_closest_obstacles=5):
		# for each obstacle in the grid object, find the euclidean distance from state_location
		obs_dist_list = [np.linalg.norm(np.asarray(state_location)-np.asarray(each_obs.location)) for each_obs in self.obstacles]
		# find the class of each obstacle
		obs_class_list = [each_obs.semantic_class for each_obs in self.obstacles]

		# sort the list which contains the distances
		obs_class_list = [obs_class for (obs_dist, obs_class) in sorted(zip(obs_dist_list, obs_class_list))]
		obs_dist_list = sorted(obs_dist_list)
		
		# only consider first no_of_closest_obstacles elements
		obs_dist_list = obs_dist_list[:no_of_closest_obstacles]
		obs_class_list = obs_class_list[:no_of_closest_obstacles]

		obs_dist_list_mult = [10./(x+1) for x in obs_dist_list] # feature is 1/(dist^2) where dist = distance from obstacle
		obs_dist_square_list = [10./((x+1)**2) for x in obs_dist_list] # feature is 1/(dist^2) where dist = distance from obstacle
		# bring to range [0,2*pi] (np.arctan2 is [-pi,pi])
		one_hot_vecs = np.eye(len(self.semantic_obstacle_weights))

		feature_vector = []
		for idx in range(len(obs_dist_list)):
			feature_vector.append(one_hot_vecs[obs_class_list[idx]-1].tolist()) # obstacle classes are 1 indexed.
			feature_vector.append(obs_dist_list_mult[idx])
			feature_vector.append(obs_dist_square_list[idx])

		feature_vector.append(1.) #bias
		return flatten_list(feature_vector)

	def get_feature_at_state_dist_onehot(self, state_location, no_of_closest_obstacles=5):		
		# for each obstacle in the grid object, find the euclidean distance from state_location
		obs_dist_list = [np.linalg.norm(np.asarray(state_location)-np.asarray(each_obs.location)) for each_obs in self.obstacles]
		# find the class of each obstacle
		obs_class_list = [each_obs.semantic_class for each_obs in self.obstacles]

		# sort the list which contains the distances
		obs_class_list = [obs_class for (obs_dist, obs_class) in sorted(zip(obs_dist_list, obs_class_list))]
		obs_dist_list = sorted(obs_dist_list)
		
		# only consider first no_of_closest_obstacles elements
		obs_dist_list = obs_dist_list[:no_of_closest_obstacles]
		obs_class_list = obs_class_list[:no_of_closest_obstacles]

		obs_dist_list_mult = [10./(x+1) for x in obs_dist_list] # feature is 1/(dist^2) where dist = distance from obstacle
		obs_dist_square_list = [10./((x+1)**2) for x in obs_dist_list] # feature is 1/(dist^2) where dist = distance from obstacle
		one_hot_vecs = np.eye(len(self.semantic_obstacle_weights))
		feature_vector = []
		for idx in range(len(obs_dist_list)):
			feature_vector.append(one_hot_vecs[obs_class_list[idx]-1].tolist()) # obstacle classes are 1 indexed.
			feature_vector.append(obs_dist_list_mult[idx])
			feature_vector.append(obs_dist_square_list[idx])
		# print feature_vector

		# flatten feature_vector to make a single list 
		return flatten_list(feature_vector)

	def get_feat_at_state_dist_no_onehot(self, state_location, no_of_closest_obstacles=3):
		# for each obstacle in the grid object, find the euclidean distance from state_location
		obs_dist_list = [np.linalg.norm(np.asarray(state_location)-np.asarray(each_obs.location)) for each_obs in self.obstacles]
		# find the class of each obstacle
		obs_class_list = [each_obs.semantic_class for each_obs in self.obstacles]
		# print "before sort", obs_dist_list
		# print "before sort", obs_class_list

		# sort the list which contains the distances
		obs_class_list = [obs_class for (obs_dist, obs_class) in sorted(zip(obs_dist_list, obs_class_list))]
		obs_dist_list = sorted(obs_dist_list)
		# print "after sort", obs_dist_list
		# print "after sort", obs_class_list, "\n"

		# only consider first no_of_closest_obstacles elements
		obs_dist_list = obs_dist_list[:no_of_closest_obstacles]
		obs_class_list = obs_class_list[:no_of_closest_obstacles]

		obs_dist_list = [1./((x+1)**2) for x in obs_dist_list] # feature is 1/(dist^2) where dist = distance from obstacle

		feature_vector = []
		for idx in range(len(obs_dist_list)):
			feature_vector.append(obs_dist_list[idx])

		return flatten_list(feature_vector)

	def get_feat_vect_traj(self, trajectory, features=get_feat_at_state_dist_no_onehot):
		all_feats = []
		for idx in range(len(trajectory)):
			curr_feature = self.get_feat_vect_at_state(trajectory[idx])
			all_feats.append(curr_feature)
		return all_feats

# http://stackoverflow.com/questions/10632111/how-to-flatten-a-hetrogenous-list-of-list-into-a-single-list-in-python
def flatten_list(xs):
	result = []
	if isinstance(xs, (list, tuple)):
		for x in xs:
			result.extend(flatten_list(x))
	else:
		result.append(xs)
	return result