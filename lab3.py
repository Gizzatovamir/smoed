import lab1
import lab2

general_population = lab1.read_data(filename=lab1.data_file_name)
sample = lab1.get_sample(general_population, lab1.selection_size)
sample_density = [pair.density for pair in sample]
table = lab2.build_table(sample_density)
X, S = lab2.get_main_values_from_table(table)

print(X, S)

