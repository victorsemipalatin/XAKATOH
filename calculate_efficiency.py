import pickle
from sys import argv
import os
from module import *


_, folder, t = argv
t = int(t)
N = [] # массив номеров событий, в которых мюон прошёл через детектор
for file in os.listdir(os.path.join(matrix_path, folder)):
    try:
        matrix = get_data_from_matrix(os.path.join(matrix_path, folder, file))
        for i in range(len(matrix)):
            if "mu" in matrix[i][0]:
                N.append(file[-9:])
                break
    except:
        pass
all_events = [0, 0, 0, 0, 0, 0]
triggered_events = [0, 0, 0, 0, 0, 0]
for number in N:
    try:
        matrix = get_data_from_matrix(os.path.join(matrix_path, folder, f"ChargedMatrix{number}"))
        event = get_data_from_event(os.path.join(events_path, folder, f"Event{number}"))
            
        x = [el[2] for el in matrix if "mu" in el[0]]
        y = [el[3] for el in matrix if "mu" in el[0]]
        z = [el[4] for el in matrix if "mu" in el[0]]
        
        try:
            k_1, b_1 = mse(x, z) # параметрическое задание прямой в пространстве с помощью мнк
            k_2, b_2 = mse(y, z)
        except:
            continue

        for i in range(len(coord)):
            if (-500 < (coord[i] - b_1) / k_1 and (coord[i] - b_1) / k_1 < 500) and (-500 < (coord[i] - b_2) / k_2 and (coord[i] - b_2) / k_2 < 500): # смотрим проходит ли трек через данную плоскость
                all_events[i] += 1
                j = -1
                for k in range(len(event)):
                    if event[k][-1] // count_in_plane == i:
                        j = k
                        break
                if j == -1:
                    continue
                sipm = event[j][-1]
                z = 0
                for k in range(len(event)):
                    if event[k][-1] == sipm:
                        current_qe = linear_interpolation(event[k][0])
                        if current_qe < np.random.sample() * 100: # моделируем фотоэффект
                            z += box_muller()
                if z / mean >= t:
                    triggered_events[i] += 1

    except Exception as err:
        pass
        
with open("Trash/" + f"{folder}_efficiency.bin", 'wb') as l:
    pickle.dump([all_events, triggered_events], l)
