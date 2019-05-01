import math
import random

class BrownianDynamic:

	gamma = 10000
	kT = 300
	dt = 0.01

	def __init__(self, gamma=10000, kT=300, dt=0.01):
		self.gamma = gamma
		self.kT = kT
		self.dt = dt

	def potential(self, position=(0, 0)):
		AA = [-200.0, -100.0, -170.0, 15.0]
		ac = [-1.0, -1.0, -6.5, 0.7]
		bc = [0.0, 0.0, 11.0, 0.6]
		cc = [-10.0, -10.0, -6.5, 0.7]
		xc = [1.0, 0.0, -0.5, -1.0]
		yc = [0.0, 0.5, 1.5, 1.0]

		re = 0.0
		for i in range(4):
			tmp = ac[i] * (position[0] - xc[i])**2 + bc[i] * (position[0] - xc[i]) * (position[1] - yc[i]) + cc[i] * (position[1] - yc[i])**2
			re += AA[i] * math.exp(tmp)
		return(re)

	def move(self, position=(0, 0), nsteps=100):
		# -----------to be continue-----------#
		
		pass
		output_list = []
		#------------end----------------------#
		return(output_list.copy())

if (__name__ == '__main__'):
	BD = BrownianDynamic()
