from math import sqrt
import matplotlib.pyplot as plt
import copy
import lab1

K_num = 6

def calcFirstCenters(sameple):
    # Прикидываем центры для начала работы
    min_elem, max_elem = min(sameple), max(sameple)
    step = (max_elem - min_elem) / (K_num)
    borders = [min_elem]
    for i in range(K_num):
        borders.append(borders[i] + step)
    
    centers = []
    for i in range(K_num):
        centers.append((borders[i] + borders[i+1]) / 2)
    return centers

def findRealClosestPointIndex(im_point, sample):
    # Ищем наиболее близкие точки в реальной выборке наивным поиском
    indexOfMin = 0
    currMinDistance = getDistance(im_point, sample[0])
    for i in range(1, len(sample)):
        dist = getDistance(im_point, sample[i])
        if dist < currMinDistance:
            currMinDistance = dist
            indexOfMin = i
    return indexOfMin

def getDistance(point_1, point_2):
    # Евклидово расстояние с поправочным на масштаб коэффициентом
    return sqrt((pow(point_2[0] - point_1[0], 2) + pow(ncf*(point_2[1] - point_1[1]),2)))

def findClosestCluster(point, centers):
    ds = [getDistance(point, center) for center in centers]
    return ds.index(min(ds))

def recalcClusterCenter(cluster, cl_index, centers):
    mid_x = sum([elem[0] for elem in cluster]) / len(cluster)
    mid_y = sum([elem[1] for elem in cluster]) / len(cluster)
    centers[cl_index] = [mid_x, mid_y]

def recalcAllCenters(clusters, centers):
    for i, cluster in enumerate(clusters):
        recalcClusterCenter(cluster, i, centers)

def initData(sample_density, sample_elastic):
    #  Инициализируем 
    sample_2D = list(zip(sample_density, sample_elastic))
    im_centers = list(zip(calcFirstCenters(sample_density), calcFirstCenters(sample_elastic)))
    pointsPull = sample_2D[:]
    centers = []
    for im_center in im_centers:
        indexOfRealPoint = findRealClosestPointIndex(im_center, pointsPull)
        print(indexOfRealPoint)
        centers.append(sample_2D[indexOfRealPoint])
        del pointsPull[indexOfRealPoint]
    clusters = [[centers[i]] for i in range(K_num)]
    return clusters, centers, pointsPull

def compareClusters(clusters_1, clusters_2):
    if len(clusters_1) != len(clusters_2):
        return False
    for i in range(K_num):
        if len(clusters_1[i]) != len(clusters_2[i]):
            return False
        for j in range(len(clusters_2[i])):
            if clusters_1[i][j] != clusters_2[i][j]:
                return False
    return True

def F_1(clusters, centers):
    result = 0
    for i, cluster in enumerate(clusters):
        for elem in cluster:
            result += getDistance(elem, centers[i])
    return result

def F_2(clusters):
    result = 0
    for cluster in clusters:
        for i in range(len(cluster)):
            for j in range(i, len(cluster)):
                result += getDistance(cluster[i], cluster[j])
    return result

def F_3(clusters, centers):
    result = 0
    for i, cluster in enumerate(clusters):
        sigma = 0
        for elem in cluster:
            sigma += pow(getDistance(elem, centers[i]), 2)
        sigma /= len(cluster)
        result += sigma
    return result

def k_algo_1(sample_density, sample_elastic):
    # Первый вариант - пересчитываем центр после каждого обновления кластера
    clusters, centers, pointsPull = initData(sample_density, sample_elastic)
    print("Начальные центры:")
    for elem in centers:
        print("({0:.2f}; {1:.2f})".format(elem[0], elem[1]), end=" ")
    print(end="\n")
    old_clusters = []

    for i in range(20):
        for point in pointsPull:
            index = findClosestCluster(point, centers)
            clusters[index].append(point)
            recalcClusterCenter(clusters[index], index, centers)
        pointsPull = list(zip(sample_density, sample_elastic))

        if i == 19:
            print("Найдено устойчивое состояние! {0} совпадает с {1}".format(i, i+1))

            colors = ["blue", "red", "yellow", "black", "green", "cyan", "grey", "blue", "red", "yellow"]
            fig, ax = plt.subplots()
            for j, cluster in enumerate(clusters):
                for point in cluster:
                    ax.plot(point[0], point[1], 'o', color=colors[j], alpha=0.5)
            for j, center in enumerate(centers):
                ax.plot(center[0], center[1], 'x', color=colors[j])
            plt.title("Финал алгоритма с пересчётом на каждом шаге")
            plt.show()
            break
        else:
            print("{} шаг процедуры:".format(i+1))
            for elem in centers:
                print("({0:.2f}; {1:.2f})".format(elem[0], elem[1]), end=" ")
            print(end="\n")
            print("F1: {:.2f}".format(F_1(clusters, centers)))
            print("F2: {:.2f}".format(F_2(clusters)))
            print("F3: {:.2f}".format(F_3(clusters, centers)))
            print(end="\n")

            old_clusters = copy.deepcopy(clusters)
            clusters.clear()
            for _ in range(len(old_clusters)):
                clusters.append([])


def k_algo_2(sample_density, sample_elastic):
    print("Начало алгоритма с пересчётом центра после просмотра всех данных")
    clusters, centers, pointsPull = initData(sample_density, sample_elastic)
    print("Начальные центры:")
    for elem in centers:
        print("({0:.2f}; {1:.2f})".format(elem[0], elem[1]), end=" ")
    print(end="\n")
    old_clusters = []

    for i in range(20):
        for point in pointsPull:
            index = findClosestCluster(point, centers)
            clusters[index].append(point)
        recalcAllCenters(clusters, centers) # Пересчитываем центры после подсчёт статистики

        if compareClusters(clusters, old_clusters):
            print("Найдено устойчивое состояние! {0} совпадает с {1}".format(i, i+1))
            
            colors = ["blue", "red", "yellow", "black", "green", "cyan", "grey", "blue", "red", "yellow"]
            fig, ax = plt.subplots()
            for j, cluster in enumerate(clusters):
                for point in cluster:
                    ax.plot(point[0], point[1], 'o', color=colors[j], alpha=0.5)
            for j, center in enumerate(centers):
                ax.plot(center[0], center[1], 'x', color=colors[j])
            plt.title("Финал алгоритма с пересчётом после всей итерации")
            plt.show()
            break
        else:
            print("{} шаг процедуры:".format(i+1))
            for elem in centers:
                print("({0:.2f}; {1:.2f})".format(elem[0], elem[1]), end=" ")
            print(end="\n")
            print("F1: {:.2f}".format(F_1(clusters, centers)))
            print("F2: {:.2f}".format(F_2(clusters)))
            print("F3: {:.2f}".format(F_3(clusters, centers)))
            print(end="\n")

            pointsPull = list(zip(sample_density, sample_elastic))
            old_clusters = copy.deepcopy(clusters)
            clusters.clear()
            for _ in range(len(old_clusters)):
                clusters.append([])



n = lab1.selection_size    
general_population = lab1.read_data(filename=lab1.data_file_name)
sample_density = lab1.get_sample_first(general_population, n)
sample_elastic = lab1.get_sample_second(general_population, n)
n = 98

sample_density = [480, 393, 482, 408, 542, 486, 405, 452, 483, 465, 474, 359, 487, 473, 510, 442, 569, 331, 437, 421, 484, 504, 440, 390, 490, 443, 532, 522, 426, 411, 484, 467, 453, 496, 344, 443, 423, 463, 396, 421, 330, 547, 482, 514, 472, 545, 386, 463, 415, 461, 386, 468, 362, 433, 438, 560, 393, 525, 453, 396, 434, 508, 463, 340, 321, 488, 566, 514, 593, 412, 403, 412, 320, 503, 391, 434, 468, 523, 351, 505, 502, 406, 518, 437, 506, 449, 547, 402, 399, 440, 392, 416, 481, 395, 500, 465, 496, 462]
sample_elastic = [153.30, 122.80, 136.40, 110.00, 146.10, 139.40, 103.60, 140.50, 143.40, 127.70, 132.50, 71.900, 146.00, 136.40, 129.40, 115.40, 157.40, 74.100, 124.30, 124.20, 140.40, 143.80, 128.50, 108.10, 139.90, 135.70, 158.70, 154.50, 119.00, 112.90, 147.50, 113.00, 119.50, 143.10, 86.800, 122.90, 131.10, 129.20, 90.100, 118.00, 71.100, 154.70, 139.90, 153.60, 134.20, 145.30, 105.80, 121.20, 119.70, 138.60,95.500, 128.90, 97.900, 128.20, 134.10, 169.80, 103.20, 156.50, 124.20, 83.800, 122.30, 159.00, 136.70, 85.100, 86.100, 134.10, 175.70, 174.60, 187.40, 127.80, 123.90, 116.30, 64.500, 148.50, 107.50, 108.70, 144.90, 148.70, 89.000, 155.80, 132.50, 113.80, 154.00, 121.80, 158.40, 124.50, 164.40, 120.80, 100.00, 126.70, 82.700, 120.50, 148.30, 109.10, 155.50, 140.90, 141.70, 138.80]
n = len(sample_density)
print(len(sample_density) == len(sample_elastic))
print(len(sample_elastic))

min_elem_x, max_elem_x = min(sample_density), max(sample_density)
min_elem_y, max_elem_y = min(sample_elastic), max(sample_elastic)
ncf = (max_elem_x - min_elem_x) / (max_elem_y - min_elem_y)
print(ncf)

k_algo_1(sample_density, sample_elastic)
k_algo_2(sample_density, sample_elastic)