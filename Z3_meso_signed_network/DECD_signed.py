"""
以Qs为优化目标的DECD
time：2022年5月8日 10:08:43
by：Youngit
"""

import igraph as ig
# import matplotlib.pyplot as plt
import random
import numpy as np
from numpy import random
import networkx as nx
import copy
import datetime

starttime = datetime.datetime.now()

########################Qs代码############################

def judge_cluster(i, j, l):
    # 判断两个节点是否在一个社区
    if l[i] == l[j]:
        return 1
    else:
        return 0

def wi_p(i, array):
    # 计算节点i连接正边的数目总和 wi+
    wip = list(array[i]).count(1)
    return wip

def wi_n(i, array):
    # 计算节点i连接负边的数目总和 wi-
    win = list(array[i]).count(-1)
    return win

def wij(i, j, array):
    # 判断两个节点是否存在  负边 wij-
    if array[i, j] == 0:
        return 0
    elif array[i, j] == 1:
        return 1
    elif array[i, j] == -1:
        return -1

def w2_p(array):
    # 计算网络中正边的数目总和 2w+
    nump = np.sum(array == 1)  # 找数组中指定数值的个数***** /2为对称
    return nump

def w2_n(array):
    # 计算网络中负边的数目总和 2w-
    nump = np.sum(array == -1)  # 找数组中指定数值的个数*****
    return nump

def Qs_array(array, cluster):
    """
    传入矩阵后求Qs
    :param array: 权值矩阵
    :param cluster: 社团划分结果
    :return: Qs
    """
    n1 = w2_p(array)
    n2 = w2_n(array)
    n = n1+n2
    q = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[0]):
            if judge_cluster(i, j, cluster) != 0:
                if n1==0 and n2==0:
                    q += wij(i, j, array)
                elif n1==0 and n2!=0:
                    q += (wij(i, j, array) - (0 - (wi_n(i, array)*wi_n(j, array) / n2)))
                elif n1!=0 and n2==0:
                    q += (wij(i, j, array) - ((wi_p(i, array)*wi_p(j, array) / n1) - 0))
                elif n1!=0 and n2!=0:
                    q += (wij(i, j, array) - ((wi_p(i, array)*wi_p(j, array) / n1) - (wi_n(i, array)*wi_n(j, array) / n2)))
    q = q / n
    return q

def Qs_txt(txt, cluster):
    """
    符号网络txt转矩阵后求Qs
    :param txt: 网络txt文件路径
    :param cluster: 社团划分结果
    :return: Qs
    """
    G = nx.read_weighted_edgelist(txt)
    G = G.to_undirected()
    n = G.number_of_nodes()
    net_txt = open(txt)  # 符号网络
    net_txt = net_txt.read()
    one_net_edge = net_txt.split("\n")
    array = np.zeros((n, n))
    a, b, s = one_net_edge[0].split(" ")
    if int(a) == 1:
        for i in range(len(one_net_edge)):
            a, b, s = one_net_edge[i].split(" ")
            array[int(a)-1][int(b)-1] = int(s)
            array[int(b)-1][int(a)-1] = int(s)
    else:
        for i in range(len(one_net_edge)):
            a, b, s = one_net_edge[i].split(" ")
            array[int(a)][int(b)] = int(s)
            array[int(b)][int(a)] = int(s)

    qs = Qs_array(array, cluster)
    return qs


#######################以下为DECD##########################
def cleanup(X, n, NP, Gi, threshold_value):
    for i in list(range(NP)):
        # 所有节点标号
        all_node_index = list(range(n))
        # 确定选择节点标号的数目
        get_num = random.randint(1, n)
        # 在1-n号节点中随机选择get_num个不一样的节点标号
        use_node_index = []
        # 在个体i中随机选择get_num个不同的节点，保存在use_node_index
        for cu_i in range(get_num):
            # 在1-n节点中随机选取一个节点序号
            cur_rand_index = random.randint(0, len(all_node_index) - 1)  # TODO
            # 添加至use_node_index
            use_node_index.append(all_node_index[cur_rand_index])
            # 将all_node_index中对应的元素删除
            all_node_index.remove(all_node_index[cur_rand_index])

        # 对use_node_index中的节点进行纠错
        for rand_i in range(get_num):
            # 针对use_node_index中的每一个节点进行社区标号纠错 ###↓↓↓↓↓↓将随机选出的各个节点与其邻居节点放入一个list
            node = use_node_index[rand_i]
            # 确定节点node的所有邻域个体，包括其自身，如node=16，那么all_adj_node=【16,33,34】
            # print('node',node)
            neigh_node = Gi.neighbors(node)
            # print('neigh',neigh_node)

            # 构建节点node自身及邻域集合列表
            # 例如：[2, 0, 1, 3, 7, 8, 9, 13, 27, 28, 32]
            all_adj_node = []
            all_adj_node.append(node)
            # for k in range(len(neigh_node)):
            # all_adj_node.append(neigh_node[k])
            all_adj_node.extend(neigh_node)  # 修改过的语句，原句在上面###↑↑↑↑↑↑将随机选出的各个节点与其邻居节点放入一个list

            # node及其邻域节点所属的社区编号
            node_comm = X[i][node]
            # node邻域节点所属的社区编号
            node_neigh_comm = []
            for k in range(len(neigh_node)):
                node_neigh_comm.append(X[i][neigh_node[k]])
            # print('邻居节点社团标号',node_neigh_comm)

            # 计算CV
            # 节点node与邻域个体属于不同社区的数目
            different_comm_number = 0
            for k in range(len(node_neigh_comm)):
                if node_comm != node_neigh_comm[k]:
                    different_comm_number += 1
                else:  # 新增部分
                    different_comm_number += 0
            # 节点node的度
            # degree_node = Gi.degree(node)#原代码：
            degree_node = len(node_neigh_comm)
            # 节点node的CV值
            CV_node = float(different_comm_number) / degree_node
            # 判断CV是否大于阈值
            # 若是，则说明节点node与邻域节点不在同一社区的概率较大
            # 节点社区标号错误,选择邻域节点中出现次数最多的社区标号
            if CV_node > threshold_value:
                # 邻域节点所属社区标号
                temp_comm = node_neigh_comm
                # 邻域节点所归属最多的社区数目
                max_num = 0
                # 邻域节点所归属最多的社区标号
                max_comm_id = 0
                # 找到node_neigh_comm中邻域节点归属最多的社区
                while len(temp_comm) > 0:
                    # 选取第一个邻域节点所属社区cur_comm
                    cur_comm = temp_comm[0]
                    # 归属cur_comm的所有邻域节点的序号集合
                    all_node = []
                    for k in range(len(temp_comm)):
                        if temp_comm[k] == cur_comm:
                            all_node.append(k)
                    # 归属cur_comm的所有邻域节点数目
                    cur_num = len(all_node)
                    # 比较cur_num与max_num，更新max_num和max_comm_id
                    if cur_num > max_num:
                        # 属于当前社区cur_comm的邻居节点>已知属于同一社区的最多邻居节点数目max_num
                        max_num = cur_num
                        max_comm_id = cur_comm
                    elif cur_num == max_num:
                        # 以50%的概率决定是否更改max_num和max_comm_id
                        if random.rand(1, 1) > 0.5:
                            max_num = cur_num
                            max_comm_id = cur_comm
                    # 删除temp_comm中归属于cur_comm的邻域节点\

                    del_comm = []
                    for k in range(len(all_node)):
                        del_comm.append(temp_comm[all_node[k]])
                    for k in del_comm:
                        temp_comm.remove(k)
                    # del temp_comm[0]  # 改进删除列表元素方式

                    # 将pop中node的社区标号更新为max_comm_id
                X[i][node] = max_comm_id  # 纠正该节点的社团编号
                # 返回纠错后的新种群
    return X


# signedTxt = "data/GGS_58.txt"
# noSignedTxt = "data/GGS_58_2.txt"
signedTxt = "data/signed/2_RD.txt"  # TODO 带符号的网络路径
noSignedTxt = "data/no_signed/2_RD.txt"  # TODO 不带符号的网络路径
# signedTxt = "data/testSigned.txt"
# noSignedTxt = "data/test.txt"

# 网络信息
G = nx.read_weighted_edgelist(signedTxt)
G = G.to_undirected()  # 转换成无向图
n = G.number_of_nodes()  # 获取一个Graph对象中node的数量

# 基于这些连边使用igraph创建一个新网络
Gi = ig.Graph.Read_Edgelist(noSignedTxt)
Gi = Gi.subgraph(map(int, G.nodes()))  # G.nodes()获取一个Graph对象中的node数组,
Gi = Gi.as_undirected()
# print(Gi)

# DECD算法检测Karate network
# 参数设置
NP = 100
Gen = 150
threshold_value = 0.7  # 阈值
exetime = 1
F = 0.9
CR = 0.3

# 构建初始种群，每个个体代表一个社区划分，每个元素对应节点所属社区标号
# 限定种群个体中各维取值范围
xmin = 1
xmax = n
D = n
# 每一维分量的取值范围[1,n]
domain = []
for i in range(0, n):
    domain.append((xmin, xmax))
# print('domain=',domain)


# 构建初始种群
# 使用列表解析
# 注意：numpy中的randint函数对于取值范围，包括起始值，但是不包括终值
pop = []
for j in range(NP):  # 生成NP个个体
    vec = [random.randint(domain[j][0], domain[j][1] + 1)  # 生成 j in [1,n] # 每个个体中的每个节点 随机赋值[1,n]的社区编号
           for j in range(D)  # 每个个体都有j维分量
           ]
    # print('vec=',vec)
    pop.append(vec)
# print('pop=',pop)


# 计算个体适应度值
# 目标函数：模块度函数
Fit = []
for i in range(NP):
    # fit = ig.GraphBase.modularity(Gi, pop[i])  # TODO
    fit = Qs_txt(signedTxt,pop[i])  # Qs
    Fit.append(fit)

# Main loop
# 主循环开始
best_in_history = []
bestx_in_history = []

while exetime < Gen:
    # 输出当前进化代数exetime
    print('exetime=', exetime)
    # 变异操作: 在初始种群（pop）中随机抽取0~NP的三个不同的个体
    mutation_pop = []  # 变异种群
    for i in range(NP):
        a = random.randint(0, NP)  # a in [0,NP-1]
        b = random.randint(0, NP)
        c = random.randint(0, NP)
        if a == i:  # 每次为了不取到自己？
            a = random.randint(0, NP)
        if b == i or b == a:
            b = random.randint(0, NP)
        if c == i or c == b or c == a:
            c = random.randint(0, NP)
        # 构造第i个个体对应的变异个体V
        V = []
        for j in range(D):
            vec = int(pop[a][j] + F * (pop[b][j] - pop[c][j]))
            # print('vec=',vec)
            # 限制每一维分量的取值范围(是否违反边界约束条件)
            if vec < domain[j][0]:
                vec1 = max(domain[j][0], int(2 * domain[j][0] - vec))
            elif vec > domain[j][1]:
                vec1 = min(domain[j][1], int(2 * domain[j][1] - vec))
            else:
                vec1 = vec
            V.append(vec1)
            # print('v=',V)
        # 将第i个个体对应的变异个体V存入变异种群mutation_pop
        mutation_pop.append(V)

    # 变异种群clean-up operation
    # 对种群中每个个体中节点的社区标号进行纠错
    # 随机选择个体中的若干个节点，选几个和选哪几个均为随机。
    # 根据其CV值及其邻域节点所属社区更新节点i的社区
    mutation_pop = cleanup(mutation_pop, n, NP, Gi, threshold_value)

    # 交叉操作 此代码中的交叉操作是：当满足条件时，将变异个体【小列表】中相同社团编号的值赋给初始个体（这是文章中的改进二项操作）
    crossover_pop = copy.deepcopy(pop)  # 深拷贝，两者是完全独立的
    #    for i in range(NP):
    #        crossover_pop.append(pop[i])
    # 根据DE算法的交叉操作，以概率CR，保留变异种群mutation_pop中的社区性状
    for i in range(NP):
        # 在[0，n-1]范围内，随机选择一维分量
        rand_j = random.randint(0, D)  # rand_j in [0,D-1] 与文章表述不一致
        for j in range(D):
            if random.rand(1, 1) <= CR or j == rand_j:  # random.rand返回一个或一组服从“0~1”均匀分布的随机样本值
                # 变异个体i中第j维分量对应的值
                comm_id_j = mutation_pop[i][j]
                # all_nodes_j是变异个体i中社团编号都为V_ij节点位置
                all_nodes_j = []
                all_nodes_j.append(j)
                for k in range(D):
                    if k != j and mutation_pop[i][k] == comm_id_j:
                        all_nodes_j.append(k)
                # 交叉个体i中上述节点集合的社区标号全部改为comm_id_j
                for k in range(D):
                    if k in all_nodes_j:
                        crossover_pop[i][k] = comm_id_j
                # crossover_pop[i][j] = comm_id_j
    # 交叉种群clean-up operation
    crossover_pop = cleanup(crossover_pop, n, NP, Gi, threshold_value)

    # 选择操作
    # 将crossover_pop中的优秀个体保留至下一代种群pop
    for i in range(NP):
        # score = ig.GraphBase.modularity(Gi, crossover_pop[i])  # 计算每一个试验个体的Q TODO
        score = Qs_txt(signedTxt,crossover_pop[i])
        if score > Fit[i]:  # 比较每一个新个体和老个体的Q
            pop[i] = crossover_pop[i]  # 把Q高的给初始种群作为第二代（其实这个[:]可以不用）
            Fit[i] = score  # 储存新个体的Q值

    # 记录每一代最优解，绘制收敛曲线
    best_in_history.append(max(Fit))  # 纵坐标是这一代的最大Q值
    bestx_in_history.append(pop[Fit.index(max(Fit))])  # 最大Q值的那一个个体
    exetime += 1


print("迭代后：\n", best_in_history)
print(len(best_in_history))
# print('The max Qs is=', best_in_history[len(best_in_history) - 1])
# print('The best membership is=', bestx_in_history[len(bestx_in_history) - 1])
print('The max Qs is=', max(best_in_history))
print('The best membership is=', bestx_in_history[best_in_history.index(max(best_in_history))])

'''NMI的计算
membership1是网络的真实社团划分
'''
# dolphins = [2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2]
#
# NMI = ig.compare_communities(dolphins, bestx_in_history[-1], method='nmi', remove_none=False)
# print('The NMI is=', NMI)

# 历史进化NMI列表
# NMIList = []
# for i in range(len(bestx_in_history)):
#     NMI_i = ig.compare_communities(comm0, bestx_in_history[i], method='nmi', remove_none=False)
#     NMIList.append(NMI_i)
# print('The NMIList is=', NMIList)

endtime = datetime.datetime.now()
print("代码用时：", (endtime - starttime))

