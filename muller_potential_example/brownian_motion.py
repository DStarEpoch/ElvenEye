import math
import random
import numpy as np

class BrownianDynamic:

	gamma = 100000
	kT = 30000
	dt = 0.025

	def __init__(self, gamma=100000, kT=30000, dt=0.025):
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
		####deltaU = [U(x+dx)-U(x)]/dx
		output_list = []
		position_update=[]
		position_update.append(position[0])
		position_update.append(position[1])
		random = np.random.normal(scale=np.sqrt((2.0 * self.kT * self.dt) / (self.gamma)),size=(nsteps - 1, 2))
		x = 0
		y = 0
		for i in range(nsteps-1):
			dx = 0.001
			dy = 0.001
			position_update[0] = x
			position_update[1] = y
			output_list.append(tuple(position_update))
			U = self.potential((x,y))
			U_x_dx = self.potential((x+dx,y))
			U_y_dy = self.potential((x,y+dy))
			deltaU = ((U_x_dx-U)/dx, (U_y_dy-U)/dy)
		#### v = -D/kT*deltaU+(2D)^0.5*lamda*f(t)	
			D = self.kT/self.gamma
			vx = -D/self.kT*deltaU[0]+math.sqrt(2*D)*random[i][0]
			vy = -D/self.kT*deltaU[1]+math.sqrt(2*D)*random[i][1]
			x = x + vx*self.dt
			y = y + vy*self.dt
			print(x, y)
		#------------end----------------------#
		return(output_list.copy())

if (__name__ == '__main__'):
	BD = BrownianDynamic()
	output = BD.move((-0.8,0.8), nsteps=10000000)
	obj_f = open('freeE.dat', 'w')
	for d in output:
		obj_f.write(str(d[0]) + '\t' + str(d[1]) + '\n')
	obj_f.close()
