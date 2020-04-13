from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import copy
import numpy as np
import lab1

def getDistance(point_1, point_2):
    # Евклидово расстояние с поправочным на масштаб коэффициентом
    return sqrt((pow(point_2[0] - point_1[0], 2) + pow(ncf*(point_2[1] - point_1[1]),2)))

def compareClusters(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    for i in range(len(list_1)):
        if len(list_1[i]) != len(list_2[i]):
            return False
        for j in range(len(list_2[i])):
            if list_1[i][j] != list_2[i][j]:
                return False
    return True

def recalcClusterCenter(cluster):
    mid_x = sum([elem[0] for elem in cluster]) / len(cluster)
    mid_y = sum([elem[1] for elem in cluster]) / len(cluster)
    return [mid_x, mid_y]

def findNewPopularPoint(points, delta):
    if len(points) == 1:
        return 0
    index = -1
    maxNeig = 1
    for i, cur_point in enumerate(points):
        num = len([point for point in points if getDistance(cur_point, point) <= delta])
        if num > maxNeig:
            maxNeig = num
            index = i
    return index

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

def makeClusters(data1, data2, R):
    size = len(data1)
    history = []
    
    points = list(zip(data1, data2))
    clusters = []
    iters = 0
    delta = 1
    points_to_process = points[:]
    while len(points_to_process) > 0:
        iters += 1
        index = np.random.randint(0, len(points_to_process))
        while True:
            index = findNewPopularPoint(points_to_process, delta)
            if index == -1:
                delta += 1
                if (delta > R1):
                    index = 0
                    break
            else:
                break
        center = points_to_process[index]
        points_in_cluster = [point for point in points_to_process if getDistance(point, center) < R]

        iter = 0
        while True:
            iter += 1
            center_new = recalcClusterCenter(points_in_cluster)
            if (abs(center[0] - center_new[0]) + abs(center[1] - center_new[1])) < 0.001:
                break
            points_in_cluster = [point for point in points_to_process if getDistance(point, center_new) < R]
            center = center_new
            if iter == 100:
                break

        for cl_point in points_in_cluster:
            for point in points_to_process:
                if (abs(cl_point[0] - point[0]) + abs(cl_point[1] - point[1])) < 0.001:
                    points_to_process.remove(cl_point)
        clusters.append(points_in_cluster)
    return clusters

def plotClusters(clusters, clusterMeans, R):
    ax = plt.axes(aspect='equal')
    for i, cluster in enumerate(clusters):
        x, y = list(zip(*cluster))
        color = np.random.rand(3,)
        color[0] = (color[0]*255 % 192) / 255
        plt.scatter(x, y, marker=".", color=color, alpha=0.5)
        ax.add_artist(plt.Circle(clusterMeans[i], R, color=color, alpha=0.1))
        xs = [mean[0] for mean in clusterMeans]
        ys = [mean[1] for mean in clusterMeans]
    plt.scatter(xs, ys, color = 'r', marker='o')
    plt.show()


if __name__ == '__main__':    
    n = lab1.selection_size    
    general_population = lab1.read_data(filename=lab1.data_file_name)
    sample_density = lab1.get_sample_first(general_population, n)
    sample_elastic = lab1.get_sample_second(general_population, n)
    # n = len(sample_density)

    sample_2D = list(zip(sample_density, sample_elastic))
    min_elem_x, max_elem_x = min(sample_density), max(sample_density)
    min_elem_y, max_elem_y = min(sample_elastic), max(sample_elastic)
    ncf = (max_elem_x - min_elem_x) / (max_elem_y - min_elem_y)

    minR = np.Inf
    maxR = -np.Inf
    for p1 in sample_2D:
        for p2 in sample_2D:
            d = getDistance(p1, p2)
            if 0 < d < minR:
                minR = d
            if d > maxR:
                maxR = d
    
    print("Минимальный радиус:", minR)
    print("Максимальный радиус:", maxR)
    R1 = 59.5
    # clusters = makeClusters(sample_density, sample_elastic, R1, maxIters=10)
    # centers = [recalcClusterCenter(cluster) for cluster in clusters]
    # print("Clusters num: {0}".format(len(clusters)))
    # print(F_1(clusters, centers))
    # print(F_2(clusters))
    # print(F_3(clusters, centers))
    # print(sorted(centers))
    # plotClusters(clusters, centers, R1)
    # exit(0)

    old_clusters = [] 
    for R in np.linspace(minR, maxR, 500): # 68 400 200
        clusters = makeClusters(sample_density, sample_elastic, R)
        centers = [recalcClusterCenter(cluster) for cluster in clusters]
        print("Clusters num: {0}".format(len(clusters)))
        print("F1: {:.2f}".format(F_1(clusters, centers)))
        print("F2: {:.2f}".format(F_2(clusters)))
        print("F3: {:.2f}".format(F_3(clusters, centers)))
        print("\n")
        if compareClusters(clusters, old_clusters):
        # if len(clusters) == 6:
            # Устойчивое!
            print("success! ", R)
            print(sorted(centers))
            print("R: {:.2f}".format(R))
            plotClusters(clusters, centers, R)
            break
        old_clusters = copy.deepcopy(clusters)
    plt.show()