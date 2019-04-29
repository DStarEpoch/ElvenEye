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

	def __init__(self, value, end_point_value, coor, father, peaklist):
		self.value = value
		self.end_point_value = end_point_value
		self.coor = coor
		self.father = father
		self.peaklist = peaklist.copy()

	def better_than(self, other):
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
			if (len(other.peaklist) >= len(self.peaklist)):
				return(True)
class Path_Lib:

	pending = []
	visited = []
	record = {}

	def __init__(self, dimention, startpoint, endpoint):
		self.dimention = dimention
		self.startpoint = startpoint
		self.endpoint = endpoint

		self.current = startpoint 
		self.expect_value = datamodule.data_get(self.endpoint)
		self.add_to_visited(self.startpoint)
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

	def add_to_visited(self, coor = (1,1)):
		if (coor in self.record):
			self.pending.remove(coor)
			self.visited.append(coor)
			n_info = self.record[coor]
		else:
			#create a root node
			self.visited.append(coor)

			value = datamodule.data_get(coor)
			father = -1
			cur_peak_list = []
			root_node = Node(value, self.expect_value, coor, father, cur_peak_list)
			
			n_info = root_node
			self.record[coor] = n_info

		pl = surround(coor)
		for p in pl:
			if (not (p in self.record)):
				new_coor = p
				new_value = datamodule.data_get(p)
				new_father = coor
				new_peak_list = []
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

				new_node = Node(new_value, self.expect_value, new_coor, new_father, new_peak_list)
				self.record[p] = new_node
				#add new node to pending set and sort
				l = len(self.pending)
				done = False
				for i in range(l):
					if (self.pending[i] in self.record):
						pass
					else:
						print(self.pending[i])
						print(self.record)
						print('False')
					if (new_node.better_than(self.record[self.pending[i]])):
						self.pending.insert(i, new_node.coor)
						done = True
						break
				if (not done):
					self.pending.append(new_node.coor)
			else:
				if (p in self.pending):
					new_coor = p
					new_value = self.record[p].value
					father = n_info.coor

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

					vp = Node(new_value, self.expect_value, new_coor, father,new_peak_list)
					if (vp.better_than(self.record[p])):
						self.pending.remove(p)
						del(self.record[p])
						self.record[p] = vp

						l = len(self.pending)
						done = False
						for i in range(l):
							if (self.record[p].better_than(self.record[self.pending[i]])):
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

		if (self.state == 'searching'):
			node_coor = self.pending[0]
			self.add_to_visited(node_coor)

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
	PL = Path_Lib(dimention = 2, startpoint = (56,175), endpoint = (172,33))
	count = 0
	while (PL.state != 'Eureka!'):
		count += 1
		path = PL.one_step()
		path = PL.adjust_trj(path)
		print(path)
		print('path length:', len(path))
		print('round:', count)
