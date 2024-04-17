import pickle
from sys import argv
import os
from module import *


# отберём события, в которых есть мюоны
_, folder = argv
t = 0 # порог был рассчита в предыдущем задании
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

reconstructed_tracks = []
for number in N: # классика
    reconstructed_tracks.append([])
    try:
        current_track = [] # трек из данного события
        matrix = get_data_from_matrix(os.path.join(matrix_path, folder, f"ChargedMatrix{number}"))
        event = get_data_from_event(os.path.join(events_path, folder, f"Event{number}"))
            
        x = [el[2] for el in matrix if "mu" in el[0]] # координаты моделируемого мюона
        y = [el[3] for el in matrix if "mu" in el[0]]
        z = [el[4] for el in matrix if "mu" in el[0]]
        
        try: # считаем, что мюон никак не отклоняется, поэтому можно считать, что его трек идеально ложится на прямую
            k_1, b_1 = mse(x, z) # параметрическое задание прямой в пространстве с помощью мнк
            k_2, b_2 = mse(y, z)
        except:
            continue
        i = 0
        while i < len(event):
            sipm = event[i][-1] # номер sipm
            s_c = sipm_coords[int(sipm)] # координаты световода
            k = i
            z = 0
            while k < len(event):
                if event[k][-1] == sipm:
                    current_qe = linear_interpolation(event[k][0])
                    if current_qe < np.random.sample() * 100: # моделируем фотоэффект
                        z += box_muller()
                else:
                    break
                k += 1
            if z / mean >= t:
                current_track.append(s_c) # добавляем в текущий трек координаты световода
            if k != i:
                i = k
            else:
                i += 1

        if len(current_track) != 0:
            reconstructed_tracks[-1] = current_track.copy()
    except Exception as err:
        pass

p = []
for i in range(len(reconstructed_tracks)):
    if len(reconstructed_tracks[i]) == 0:
        p.append(i)
for i in range(-1, -len(p) - 1, -1):
    reconstructed_tracks.pop(p[i])

with open("RECONSTRUCTED_TRACKS/" + f"{folder}_tracks.bin", 'wb') as l:
    pickle.dump(reconstructed_tracks, l)