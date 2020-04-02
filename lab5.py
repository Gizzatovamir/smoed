from math import sqrt
import lab1
import lab2
import lab4

n = lab1.selection_size    
general_population = lab1.read_data(filename=lab1.data_file_name)
sample_density = lab1.get_sample_first(general_population, n)
sample_elastic = lab1.get_sample_second(general_population, n)

table_x = lab2.build_table(sample_density)
mean_x, S_x = lab2.get_main_values_from_table(table_x)

table_y = lab2.build_table(sample_elastic)
mean_y, S_y = lab2.get_main_values_from_table(table_y)

r = lab4.get_correl_coef(sample_density, sample_elastic)

print("Для X:\n\tmean = {0:.2f}\n\tS = {1:.2f}".format(mean_x, S_x))
print("Для Y:\n\tmean = {0:.2f}\n\tS = {1:.2f}".format(mean_y, S_y))
print("Коэффициент корреляции: {0:.3f}".format(r))

coef_y_x = r * S_y / S_x
free_number_y_x = mean_y + coef_y_x*mean_x*(-1)
print(free_number_y_x)

coef_x_y = r * S_x / S_y    
free_number_x_y = mean_x + coef_x_y*mean_y*(-1)
print(free_number_x_y)


resudial_disp_x = pow(S_x,2) * pow(1-r, 2)
resudial_disp_y = pow(S_y,2) * pow(1-r, 2)
# print(resudial_disp_x, resudial_disp_y)

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax.plot(sample_density, sample_elastic, 'ok')

# min_val, max_val = min(sample_density), max(sample_density)
# y_minval = mean_y + coef_y_x*(min_val - mean_x)
# y_maxval = mean_y + coef_y_x*(max_val - mean_x)
# ax.plot([min_val, max_val], [y_minval, y_maxval], "-r", label="$y_x$ = 0.31x - 12.33") # yx

# min_val, max_val = min(sample_elastic), max(sample_elastic)
# print(min_val, max_val)
# x_minval = mean_x + coef_x_y*(min_val - mean_y)
# x_maxval = mean_x + coef_x_y*(max_val - mean_y)
# ax.plot([x_minval, x_maxval], [min_val, max_val], "-b", label="$x_y$ = 1.91y + 212.58") # xy
# ax.legend()
# # ax.set_xlabel('Варианты')
# # ax.set_ylabel('Абсолютная частота')
# ax.set_title('Прямые среднеквадратической регрессии')
# # fig.tight_layout()
# plt.show()


borders_x, buckets_x = lab1.get_interval_sample(sample_density)
borders_y, buckets_y = lab1.get_interval_sample(sample_elastic)
freqs_x = [len(array) for array in buckets_x]
freqs_y = [len(array) for array in buckets_y]
mid_borders_x = [(border[0] + border[1])/2 for border in borders_x]
mid_borders_y = [(border[0] + border[1])/2 for border in borders_y]

for elem in mid_borders_x:
    print("{0:.2f}".format(elem), end=" ")
print()
# print(freqs_x)

for elem in mid_borders_y:
    print("{0:.2f}".format(elem), end=" ")
print()
# print(freqs_y)

sample_2D = list(zip(sample_density, sample_elastic))
table = lab4.build_corr_table(sample_2D, borders_x, borders_y)
for row in table:
    print(row)
print(end="\n")

n_y = []
x_y_cherta = []
for i in range(len(table)):
    summ = 0
    num = 0
    for j in range(len(table)):
        num += table[j][i]
        summ += table[j][i] * mid_borders_x[j]
    n_y.append(num)
    x_y_cherta.append(summ / num)
# n_y[-1] +=1 

n_x = []
y_x_cherta = []
for i in range(len(table)):
    summ = 0
    num = 0
    for j in range(len(table)):
        num += table[i][j]
        summ += table[i][j] * mid_borders_y[j]
    n_x.append(num)
    y_x_cherta.append(summ / num)
# n_x[-1] += 1

D_o_xy = sum([n_x[i] * pow((mid_borders_x[i]-mean_x),2) for i in range(len(table))]) / n
sigma_x_xy = sqrt(D_o_xy)
D_m_xy = sum([n_y[i] * pow((x_y_cherta[i]-mean_x),2) for i in range(len(table))]) / n
sigma_xy = sqrt(D_m_xy)
nu_xy = sigma_xy / sigma_x_xy


print("D(общ): {0:.2f}".format(D_o_xy))
print("σ(x): {0:.2f}".format(sigma_x_xy))
print("D(меж): {0:.2f}".format(D_m_xy))
print("σ(xy): {0:.2f}".format(sigma_xy))
print("η(xy): {0:.3f}".format(nu_xy))

D_o_xy = sum([n_y[i] * pow((mid_borders_y[i]-mean_y),2) for i in range(len(table))]) / n
sigma_x_xy = sqrt(D_o_xy)
D_m_xy = sum([n_x[i] * pow((y_x_cherta[i]-mean_y),2) for i in range(len(table))]) / n
sigma_xy = sqrt(D_m_xy)
nu_xy = sigma_xy / sigma_x_xy

print()
print("D(общ): {0:.2f}".format(D_o_xy))
print("σ(x): {0:.2f}".format(sigma_x_xy))
print("D(меж): {0:.2f}".format(D_m_xy))
print("σ(yx): {0:.2f}".format(sigma_xy))
print("η(yx): {0:.3f}".format(nu_xy))


# 3 часть
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(sample_density, sample_elastic, 'ok')

sum_1 = sum([n_x[i] * mid_borders_x[i]**1 for i in range(len(table))])
sum_2 = sum([n_x[i] * mid_borders_x[i]**2 for i in range(len(table))])
sum_3 = sum([n_x[i] * mid_borders_x[i]**3 for i in range(len(table))])
sum_4 = sum([n_x[i] * mid_borders_x[i]**4 for i in range(len(table))])
sum_y_1 = sum([n_x[i] * y_x_cherta[i] * mid_borders_x[i]**1 for i in range(len(table))])
sum_y_2 = sum([n_x[i] * y_x_cherta[i] * mid_borders_x[i]**2 for i in range(len(table))])
sum_y_3 = sum([n_x[i] * y_x_cherta[i] * mid_borders_x[i]**0 for i in range(len(table))])
print(round(sum_1))
print(round(sum_2))
print(round(sum_3))
print(round(sum_4))
print(round(sum_y_1))
print(round(sum_y_2))
print(round(sum_y_3))

a = 1330980770795 / 7822224861288736
b = 1585312202138487 / 7822224861288736
c = (-574079274021227) / 7822224861288736
print()
print("a = {:.5f}".format(a))
print("b = {:.5f}".format(b))
print("c = {:.5f}".format(c))
print()

min_val, max_val = min(sample_density), max(sample_density)
xs = [min_val+((max_val-min_val)/10000*i) for i in range(10000)]
ys = [a*xs[i]**2 + b*xs[i] + c for i in range(10000)]
ax.plot(xs, ys, label="$y_x$") # yx




sum_1 = sum([n_y[i] * mid_borders_y[i]**1 for i in range(len(table))])
sum_2 = sum([n_y[i] * mid_borders_y[i]**2 for i in range(len(table))])
sum_3 = sum([n_y[i] * mid_borders_y[i]**3 for i in range(len(table))])
sum_4 = sum([n_y[i] * mid_borders_y[i]**4 for i in range(len(table))])
sum_y_1 = sum([n_y[i] * x_y_cherta[i] * mid_borders_y[i]**2 for i in range(len(table))])
sum_y_2 = sum([n_y[i] * x_y_cherta[i] * mid_borders_y[i]**1 for i in range(len(table))])
sum_y_3 = sum([n_y[i] * x_y_cherta[i] * mid_borders_y[i]**0 for i in range(len(table))])
print(round(sum_1))
print(round(sum_2))
print(round(sum_3))
print(round(sum_4))
print(round(sum_y_1))
print(round(sum_y_2))
print(round(sum_y_3))

a = 3400468111 / 11432286831000
b = 24837124860883 / 11432286831000
c = 7906387274955121 / 45729147324000
print()
print("a = {:.5f}".format(a))
print("b = {:.5f}".format(b))
print("c = {:.5f}".format(c))
print()

min_val, max_val = min(sample_elastic), max(sample_elastic)
ys = [min_val+((max_val-min_val)/10000*i) for i in range(10000)]
xs = [a*ys[i]**2 + b*ys[i] + c for i in range(10000)]
ax.plot(xs, ys, label="$x_y$")

ax.legend()
ax.set_title('Уравнения параболической регрессии')
plt.show()