from collections import namedtuple
from collections import Counter
import random
import math
from operator import attrgetter
Measurement = namedtuple("Measurement", ['density', 'elastic'])

selection_size = 96 # объём выборочной совокупности
data_file_name = "Tabl.txt"
sample_seed = 120 # None to random # Зерно для выборки, константа, чтобы всегда одинаково
block_output_size = 17 # (c учётом, что на одну запись уходит 6 символов(с пробелом))

def read_data(filename):
    # Извлекаем из файла данные и формируем генеральную совокупность.
    general_population = []
    with open(filename) as file:
        for line in file:
            line = line.replace(',', '.').replace(' ', '').strip().split("\t")
            general_population += [Measurement(float(line[i]), float(line[i+1])) for i in range(0, len(line), 2) if line[i]]
    return general_population

def get_sample(gen_pop, size_of_gen_pop):
    # Формируем выборку из генеральной совокупности
    prev_state = random.getstate()
    random.seed(sample_seed)
    sample = random.sample(gen_pop, size_of_gen_pop)
    random.setstate(prev_state)
    return sample

def print_beautiful_sample(sample: list):
    for i, value in enumerate(sample):
        if i % block_output_size == 0 and i != 0:
            print(end="\n")
        print(value, end=" ")
    print(end="\n")

def print_beautiful_variation(variation: Counter):
    sorted_density_values = list(sorted(variation_series_density))
    for i in range(int(len(variation)/block_output_size) + 1):
        for index in range(i*block_output_size, (i+1)*block_output_size):
            if index >= len(variation): break
            key = sorted_density_values[index]
            print("{0:^6}".format(key), end="")
        print()
        for index in range(i*block_output_size, (i+1)*block_output_size):
            if index >= len(variation): break
            key = sorted_density_values[index]
            print("{0:^6}".format(variation[key]), end="")
        print()


general_population = read_data(filename=data_file_name)
sample = get_sample(general_population, selection_size)
sample_density = [pair.density for pair in sample]
sample_elastic = [pair.elastic for pair in sample]

print("\nСформированная выборка:")
print_beautiful_sample(sample_density)

# ranked_row = sorted(sample, reverse=False, key=attrgetter('density'))
ranked_row = sorted(sample_density)
print("\nРанжированный ряд (по возрастанию): ")
print_beautiful_sample(ranked_row)

# Вариационный ряд значений плотности
variation_series_density = Counter(sample_density)
print("\nВариационный ряд:")
print_beautiful_variation(variation_series_density)

# Для интервального ряда нужно оценить длину частичного интервала
# Для этого воспользуемся формулой Стерджеса: k = 1 + 3.322*log10(n)
buckets_number = int(1 + 3.322 * math.log10(selection_size))
min_density, max_density = min(sample_density), max(sample_density)
range_density = max_density - min_density
print("\nИспользуя формулу Стерджеса рассчитаем количество групп для разбиения выборки:")
print("1 + 3.322*lg({0}) = {1}".format(selection_size, buckets_number))
print("Минимальное значение ряда: ", min_density)
print("Максимальное значение ряда:", max_density)
print("Размах выборки", range_density)

isInBucket = lambda x: min(int((abs(x) - min_density) / range_density * buckets_number), buckets_number-1)
borders = [(min_density + range_density/buckets_number*i, min_density + range_density/buckets_number*(i+1)) for i in range(buckets_number)]
buckets = [[] for i in range(buckets_number)]
for value in sample_density:
    buckets[isInBucket(value)].append(value)
print("\nИнтервальный ряд со значениями:")
for i, border in enumerate(borders):
    if i != len(borders)-1:
        print("[{0:.3f} - {1:.3f}):".format(border[0], border[1]), end=" ")
    else:
        print("[{0:.3f} - {1:.3f}]:".format(border[0], border[1]), end=" ")
    for elem in buckets[i]:
        print(elem, end=" ")
    print(end="\n")

print("\nИнтервальный ряд с частотами:")
print("|       Интервал      | Абс. частота | Отн. частота |")
for i, border in enumerate(borders):
    if i != len(borders)-1:
        print("| [{0:.3f} - {1:.3f}) |".format(border[0], border[1]), end=" ")
    else:
        print("| [{0:.3f} - {1:.3f}] |".format(border[0], border[1]), end=" ")
    print("{0:^13.3f}| {1:^13.3f}|".format(len(buckets[i]), len(buckets[i])/selection_size))


# --------------------------------- Рисуночки! ---------------------------------

import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
# Гистограммы
fig, ax = plt.subplots()
ax.hist(sample_density, bins=buckets_number, density=False, edgecolor='black', facecolor='blue')
center_of_borders = [(border[0] + border[1])/2 for border in borders]
y = [len(bucket) for bucket in buckets]
ax.plot(center_of_borders, y, '--')
ax.set_xlabel('Варианты')
ax.set_ylabel('Абсолютная частота')
ax.set_title('Гистограмма абсолютных частот')
fig.tight_layout()
plt.show()

fig, ax = plt.subplots()
ax.hist(sample_density, buckets_number, weights=np.ones(len(sample_density)) / len(sample_density), density=False, edgecolor='black', facecolor='blue')
center_of_borders = [(border[0] + border[1])/2 for border in borders]
y = [len(bucket)/selection_size for bucket in buckets]
ax.plot(center_of_borders, y, '--')
ax.set_xlabel('Варианты')
ax.set_ylabel('Относительная частота')
ax.set_title('Гистограмма относительных частот')
fig.tight_layout()
plt.show()
