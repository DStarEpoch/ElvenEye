import quick_A_star_2D as psA
#import Path_A_star_2 as psA
import mapmodule as mpm
import os
import sys
import pygame
from pygame.locals import *
import map2image
import math

BGCOLOR = (150,150,150)
TRJCOLOR  = (255, 255, 0)
WHITE = (255,255,255)


class Drawing_Board:
    trj = []
    dimention = 2
    map_range = (200, 200)
    mapdata = []
    load_state = 'done'
    
    find_path_state = 'searching'
    mapvalue = []
    
    #do not remember to change parament in class Animation
    def __init__(self,screen,mapfile):
        self.screen = screen
        self.mapfile = mapfile
        mpt = mpm.Map_LIB()
        mpc = mpt.map_load(filename = mapfile)
        if ((mpc.dimention == 2) and (mpc.map_range == (200, 200))):
            mp = mpc.mapdata
            maxv = -1000000000000.0
            minv = 10000000000000.0
            for i in range(200):
                for j in range(200):
                    if (mp[i][j] > maxv):
                        maxv = mp[i][j]
                    if (mp[i][j] < minv):
                        minv = mp[i][j]
            step = (maxv - minv) / 255
            for i in range(mpc.map_range[0]):
                self.mapdata.append([])
                for j in range(mpc.map_range[1]):
                    self.mapdata[i].append(int((mp[i][j] - minv)/step))

            self.map_image = map2image.convert_map(self.mapdata)
            self.map_image_pos = self.map_image.get_rect()
            self.map_image_pos.center = (900, 500)

            self.load_state = 'done'
        else:
            self.load_state = 'error'

    def draw_map(self,screen):
        screen.blit(self.map_image, self.map_image_pos)
        

    def draw_trajectory(self, path):
        self.find_path_state = path.state
        if (path.state != 'Eureka!'):
            pth = path.one_step()
            self.trj = path.adjust_trj(pth)

        plist = []
        for p in self.trj:
            get_x = 400 + (p[0] - 1) * 5 + 3
            get_y = 1000 - (p[1] - 1) * 5 - 3
            plist.append((get_x,get_y))
        
        pygame.draw.lines(self.screen, TRJCOLOR, False, plist, 5) 

class Animation:
	size = width,height = 1800,1000
	Max_dot_num = 3000
	Max_Frame = 2000000000
	trans_matrix = []

	def __init__(self,mapfile = 'test.mpd'):
		pygame.init()
		pygame.display.set_caption('milestoning')
		self.mapfile = mapfile
		self.screen = pygame.display.set_mode(self.size)
		self.frame_rate = 50
		self.clock = pygame.time.Clock()
		self.path = psA.Path_Lib(dimention = 2, startpoint = (56,175, 56), endpoint = (172, 33, 172), milestone_label = 1) 

	def start_animation(self):
		db = Drawing_Board(self.screen, self.mapfile)

		count = 0
		while (True):
			for event in pygame.event.get():
				if (event.type == QUIT):
					path = self.path.one_step()
					trj = self.path.adjust_trj(path)
					print(trj)
					print('length of pathway:',len(trj))
					pygame.quit()
					sys.exit()

			self.screen.fill(BGCOLOR)

			db.draw_map(self.screen)
			db.draw_trajectory(self.path)

			pygame.display.flip()
            
			self.clock.tick(self.frame_rate)

if (__name__ == '__main__'):
	anm = Animation('test.mpd')
	anm.start_animation()
