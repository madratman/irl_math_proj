import os

data_dir = '/home/ratneshmadaan/projects/irl_math_proj/data'
subdir = sorted(next(os.walk(data_dir))[1])
str_to_remove = 'a_star_traj'

for idx in range(1):
	traj_dir = os.path.join(data_dir, subdir[idx], 'features')
	files = sorted(os.listdir(traj_dir))
	# retain a star traj
	for item in files:
		if str_to_remove in item:
			files.remove(item)
			# print item
	files = sorted(files)
	print files
	# for item in files:
		# full_path = os.path.join(traj_dir, item)
		# print item, indices_to_remove

