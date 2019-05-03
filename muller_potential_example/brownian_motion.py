import math
import random
import numpy as np

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
		####deltaU = [U(x+dx)-U(x)]/dx
		output_list = []
		position_update=[]
		position_update.append(position[0])
		position_update.append(position[1])
		for i in range(nsteps):
			dx = 0.01
			dy = 0.01
			output_list.append(position_update)
			x = position_update[0]
			y = position_update[1]
			U = self.potential((x,y))
#			U_y = self.potential((x,y))[1]
			U_x_dx = self.potential((position_update[0]+dx,position_update[1]))
			U_y_dy = self.potential((position_update[0],position_update[1]+dy))
			deltaU = ((U_x_dx-U)/dx, (U_y_dy-U)/dy)
		####f(t) in 2D is f(x,y) = Aexp(-(x^2/2sigma_x^2)+(y^2/2sigma_y^2))
			random_xy = self.gauss_2d(mu=0,sigma=math.sqrt(2*self.gamma*self.kT/self.dt))
			sigma_x = math.sqrt(2*self.gamma*self.kT/self.dt)
			sigma_y = math.sqrt(2*self.gamma*self.kT/self.dt)
		#f = Aexp(-(random_xy[0]^2/(2*sigma_x^2))+(random_xy[1]^2/(2*sigma_y^2)))
			fx = 1/math.sqrt(2*math.pi)/sigma_x*np.exp(-random_xy[0]*random_xy[0]/(2*sigma_x*sigma_x))
			fy = 1/math.sqrt(2*math.pi)/sigma_y*np.exp(-random_xy[1]*random_xy[1]/(2*sigma_y*sigma_y))
		#### v = -D/kT*deltaU+(2D)^0.5*lamda*f(t)	
			D = self.kT/self.gamma
			vx = -D/self.kT*deltaU[0]+math.sqrt(2*D)*fx
			vy = -D/self.kT*deltaU[1]+math.sqrt(2*D)*fy
			position_update[0] = position_update[0]+vx*self.dt
			position_update[1] = position_update[1]+vy*self.dt
		#------------end----------------------#
		return(output_list.copy())

	def gauss_2d(self, mu, sigma):
		x = random.gauss(mu,sigma)
		y = random.gauss(mu,sigma)
		return(x,y)
if (__name__ == '__main__'):
	BD = BrownianDynamic()
	output = BD.move((0,0), nsteps=10000)
	obj_f = open('freeE.dat', 'w')
	for d in output:
		obj_f.write(str(d[0]) + '\t' + str(d[1]) + '\n')
	obj_f.close()
