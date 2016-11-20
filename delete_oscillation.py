import os
from pprint import pprint
def get_indices_of_repeated_states(filename, delete_duplicates=0, delete_min_length=0, min_length=20):
	all_at_once = []
	with open(filename) as file:
	    for line in file:
	        inner_list = [elt.strip() for elt in line.split(' ')]
	        all_at_once.append(inner_list)

	row_idx = [listicle[0] for listicle in all_at_once]
	col_idx = [listicle[1] for listicle in all_at_once]

	all_states = zip(row_idx, col_idx)

	from collections import Counter, defaultdict
	def duplicates(lst):
	    cnt= Counter(lst)
	    return [key for key in cnt.keys() if cnt[key]> 1]
	def duplicates_indices(lst):
	    dup, ind= duplicates(lst), defaultdict(list)
	    for i, v in enumerate(lst):
	        if v in dup: ind[v].append(i)
	    return ind

	indices = duplicates_indices(all_states)
	indices = indices.values()

	indices_flat = [item for sublist in indices for item in sublist]
	# print duplicates(all_states) # ['a', 'b']
	# print duplicates_indices(all_states) # ..., {'a': [0, 2, 5], 'b': [1, 4]})

	if delete_duplicates:
		# entries_to_delete = [all_at_once[idx] for idx in indices_flat]
		# pprint(entries_to_delete)
		all_at_once = [i for j, i in enumerate(all_at_once) if j not in indices_flat]
		# pprint(all_at_once)
		if delete_min_length:
			if len(all_at_once)<min_length:
				# print filename
				# os.system("cp "+filename+" temp/")
				os.system("rm "+filename)

		# file = open(filename+".uniq", 'w')
		file = open(filename, 'w')
		for idx in range(len(all_at_once)):
			file.write(' '.join(str(stuff) for stuff in all_at_once[idx]))
			file.write("\n")
		file.close()	

if __name__ == "__main__":
	data_dir = '/home/ratneshmadaan/projects/irl_math_proj/data'
	subdir = sorted(next(os.walk(data_dir))[1])
	str_to_remove = 'a_star'
	for idx in range(len(subdir)):
		traj_dir = os.path.join(data_dir, subdir[idx], 'features')
		files = os.listdir(traj_dir)
		# remove a star traj
		for item in files:
			if str_to_remove in item:
				files.remove(item)
		files = sorted(files)
		# print files
		for item in files:
			full_path = os.path.join(traj_dir, item)
			get_indices_of_repeated_states(full_path,delete_duplicates=1, delete_min_length=1, min_length=20)
			# print item, indices_to_remove

