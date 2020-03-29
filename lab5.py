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

print("Для X:\n\tmean = {0:.3f}\n\tS = {1:.2f}".format(mean_x, S_x))
print("Для Y:\n\tmean = {0:.3f}\n\tS = {1:.2f}".format(mean_y, S_y))
print("Коэффициент корреляции: {0:.3f}".format(r))
