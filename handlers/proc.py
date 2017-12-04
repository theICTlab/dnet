import numpy as np

class Process:
	@classmethod
	def setup(cls, s_l, l):
		"""Sets up the labels for the network.
		#Arguments
			s_l: Selected labels to learn in network
			l: labels that correspond to all labels in images when flattened to single channel.
				This is required because some images might not have all labels. Example = Red,Blue,Yellow = 1,4,3
		"""
		cls.selected_labels = s_l
		cls.max_labels = l
	
	@staticmethod
	def join_imgs(xs,ys,depth=1):
		return [np.concatenate(x,y[:,:,:depth],axis=3) for x,y in zip(xs,ys)]

	@staticmethod
	def label_bin(y, max_labels):
		_y = np.zeros((y.shape[0], max_labels),dtype=np.int)
		_y[np.arange(y.shape[0]),y] = 1
		return _y

	@classmethod
	def categorize_img(cls, y):
		y = cls.to_single_channel(y)
		_y = y.reshape((y.size,1))
		_sz = len(cls.max_labels)
		_y = label_bin(_y,range(_sz))
		_y = _y.reshape((y.shape[:2]+(_sz,))).astype(int)
		_y = _y[:,:,cls.selected_labels]
		return _y

	@classmethod
	def categorize_imgs(cls,ys):
		return [cls.categorize_img(y) for y in ys] 

	@classmethod	
	def to_single_channel(cls,y):
		y_res = y[:,:,0]+(2*y[:,:,1])+(4*y[:,:,2])
		y_comp = np.copy(y_res)
		vals = [0]*len(cls.max_labels)	
		for l in cls.selected_labels:
			vals[l] = l
		for k, v in zip(cls.max_labels,cls.selected_labels):
			y_comp[y_res==k]= v

		return y_comp
	
	@classmethod
	def generate_patch(xs,ys,patch_size, batch_size=64, augment=False):
		x_train = []
		y_train = []

		while True:
			#Randomizes all possible locations into "patch_locations"
			patch_locations = []
			sum_locations = 0
			all_locations = []
			for y in ys:
				locations = int((y.shape[0]-patch_size[0])*(y.shape[1]-patch_size[1]))
				sum_locations += locations
				all_locations.append(locations)
				patch_locations.append(np.random.permutation(locations))
			patch_index = [0]*len(ys)
			
			i = 0
			while sum(patch_index) < sum_locations:
				#If patch_index has not reached all locations
				if patch_index[i] < all_locations[i]:
					index=patch_locations[i][patch_index[i]]
					x_patch = get_patch(xs[i], patch_size, index)
					y_patch = get_patch(ys[i], patch_size, index)
					x_train.append(x_patch)
					y_train.append(y_patch)
					patch_index[i] += 1
				i+=1
				i = i%len(y)

				if len(y_train) == batch_size:
					y_train = np.array(y_train)
					x_train = np.array(x_train)
					yield x_train, y_train
					x_train = []
					y_train = []
		
		
	@staticmethod
	def get_patch(img, patch_size, index):
		x_val = index%(img.shape[0]-patch_size[0])
		y_val = index//(img.shape[0]-patch_size[0])
		return img[x_val:x_val+patch_size[0],y_val:y_val+patch_size[1],:]