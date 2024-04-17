import numpy as np


def get_data_from_event(file):
    f = open(file, 'r')
    data = [list(map(float, el.split('\t'))) for el in f.readlines()[1:]]
    f.close()
    return data


def get_data_from_matrix(file): # удобное чтение файлов
    f = open(file, 'r')
    data = [[el.split('\t')[0]] + list(map(float, el.split('\t')[1:])) for el in f.readlines()[1:]]
    f.close()
    return data


def binary_search(list, key): # бинарный поиск
    low = 0
    high = len(list) - 1

    while low <= high:
        mid = (low + high) // 2
        midVal = list[mid]
        if midVal == key:
            return mid, 1
        if midVal > key:
            high = mid - 1
        else:
            low = mid + 1
    return mid, 0


def mse(x, y): # мнк
    xy = [x[i] * y[i] for i in range(len(x))]
    x2 = [x[i] ** 2 for i in range(len(x))]
    
    k = (len(x) * sum(xy) - sum(x) * sum(y)) / (len(x) * sum(x2) - sum(x) ** 2)
    b = (sum(y) - k * sum(x)) / len(x)
    
    return [k, b]


def linear_interpolation(energy):
    ind, _ = binary_search(qe_e, energy)
    if energy > qe_e[ind]:
        ind += 1
    k = (qe_q[ind] - qe_q[ind - 1]) / (qe_e[ind] - qe_e[ind - 1])
    b = qe_q[ind] - k * qe_e[ind]
    return k * energy + b # с помощью метода линейной интерполяции нашли нужную квантовую эффективность


def box_muller():
    r, phi = np.random.sample(), np.random.sample() # метод Бокса-Мюллера
    z = np.cos(2 * np.pi * phi) * np.sqrt(-2 * np.log(r))
    return mean + sigma * z


mean = 0.201912 # средняя амплитуда сигнала на 1 фотоэлектрон
sigma =  0.034257 # стандартное отклонение
events_path = "EVENTS_DATA" # расположение папки с данными
matrix_path = "CHARGED_MATRIX" # расположение папки с данными
count_in_plane = 96 * 2 # число стрипов в плоскости
qe_e = [el[0] for el in get_data_from_event("PDE_data.dat")] # энергии фотонов
qe_q = [el[1] for el in get_data_from_event("PDE_data.dat")] # квантовые эффективности
coord = [-(500 - 7 - 0.1), -(500 - 14 - 0.2 - 7 - 0.1), -(0.1 + 7 + 0.1), 0.1 + 7 + 0.1, 500 - 14 - 0.2 - 7 - 0.1, 500 - 7 - 0.1] # координаты центров плосокстей
sipm_coords = [] # координаты световодов
coord = [-(500 - 7 - 0.1), -(500 - 14 - 0.2 - 7 - 0.1), -(0.1 + 7 + 0.1), 0.1 + 7 + 0.1, 500 - 14 - 0.2 - 7 - 0.1, 500 - 7 - 0.1]
for i in range(0, 1152):
    x = i // 96
    if x % 4 == 0:
        sipm_coords.append((-500 + 10.2 + (10.2 + 0.2) * (i % 96), None, (coord[i // (96 * 2)] - 3.5 - 0.1)))
    elif x % 4 == 1:
        sipm_coords.append((-500 + 10.2 / 2 + (10.2 + 0.2) * (i % 96), None, coord[i // (96 * 2)] + 3.5 + 0.1))
    elif x % 4 == 2:
        sipm_coords.append((None, -500 + 10.2 + (10.2 + 0.2) * (i % 96), coord[i // (96 * 2)] - 3.5 - 0.1))
    elif x % 4 == 3:
        sipm_coords.append((None, -500 + 10.2 / 2 + (10.2 + 0.2) * (i % 96) ,coord[i // (96 * 2)] + 3.5 + 0.1))
