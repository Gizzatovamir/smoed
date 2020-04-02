from math import sqrt, log, exp
import lab1

def print_beauty(sample: list, size):
    for i in range(1, len(sample)+1):
        print(sample[i-1], end='\t')
        if i % size == 0:
            print(end="\n")

def check(value_1, value_2, border_1, border_2):
    is_1_in_interval  = value_1 >= border_1[0] and value_1 <= border_1[1]
    is_2_in_interval = value_2 >= border_2[0] and value_2 <= border_2[1]
    return is_1_in_interval and is_2_in_interval

def build_corr_table(sample_2D, borders_1, borders_2):
    table = []
    for i in range(len(borders_1)):
        table.append([])
        for j in range(len(borders_2)):
            tmp = map(lambda x: check(x[0], x[1], borders_1[i], borders_2[j]), sample_2D)
            table[i].append(sum(tmp))
    return table

def countSum(table, v, u):
    sum_from_table = 0
    for i in range(7):
        for j in range(7):
            sum_from_table += table[i][j] * v[i] * u[j]
    return sum_from_table

def get_correl_coef(sample_density, sample_elastic):
    import lab1
    n = lab1.selection_size
    sample_2D = list(zip(sample_density, sample_elastic))
    borders_1, buckets_1 = lab1.get_interval_sample(sample_density)
    borders_2, buckets_2 = lab1.get_interval_sample(sample_elastic)
    freqs_1 = [len(array) for array in buckets_1]
    freqs_2 = [len(array) for array in buckets_2]
    mid_borders_1 = [(border[0] + border[1])/2 for border in borders_1]
    mid_borders_2 = [(border[0] + border[1])/2 for border in borders_2]
    step_size_1 = borders_1[0][1] - borders_1[0][0]
    step_size_2 = borders_2[0][1] - borders_2[0][0]
    C_1 = 472 # из прошлых работ
    C_2 = 122
    # СКО для условных вариант
    v = [(elem - C_1) / step_size_1 for elem in mid_borders_1]
    u = [(elem - C_2) / step_size_2 for elem in mid_borders_2]
    mean_v = sum([x[0] * x[1] for x in zip(v, freqs_1)]) / n
    mean_u = sum([x[0] * x[1] for x in zip(u, freqs_2)]) / n
    S_v = sqrt(sum([x[0]**2 * x[1] for x in zip(v, freqs_1)]) / n - mean_v**2)
    S_u = sqrt(sum([x[0]**2 * x[1] for x in zip(u, freqs_2)]) / n - mean_u**2)

    table = build_corr_table(sample_2D, borders_1, borders_2)
    sum_from_table = countSum(table, v, u)

    r = (sum_from_table + n * mean_v * mean_u) / (n * S_v * S_u)
    return r


if __name__ == "__main__":
    n = lab1.selection_size
    general_population = lab1.read_data(filename=lab1.data_file_name)
    sample_density = lab1.get_sample_first(general_population, n)
    sample_elastic = lab1.get_sample_second(general_population, n)

    borders_1, buckets_1 = lab1.get_interval_sample(sample_density)
    borders_2, buckets_2 = lab1.get_interval_sample(sample_elastic)
    freqs_1 = [len(array) for array in buckets_1]
    freqs_2 = [len(array) for array in buckets_2]
    # Расчёты прогоняем, меняя источник данных в лабе 2

    # Часть 2
    sample_2D = list(zip(sample_density, sample_elastic))
    print("Двумерная выборка:")
    print_beauty(sample_2D, size=6)
    print(end="\n")

    table = build_corr_table(sample_2D, borders_1, borders_2)
    print("Данные для таблицы:")
    for row in table:
        print(row)
    print(end="\n")

    mid_borders_1 = [(border[0] + border[1])/2 for border in borders_1]
    mid_borders_2 = [(border[0] + border[1])/2 for border in borders_2]
    step_size_1 = borders_1[0][1] - borders_1[0][0]
    step_size_2 = borders_2[0][1] - borders_2[0][0]
    C_1 = 472 # из прошлых работ
    C_2 = 122

    # Условные варианты
    v = [(elem - C_1) / step_size_1 for elem in mid_borders_1]
    u = [(elem - C_2) / step_size_2 for elem in mid_borders_2]

    # средние для условных вариант
    mean_v = sum([x[0] * x[1] for x in zip(v, freqs_1)]) / n
    mean_u = sum([x[0] * x[1] for x in zip(u, freqs_2)]) / n

    # СКО для условных вариант
    S_v = sqrt(sum([x[0]**2 * x[1] for x in zip(v, freqs_1)]) / n - mean_v**2)
    S_u = sqrt(sum([x[0]**2 * x[1] for x in zip(u, freqs_2)]) / n - mean_u**2)

    print('u: Среднее: {0:.3f}, СКО: {1:.3f}'.format(mean_u, S_u))
    print('v: Среднее: {0:.3f}, СКО: {1:.3f}'.format(mean_v, S_v))
    print(end="\n")

    sum_from_table = countSum(table, v, u)
    print(sum_from_table)
    # коэффициент корреляции Пирсона
    r = (sum_from_table + n * mean_v * mean_u) / (n * S_v * S_u)
    print('Коэффициент корреляции П ирсона {0:.4f}'.format(r))

    # нахождение доверительного интервала
    z = 0.5 * log((1 + r)/(1 - r))
    # доверительный интервал для z
    left  = z - 1.96 / sqrt(n - 3)
    right = z + 1.96 / sqrt(n - 3)
    print('Доверительный интервал для Z: ({0:.3f}, {1:.3f})'.format(left, right))
    # обратное преобразование
    left  = (exp(2 * left) - 1) / (exp(2 * left) + 1)
    right = (exp(2 * right) - 1) / (exp(2 * right) + 1)
    print('Доверительный интервал: ({0:.3f}, {1:.3f})'.format(left, right))

    # проверка гипотезы
    t_sample = r * sqrt(n-2) / sqrt(1 - r**2)
    t_cr = 1.98
    print(t_cr)

    print('t выборочное  = {0:.3f}'.format(t_sample))
    print('t критическое = {0:.3f}'.format(t_cr))
    if t_sample <= t_cr:
        print('Не достаточно отснований, чтобы отклонить H0')
    else:
        print('Отвергаем гипотезу H0')