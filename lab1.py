from collections import namedtuple
from collections import Counter
import random
import math
from operator import attrgetter
Measurement = namedtuple("Measurement", ['density', 'elastic'])

selection_size = 96 # объём выборочной совокупности
data_file_name = "Tabl.txt"
sample_seed = 120 # None to random
block_output_size = 17

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

def print_beautiful_variation(variation):
    # Input: Counter
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

# Ранжированный ряд (по возрастанию плотности)
ranked_row = sorted(sample, reverse=False, key=attrgetter('density'))

# Вариационный ряд значений плотности
variation_series_density = Counter(sample_density)
print_beautiful_variation(variation_series_density)

# print(variation_series_density)
# for x, y in ranked_row:
#     print(x,y)
# print(ranked_row)

# Для интервального ряда нужно оценить длину частичного интервала
# Для этого воспользуемся формулой Стерджеса: k = 1 + 3.322*log10(n)
buckets_number = int(1 + 3.322 * math.log10(selection_size))
print(buckets_number)
min_val, max_val = min(sample_density), max(sample_density)
range_density = max_val - min_val
print("Размах выборки плотности:", range_density)
fn = lambda x: min(int((abs(x) - min_val) / range_density * buckets_number), buckets_number-1)
print(list(map(fn, sample_density)))

buckets = [[] for i in range(buckets_number)]
borders = [(min_val + range_density/buckets_number*i, min_val + range_density/buckets_number*(i+1)) for i in range(buckets_number)]
print(borders)
for value in sample_density:
    buckets[fn(value)].append(value)
for num, bucket in enumerate(buckets):
    print(num, ") ", sep="", end="")
    print(bucket)

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(sample_density, buckets_number, density=False, edgecolor='black')
print(n, bins)

ax.set_xlabel('Значение плотности')
ax.set_ylabel('Относительная частота')
ax.set_title(r'Гистограмма плотности')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()



            

