from math import sqrt
import matplotlib.pyplot as plt
import copy
import lab1

K_num = 5

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
        if len(clusters_1[i]) == len(clusters_2[i]):
            for j in range(len(clusters_2[i])):
                if clusters_1[i][j] != clusters_2[i][j]:
                    return False
        else:
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

    for i in range(10):
        for point in pointsPull:
            index = findClosestCluster(point, centers)
            clusters[index].append(point)
            recalcClusterCenter(clusters[index], index, centers)
        pointsPull = list(zip(sample_density, sample_elastic))

        if compareClusters(clusters, old_clusters):
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

min_elem_x, max_elem_x = min(sample_density), max(sample_density)
min_elem_y, max_elem_y = min(sample_elastic), max(sample_elastic)
ncf = (max_elem_x - min_elem_x) / (max_elem_y - min_elem_y)
print(ncf)

k_algo_1(sample_density, sample_elastic)
k_algo_2(sample_density, sample_elastic)