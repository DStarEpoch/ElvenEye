import math
import pickle
import os

class Map_Class:
    dimention = 2
    map_range = (0, 0)
    mapdata = []

    
class Map_LIB(Map_Class):
    '返回的mapdata数据从下标从0开始'
    
    def __init__(self):
        pass

    def map_load(self, filename):
        mc = Map_Class()

        os.chdir('map')

        pickle_file = open(filename, 'rb')
        dimention = pickle.load(pickle_file)
        map_range = pickle.load(pickle_file)
        mapdata   = pickle.load(pickle_file)
        pickle_file.close()

        os.chdir('..')

        mc.dimention = dimention
        mc.map_range = map_range
        mc.mapdata   = mapdata.copy()

        return(mc)
        

#MullerPotential
    def analysis_func(self,coor = (0,0)):
        AA = [-200.0, -100.0, -170.0, 15.0]
        ac = [-1.0, -1.0, -6.5, 0.7]
        bc = [0.0, 0.0, 11.0, 0.6]
        cc = [-10.0, -10.0, -6.5, 0.7]
        xc = [1.0, 0.0, -0.5, -1.0]
        yc = [0.0, 0.5, 1.5, 1.0]

        e = 0.0
        for i in range(4):
            tmp = ac[i] * (coor[0] - xc[i])**2 + bc[i] * (coor[0] - xc[i]) * (coor[1] - yc[i]) + cc[i] * (coor[1] - yc[i])**2
            e += AA[i] * math.exp(tmp)

        return(e)

#double well potential
#    def analysis_func(self, coor = (0,0)):
#        delta = 0.1
        #U = coor[0]**6 + coor[1]**6 + math.exp((-coor[0]/delta)**2)*(1-math.exp((-coor[1]/delta)**2))
#        U = coor[0]**6 + coor[1]**6 + math.exp(-(coor[0]/delta)**2)*(1-math.exp(-(coor[1]/delta)**2))
#        print(coor, '-->', U)

#        return(U)

    def analysis2map(self):
        filename = 'test.mpd'
        dimention = 2
        map_range = (200, 200)
        mapdata = []
        #MullerPotential range
        coor_range = ((-1.2, 0.8), (-0.3, 1.7))

        #double well range
        #coor_range = ((-1.0, 1.0), (-1.0, 1.0))
 
        coor = []
        for i in range(dimention):
            coor.append(0)
            
        def irrdata(obje, lay, d, map_range, coordinate_range):
            nonlocal coor

            output_list = []
            if (lay == d):
                for i in range(map_range[lay - 1]):
                    coor[lay-1] = coordinate_range[lay-1][0] + (coordinate_range[lay-1][1] - coordinate_range[lay-1][0]) * i / map_range[lay-1]
                    output_list.append(obje.analysis_func(coor))
                return(output_list)
            else:
                for i in range(map_range[lay - 1]):
                    coor[lay-1] = coordinate_range[lay-1][0] + (coordinate_range[lay-1][1] - coordinate_range[lay-1][0]) * i / map_range[lay-1]
                    output_list.append(irrdata(obje,lay+1,d,map_range,coordinate_range))
                return(output_list)
        
        mapdata = irrdata(self, 1, dimention, map_range, coor_range)
        #for i in range(len(mapdata)):
        #    print(mapdata[i])
        self.map_save(filename, dimention,map_range,mapdata)
    
    def map_save(self, filename, dimention, map_range, mapdata):
        if (not os.path.exists('map')):
            os.mkdir('map')
        os.chdir('map')

        if (os.path.exists(filename)):
            os.remove(filename)
        pickle_file = open(filename, 'wb')
        pickle.dump(dimention, pickle_file)
        pickle.dump(map_range, pickle_file)
        pickle.dump(mapdata, pickle_file)
        pickle_file.close()
        
        os.chdir('..')

if (__name__ == '__main__'):
    mp = Map_LIB()
    mp.analysis2map()
        
