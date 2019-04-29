import pygame

def colorbar_map(value):
    if (value <= 0):
        return((0,0,0))
    
    if ((value > 0) and (value <= 64)):
        return((0,0,value * 4 - 1))
    
    if ((value > 64) and (value <= 128)):
        return((0, (value - 64)*4 - 1, 255))
    
    if ((value > 128) and (value <= 255)):
        return(((value - 128)*2 - 1,255,255))
    
    if (value > 255):
        return((255,255,255))

def convert_map(mapdata):
    suf = pygame.image.load('map_image.bmp')
    for i in range(200):
        for j in range(200):
            for k in range(5):
                for l in range(5):
                    suf.set_at((5*i+k,1000 - (5*j+l)), colorbar_map(mapdata[i][j]))
    return(suf)                
