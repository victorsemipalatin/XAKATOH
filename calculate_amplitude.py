import pickle
from sys import argv
import os
from module import *


_, folder = argv
N = 0 # количество непустых событий
sipm = [] # массив с амплитудами сигналов каждого SiPM
for i in range(0, 1153):
    sipm.append(0)
for file in os.listdir(os.path.join(events_path, folder)):
    try:
        event = get_data_from_event(os.path.join(events_path, folder, file)) # одно событие, соответствующее файлу Event____.dat
        if len(event) != 0:
            N += 1
        for i in range(len(event)):
            current_qe = linear_interpolation(event[i][0])
            if current_qe < np.random.sample() * 100: # моделируем фотоэффект
                    z = box_muller() # слкчайная величина из гауссовского распределения
                    sipm[int(event[i][2])] += z / mean
    except:
        pass

sipm[-1] = N
with open("Trash/" + folder + "_calculated.bin", 'wb') as l:
    pickle.dump(sipm, l)
