from lab1 import *
from collections import Counter


# def get_math_expectation_moment():
#     math_expectation = 0
#     elems_num = 0
#     for key, value in variation_series_density.items():
#         math_expectation += key * value
#         elems_num += value
#         print(key, "*", value)
#     print(math_expectation, "/", elems_num)
#     math_expectation /= elems_num

#     print(math_expectation)

general_population = read_data(filename=data_file_name)
sample = get_sample(general_population, selection_size)
sample_density = [pair.density for pair in sample]

# print("\nСформированная выборка:")
# print_beautiful_sample(sample_density)

borders, buckets = get_interval_sample(sample_density)
print_beautiful_interval_freq(buckets, borders)
# print_beautiful_interval_values(buckets, buckets)

# Задание: Для заданных выборочных данных вычислить с использованием метода моментов и условных вариант
# точечные статистические оценки математического ожидания, дисперсии, среднеквадратического отклонения,
#  асимметрии и эксцесса исследуемой случайной величины. Полученные результаты содержательно проинтерпретировать.

variation_series_density = Counter(sample_density)

# Метод моментов

math_expectation = 0
elems_num = 0
for key, value in variation_series_density.items():
    math_expectation += key * value
    elems_num += value
print(math_expectation, "/", elems_num)
math_expectation /= elems_num
print("Мат ождиание: {:.3f}".format(math_expectation))


dispersion = math.sqrt(sum([pow(xi - math_expectation, 2) for xi in sample_density]) / (selection_size - 1))
print("Дисперсия: {:.3f}".format(dispersion))




