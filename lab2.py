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
mid_borders = [round((border[0] + border[1])/2) for border in borders]
print_beautiful_interval_freq(buckets, borders)
C = mid_borders[max([(len(bucket), i) for i, bucket in enumerate(buckets)])[1]]
# h = mid_borders[1] - mid_borders[0]
h = int((mid_borders[-1] - mid_borders[0]) / (len(mid_borders)-1)) #  вроде работает, на за счёт округление может быть шляпа
print("C =", C)
print("h =", h)

table = [[0 for i in range(8)] for i in range(len(mid_borders)+1)]
for i, bucket in enumerate(buckets):
    xi = mid_borders[i]
    n = len(buckets[i])
    ui = (xi - C) / h
    table [i][0] = xi
    table[-1][0] += xi
    table [i][1] =  n
    table[-1][1] += n
    table [i][2] =  ui
    table[-1][2] += ui
    table [i][3] =  ui * n
    table[-1][3] += ui * n
    table [i][4] =  ui ** 2 * n
    table[-1][4] += ui ** 2 * n
    table [i][5] =  ui ** 3 * n
    table[-1][5] += ui ** 3 * n
    table [i][6] =  ui ** 4 * n
    table[-1][6] += ui ** 4 * n 
    table [i][7] =  (ui+1) ** 4 * n
    table[-1][7] += (ui+1) ** 4 * n


for row in table:
    print(row)

lhs = table[-1][6] + 4*table[-1][5] + 6*table[-1][4] + 4*table[-1][3] + table[-1][1]
rhs = table[-1][7]
print("\nПроверка:", lhs, "=", rhs, sep=" ")

n = table[-1][1]
M1 = table[-1][3] / n
M2 = table[-1][4] / n
M3 = table[-1][5] / n
M4 = table[-1][6] / n

print("\nНачальные выборочные моменты с 1 по 4:")
print("M1:{0:.4f}".format(M1))
print("M2:{0:.4f}".format(M2))
print("M3:{0:.4f}".format(M3))
print("M4:{0:.4f}".format(M4))
print()

m2 = (M2 - pow(M1,2)) * pow(h,2)
m3 = (M3 - 3*M2*M1 + 2*pow(M1,3)) * pow(h,3)
m4 = (M4 - 4*M3*M1 + 6*M2*pow(M1,2) - 3*pow(M1, 4)) * pow(h,4)
print("Центральные выборочные моменты:")
print("m2: {0:.4f}".format(m2))
print("m3: {0:.4f}".format(m3))
print("m4: {0:.4f}".format(m4))
print()

x_cherta = M1*h + C
Dv = m2
sigma = math.sqrt(Dv)
s2 = (n / (n-1)) * Dv
s = math.sqrt(s2)
As = m3 / pow(sigma, 3)
E = (m4 / pow(sigma, 4)) - 3
print("Оценка мат ожидания:", x_cherta)
print("Смещённая оценка дисперсии:", Dv)
print("Оценка среднеквадратичного отклонения:", sigma)
print("Исправленная оценка дисперсии", s2)
print("Исправленная оценка СКО", s)
print("Оценка асимметрии", As)
print("Оценка эксцесса", E)








# print_beautiful_interval_values(buckets, buckets)

# Задание: Для заданных выборочных данных вычислить с использованием метода моментов и условных вариант
# точечные статистические оценки математического ожидания, дисперсии, среднеквадратического отклонения,
#  асимметрии и эксцесса исследуемой случайной величины. Полученные результаты содержательно проинтерпретировать.

variation_series_density = Counter(sample_density)

# Проосто считаем

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




