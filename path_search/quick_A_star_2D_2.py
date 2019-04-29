import datamodule
import math

def surround(node = (0,0)):
	dot = list(node)
	l = len(dot)

	output_list = []
	for i in range(l):
		new_dot1 = dot.copy()
		new_dot1[i] -= 1
		new_dot2 = dot.copy()
		new_dot2[i] += 1
		output_list.append(tuple(new_dot1))
		output_list.append(tuple(new_dot2))

	return(output_list)

class Node:
	
	def __init__(self, value, end_point_value, coor, father, peaklist, pre_dist, fwd_dist):
		self.value = value
		self.end_point_value = end_point_value
		self.coor = coor
		self.father = father
		self.peaklist = peaklist.copy()
		self.pre_dist = pre_dist
		self.fwd_dist = fwd_dist

	def better_than(self, other, label, milestone_seq):
		if (self.value < self.end_point_value):
			list1 = [self.end_point_value]
		else:
			list1 = [self.value]
		if (other.value < self.end_point_value):
			list2 = [self.end_point_value]
		else:
			list2 = [other.value]

		if (len(self.peaklist) > len(other.peaklist)):
			length = len(other.peaklist)
		else:
			length = len(self.peaklist)

		for i in range(length):
			done = False
			for j in range(len(list1)):
				if (self.peaklist[i] > list1[j]):
					list1.insert(j, self.peaklist[i])
					done = True
					break
			if (not done):
				list1.append(self.peaklist[i])
		for i in range(length):
			done = False
			for j in range(len(list2)):
				if (other.peaklist[i] > list2[j]):
					list2.insert(j, other.peaklist[i])
					done = True
					break
			if (not done):
				list2.append(other.peaklist[i])

		length += 1
		for i in range(length):
			if (list2[i] != list1[i]):
				break
		if (list2[i] < list1[i]):
			return(False)
		if (list2[i] > list1[i]):
			return(True)
		if (list2[i] == list1[i]):
			if (len(other.peaklist) < len(self.peaklist)):
				return(False)
			if (len(other.peaklist) >len(self.peaklist)):
				return(True)

		if ((self.pre_dist + self.fwd_dist) < (other.pre_dist + other.fwd_dist)):
			return(True)
		if ((self.pre_dist + self.fwd_dist) > (other.pre_dist + other.fwd_dist)):
			return(False)

		d1 = milestone_seq.index(self.coor[label])
		d2 = milestone_seq.index(other.coor[label])
		if (d1 >= d2):
			return(True)
		else:
			return(False)


class Path_Lib:

	pending = []
	visited = []
	record  = {}

	fix_label = {}

	def __init__(self, dimention, startpoint, endpoint, milestone_label):
		self.dimention =dimention
		self.startpoint = startpoint
		self.endpoint = endpoint
		self.max_memory = 2 * len(self.startpoint)**2

		route = abs(endpoint[milestone_label] - startpoint[milestone_label])
		if (endpoint[milestone_label] >= startpoint[milestone_label]):
			step = 1
		else:
			step = -1
		self.milestone_label = milestone_label
		self.current_milestone_index = 0
		self.milestone_seq = []
		for i in range(route+1):
			self.milestone_seq.append(startpoint[milestone_label]+i*step)
		

		#self.current = startpoint
		self.expect_value = datamodule.data_get(self.endpoint)
		self.add_to_visited(self.startpoint)
		self.state = 'searching'

	def update_milestone(self, startpoint, endpoint):
		max_dis = abs(startpoint[0] - endpoint[0])
		k = 0
		for i in range(len(startpoint)):
			d = abs(startpoint[i] - endpoint[i])
			if (d > max_dis):
				max_dis = d
				k = i
		self.milestone_label = k
		self.current_milestone_index = 0
		self.milestone_seq = []

		route = abs(endpoint[k] - startpoint[k])
		if (endpoint[k] >= startpoint[k]):
			step = 1
		else:
			step = -1
		for i in range(route+1):
			self.milestone_seq.append(startpoint[k] + i*step)

		self.state = 'searching'

	def ifpeak(self, node_pre, value):
		if (node_pre.value <= value):
			return(False)
		else:
			p1 = self.record[node_pre.coor]
			p1f = node_pre.father
			if (p1f == -1):
				return(False)
			else:
				while(p1.value == self.record[p1f].value):
					p1 = self.record[p1f]
					p1f = p1.father
					if (p1f == -1):
						return(False)
				if (self.record[p1f].value > p1.value):
					return(False)
				else:
					return(True)

	def distance(self, coor1, coor2):
		SUM = 0 
		for i in range(len(coor1)):
			SUM += (coor1[i] - coor2[i])**2
		SUM = math.sqrt(SUM)
		return(SUM)

	def clean(self, coor):
		self.pending = []
		visited_new = [coor]
		record_new = {}

		f = self.record[coor]
		record_new[coor] = f
		while (f.father != -1):
			f = self.record[f.father]
			visited_new.append(f.coor)
			record_new[f.coor] = f

		self.visited = visited_new.copy()

		self.record = record_new
		

	def add_to_visited(self, coor = (1,1)):
		if (coor in self.record):
			self.pending.remove(coor)
			self.visited.append(coor)
			n_info = self.record[coor]
			if (self.milestone_seq[self.current_milestone_index] != self.endpoint[self.milestone_label]):
				if (n_info.coor[self.milestone_label] == self.milestone_seq[self.current_milestone_index + 1]):
					self.current_milestone_index += 1
					n_info.peaklist =[]
					self.clean(coor)
			else:
				self.state = 'reach_end_milestone'
				n_info.peaklist = []
				self.clean(coor)
				self.fix_label[self.milestone_label] = coor[self.milestone_label]
		else:
			#create a root node
			self.visited.append(coor)
			
			value = datamodule.data_get(coor)
			father = -1
			pre_dist = 0
			fwd_dist = self.distance(coor, self.endpoint)
			cur_peak_list = [] 
			root_node = Node(value, self.expect_value, coor, father, cur_peak_list, pre_dist, fwd_dist)
			
			n_info = root_node
			self.record[coor] = n_info
		
		pl = surround(coor)
		for p in pl:
			if (not (p in self.record)):
				#record a new node
				#estimate whether the new node is a legitimate node
				if (p[self.milestone_label] in self.milestone_seq[self.current_milestone_index:]):
					go_on = True
					for fi in self.fix_label:
						if (self.fix_label[fi] != p[fi]):
							go_on = False
					if (not go_on):
						continue
					#set new node's father as new visited node
					new_coor = p
					new_value = datamodule.data_get(p)
					new_father = coor
					new_pre_dist = n_info.pre_dist + self.distance(coor, p)
					fwd_dist = self.distance(p, self.endpoint)
					new_peak_list = []
					for i in n_info.peaklist:
						new_peak_list.append(i)
					if (self.ifpeak(n_info, new_value)):
						newpeak = n_info.value
						l = len(new_peak_list)
						done = False
						for i in range(l):
							if (new_peak_list[i] < newpeak):
								new_peak_list.insert(i, newpeak)
								done = True
								break
						if (not done):
							new_peak_list.append(newpeak)

					new_node = Node(new_value, self.expect_value, new_coor, new_father, new_peak_list, new_pre_dist, fwd_dist)
					self.record[p] = new_node
					#add new node to pending set and sort the pending set
					l = len(self.pending)
					done = False
					for i in range(l):
						if (new_node.better_than(self.record[self.pending[i]],self.milestone_label, self.milestone_seq)):
							self.pending.insert(i, new_node.coor)
							done = True
							break
					if (not done):
						self.pending.append(new_node.coor)

			else:
				#if the node has been recorded, check if it is in pending set
				if (p in self.pending):
					#estimate should we replace the node's father
					#in order to estimate we create a virtual point as the state of node's father has been replaced
					new_coor = p
					new_value = self.record[p].value
					father = n_info.coor
					new_pre_dist = n_info.pre_dist + self.distance(n_info.coor, p)
					fwd_dist = self.record[p].fwd_dist

					new_peak_list = []
					for i in n_info.peaklist:
						new_peak_list.append(i)
					if (self.ifpeak(n_info, new_value)):
						newpeak = n_info.value
						l = len(new_peak_list)
						done = False
						for i in range(l):
							if (new_peak_list[i] < newpeak):
								new_peak_list.insert(i, newpeak)
								done = True
								break
						if (not done):
							new_peak_list.append(newpeak)
					
					vp = Node(new_value, self.expect_value, new_coor, father, new_peak_list, new_pre_dist, fwd_dist)
					if (vp.better_than(self.record[p], self.milestone_label, self.milestone_seq)):
						self.pending.remove(p)
						del(self.record[p])
						self.record[p] = vp

						l = len(self.pending)
						done = False
						for i in range(l):
							if (self.record[p].better_than(self.record[self.pending[i]], self.milestone_label, self.milestone_seq)):
								self.pending.insert(i, self.record[p].coor)
								done = True
								break
						if (not done):
							self.pending.append(p)
					del(vp)

	def adjust_trj(self, trj):
		output_list = [trj[0]]
		current = 0
		for i in range(len(trj)):
			if (i == len(trj) - 1):
				output_list.append(trj[i])
				return(output_list)
			else:
				flag = False
				for j in range(len(trj[i])):
					if (abs(trj[i][j] - output_list[current][j]) >= 2):
						flag = True
						break
				if (flag):
					output_list.append(trj[i-1])
					current += 1
				

	def one_step(self):
		if (self.endpoint in self.visited):
			print('Searching Complete')
			self.state = 'Eureka!'

			p1 = self.endpoint
			p2 = self.record[self.endpoint].father
			output_list = [p1]
			while (p2 != -1):
				p1 = p2
				p2 = self.record[p1].father
				output_list.insert(0, p1)

			return(output_list)

		if (self.state != 'Eureka!'):
			if (self.current_milestone_index < len(self.milestone_seq)-1):
				if (len(self.pending) > self.max_memory):
					for k in self.pending:
						if (k[self.milestone_label] == self.milestone_seq[self.current_milestone_index + 1]):
							coor = k
							break

					ind = self.pending.index(coor)
					tmp = self.pending[0]
					self.pending[0] = coor
					self.pending[ind] = tmp

			node_coor = self.pending[0]
			self.add_to_visited(node_coor)
			if (self.state == 'reach_end_milestone'):
				self.update_milestone(node_coor, self.endpoint)

			output_list = []
			p1 = node_coor
			p2 = self.record[node_coor].father
			output_list = [p1]
			while (p2 != -1):
				p1 = p2
				p2 = self.record[p1].father
				output_list.insert(0, p1)
			return(output_list)

if (__name__ == '__main__'):
	PL = Path_Lib(dimention = 2, startpoint = (56,175), endpoint = (172,33), milestone_label = 1)
	count = 0
	while (PL.state != 'Eureka!'):
			count += 1
			path = PL.one_step()
			path = PL.adjust_trj(path)
			print(path)
			print('path length:', len(path))
			print('round:', count)
