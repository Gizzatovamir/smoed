from lab1 import *

general_population = read_data(filename=data_file_name)
sample = get_sample(general_population, selection_size)
sample_density = [pair.density for pair in sample]

print("\nСформированная выборка:")
print_beautiful_sample(sample_density)

borders, buckets = get_interval_sample(sample_density)
print_beautiful_interval_freq(buckets, borders)
print_beautiful_interval_values(buckets, buckets)

# Задание: Для заданных выборочных данных вычислить с использованием метода моментов и условных вариант
# точечные статистические оценки математического ожидания, дисперсии, среднеквадратического отклонения,
#  асимметрии и эксцесса исследуемой случайной величины. Полученные результаты содержательно проинтерпретировать.

# Метод моментов
