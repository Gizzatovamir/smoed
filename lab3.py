import lab1
import lab2
from scipy.stats import t, chi2
from scipy.special import erf
Ф = lambda x: erf(x/2**0.5)/2 # функция лапласа
from math import sqrt

def print_2digits(list, string):
    print(string)
    for elem in list:
        print("{0:.2f}".format(elem), end=" ")
    print(end="\n")

N = lab1.selection_size # 96
n = N-1 # 95

general_population = lab1.read_data(filename=lab1.data_file_name)
sample = lab1.get_sample(general_population, lab1.selection_size)
sample_density = [pair.density for pair in sample]
table = lab2.build_table(sample_density)
X, S = lab2.get_main_values_from_table(table)

print("С прошлой работы получим значения:\nX = {0:.2f}\nS = {1:.2f}".format(X, S))
igrek = 0.95
t_igrek = 1.9855


a_left = X - t_igrek * S / sqrt(N)
a_right = X + t_igrek * S / sqrt(N)
print("Доверительный интервал для математического ожидания: ", end="")
print("({0:.4f}; {1:.4f})\n".format(a_left, a_right))

gamma = 0.95
q = 0.147

sd_left = S*(1-q)
sd_right = S*(1+q)
print("Доверительный интервал для среднеквадратического отклонения: ",  end="")
print("({0:.4f}; {1:.4f})\n".format(sd_left, sd_right))



borders, buckets = lab1.get_interval_sample(sample_density)
# print(borders, buckets)
vals = [len(bucket) for bucket in buckets]
# print(borders)
# print(buckets)
print("Частоты в интервалах:")
print(vals)
print()

# Объединяем последние интервалы
borders[-2] = (borders[-2][0], borders[-1][1])
del borders[-1]
buckets[-2] += buckets[-1]
del buckets[-1]
vals = [len(bucket) for bucket in buckets]
# print(borders)
# print(buckets)
print("Частоты в интервалах после:")
print(vals)
print()


# границы интервалов в интервальном ряду
bins = [elem[0] for elem in borders] + [borders[-1][1]]
print_2digits(bins, "Границы интервалов:")

# # стандартизуем границы интервалов
z = [(e - X)/S for e in bins]
z[0] = -float('inf')
z[-1] = float('inf')
print_2digits(z, "Значения Z:")

p = []
for i in range(1, len(z)):
    p.append(Ф(z[i])-Ф(z[i-1]))
print_2digits(p, "Вероятности попадания в интервалы:")
print(end="\n")
    
# freq_theor = list(map(lambda x: x*n, p))
freq_theor = [x*N for x in p]
print_2digits(freq_theor, "Теоретические частоты по интервалам:")
print(end="\n")

freq_expect = vals
print_2digits(freq_expect, "Ожидаемые частоты по интервалам:")
print(end="\n")

# посчитаем статистику критерия Хи-квадрат
stats_crit = []
for i in range(len(freq_expect)):
    stats_crit.append((freq_expect[i] - freq_theor[i])**2/freq_theor[i])
chi2_calculated = sum(stats_crit)
print("Cтатистики критерия Хи-квадрат:")
for elem in stats_crit:
    print("{0:.4f}".format(elem), end=" ")
print(end="\n")
print('Общее значение: {}'.format(chi2_calculated))
print(end="\n")


k = 5 # число интервалов
l = 2 # число параметров
alpha = 0.05 # уровень значимости
# критическое значение статистики критерия
chi2_criterion = chi2.ppf(1-alpha, df=k-l-1)
print('Критическое значение: {}'.format(chi2_criterion))

# принимаем решение
if chi2_calculated > chi2_criterion:
    print('Отвергаем гипотезу H0')
else:
    print('Не отвергем гипоетезу H0')


