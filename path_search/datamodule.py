import math

def potantial2(x,y):
	AA = [-200.0, -100.0, -170.0, 15.0]
	ac = [-1.0, -1.0, -6.5, 0.7]
	bc = [0.0, 0.0, 11.0, 0.6]
	cc = [-10.0, -10.0, -6.5, 0.7]
	xc = [1.0, 0.0, -0.5, -1.0]
	yc = [0.0, 0.5, 1.5, 1.0]

	e = 0.0
	for i in range(4):
		tmp = ac[i] * (x - xc[i])**2 + bc[i] * (x - xc[i]) * (y - yc[i]) + cc[i] * (y - yc[i])**2
		e += AA[i] * math.exp(tmp)

	return(e)


def potantial3(x,y,z):
	AA = [-200.0, -100.0, -170.0, 15.0]
	ac = [-1.0, -1.0, -6.5, 0.7]
	bc = [0.0, 0.0, 11.0, 0.6]
	cc = [-10.0, -10.0, -6.5, 0.7]
	xc = [1.0, 0.0, -0.5, -1.0]
	yc = [0.0, 0.5, 1.5, 1.0]

	e = 0.0
	for i in range(4):
		tmp = ac[i] * (x - xc[i])**2 + ac[i] * (z - xc[i])**2 + bc[i] * (x - xc[i]) * (y - yc[i]) + bc[i] * (z - xc[i]) * (y - yc[i]) + cc[i] * (y - yc[i])**2
		e += AA[i] * math.exp(tmp)

	return(e)

def potantial4(x,y,z,a):
	AA = [-200.0, -100.0, -170.0, 15.0]
	ac = [-1.0, -1.0, -6.5, 0.7]
	bc = [0.0, 0.0, 11.0, 0.6]
	cc = [-10.0, -10.0, -6.5, 0.7]
	xc = [1.0, 0.0, -0.5, -1.0]
	yc = [0.0, 0.5, 1.5, 1.0]

	e = 0.0
	for i in range(4):
		tmp = ac[i] * (x - xc[i])**2 + ac[i] * (z - xc[i])**2 + ac[i] * (a - xc[i])**2+ bc[i] * (x - xc[i]) * (y - yc[i]) + bc[i] * (z - xc[i]) * (y - yc[i]) + bc[i] * (a - xc[i]) * (y -yc[i])+ cc[i] * (y - yc[i])**2
		e += AA[i] * math.exp(tmp)

	return(e)

def data_get(coor):
	if (len(coor) == 2):
		get_x = -1.2 + (coor[0]-1) * 0.01
		get_y = -0.3 + (coor[1]-1) * 0.01
		return(potantial2(get_x, get_y)) 
	if (len(coor) == 3):
		get_x = -1.2 + (coor[0]-1) * 0.01
		get_z = -1.2 + (coor[2]-1) * 0.01
		get_y = -0.3 + (coor[1]-1) * 0.01
		return(potantial3(get_x, get_y, get_z))
	if (len(coor) == 4):
		get_x = -1.2 + (coor[0]-1) * 0.01
		get_z = -1.2 + (coor[2]-1) * 0.01
		get_a = -1.2 + (coor[3]-1) * 0.01
		get_y = -0.3 + (coor[1]-1) * 0.01
		return(potantial4(get_x, get_y, get_z, get_a))
