import lab1
import random
from collections import Counter

def get_sample(gen_pop, size_of_gen_pop, seed):
    # Формируем выборку из генеральной совокупности
    random.seed(seed)
    # random.setstate(seed)
    sample = random.sample(gen_pop, size_of_gen_pop)
    return sample


general_population = lab1.read_data(filename=lab1.data_file_name)
sample_density = [409.00, 483.00, 489.00, 484.00, 471.00, 432.00, 418.00, 493.00, 376.00, 452.00, 542.00, 560.00, 406.00, 541.00, 475.00, 377.00, 351.00, 441.00, 358.00, 480.00, 394.00, 415.00, 585.00, 437.00, 437.00, 479.00, 496.00, 393.00, 481.00, 470.00, 453.00, 522.00, 473.00, 430.00, 493.00, 623.00, 395.00, 412.00, 406.00, 433.00, 498.00, 460.00, 523.00, 478.00, 371.00, 442.00, 477.00, 388.00, 525.00, 503.00, 466.00, 438.00, 411.00, 464.00, 422.00, 431.00, 465.00, 426.00, 468.00, 366.00, 460.00, 448.00, 427.00, 443.00, 429.00, 383.00, 513.00, 495.00, 466.00, 454.00, 498.00, 396.00, 400.00, 482.00, 428.00, 446.00, 320.00, 433.00, 484.00, 464.00, 462.00, 451.00, 362.00, 547.00, 448.00, 441.00, 458.00, 449.00, 434.00, 443.00, 505.00, 487.00, 344.00, 452.00, 502.00, 400.00, 576.00, 405.00]
sample_elastic = [116.70 , 143.40 , 149.80 , 147.50 , 143.90 , 123.00 , 118.40 , 154.50 , 103.10 , 116.10 , 146.10 , 169.80 , 113.80 , 146.80 , 143.60 , 97.80 , 89.00 , 126.10 , 98.30 , 114.00 , 112.10 , 107.10 , 177.70 , 129.20 , 115.10 , 138.70 , 141.70 , 103.20 , 135.20 , 143.90 , 138.20 , 143.80 , 136.40 , 104.30 , 151.20 , 195.70 , 109.10 , 127.80 , 110.10 , 131.50 , 139.30 , 122.40 , 148.70 , 126.60 , 91.90 , 126.20 , 139.70 , 105.60 , 162.10 , 146.60 , 130.30 , 120.70 , 112.90 , 131.30 , 115.70 , 125.00 , 140.70 , 129.10 , 128.60 , 93.60 , 124.50 , 137.70 , 125.80 , 141.60 , 120.90 , 107.40 , 159.30 , 150.90 , 137.90 , 131.10 , 145.50 , 90.10 , 114.60 , 148.20 , 130.30 , 130.30 , 72.60 , 130.00 , 140.40 , 143.20 , 135.70 , 128.60 , 84.30 , 154.70 , 121.90 , 140.80 , 104.70 , 124.50 , 110.50 , 121.90 , 155.80 , 146.00 , 86.80 , 119.70 , 132.50 , 106.30 , 170.10 , 107.50]
sample2D = list(zip(sample_density, sample_elastic))

variation_series_density = Counter(sample2D)
indexes = []
for elem_2 in sample_density:
    for i, elem in enumerate(general_population):
        if elem.density == elem_2:
           indexes.append(i) 
           break
print(indexes)
print(len(indexes) == len(set(indexes)))
print(len(indexes))
print(Counter(indexes))
print(sample2D[18])
for i, elem in enumerate(sample2D):
    if elem[0] == sample2D[18][0] and elem[1] == sample2D[18][1]:
        print(elem)
print(Counter([elem.density for elem in general_population]))

    

# seed = 0
# max_elems = 0
# while True:
#     sample = get_sample(general_population, 98, seed)
#     sample = set([x[0] for x in sample])
#     communizm = sample.intersection(sample_density)
#     if len(communizm) > max_elems:
#         max_elems = len(communizm)
#         print("Seed:", seed, "Eq: ", len(communizm))
#     seed += 1
#     if (communizm == 98):
#         break
        