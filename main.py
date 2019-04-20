import threading
from collections import defaultdict
import random

import matplotlib.pyplot as plt
import networkx as nx


def main():
    graph = nx.erdos_renyi_graph(50, .25)
    sis(graph, 0, 25, set())

    # random_network = 'ER'
    # ba_network = 'BA'
    # rc_network = 'RC'
    # array = 0
    #
    # thread1 = threading.Thread(target=run_simulation, args=(random_network, 0, array,))
    # thread2 = threading.Thread(target=run_simulation, args=(ba_network, 0, array,))
    # thread3 = threading.Thread(target=run_simulation, args=(rc_network, 0, array,))
    #
    # thread1.start()
    # thread2.start()
    # thread3.start()
    #
    # thread1.join()
    # thread2.join()
    # thread3.join()


def run_simulation(network_type, disease, patient_zero):
    num_simulations = 10
    network_array = []
    empty_dict = defaultdict(int)

    immune_group_random = defaultdict(int)
    immune_group_friend = defaultdict(int)
    immune_group_bc = defaultdict(int)
    immune_group_hd = defaultdict(int)
    vac_count = 0

    for x in range(1, num_simulations):
        network_array.append(load_graph_file(network_type + str(x) + '.gml'))

    for graph in network_array:
        thread1_graph = threading.Thread(target=random_vaccination, args=(graph, vac_count, immune_group_random,))
        thread2_graph = threading.Thread(target=friend_vaccination, args=(graph, vac_count, immune_group_friend,))
        thread3_graph = threading.Thread(target=bc_vaccination, args=(graph, vac_count, immune_group_bc,))
        thread4_graph = threading.Thread(target=hd_vaccination, args=(graph, vac_count, immune_group_hd,))

        thread1_graph.start()
        thread2_graph.start()
        thread3_graph.start()
        thread4_graph.start()

        thread1_graph.join()
        thread2_graph.join()
        thread3_graph.join()
        thread4_graph.join()

        thread1 = threading.Thread(target=sir, args=(graph, disease, patient_zero, empty_dict,))
        thread2 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_random,))
        thread3 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_friend,))
        thread4 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_bc,))
        thread5 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_hd,))
        thread6 = threading.Thread(target=sis, args=(graph, disease, patient_zero, empty_dict,))
        thread7 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_random,))
        thread8 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_friend,))
        thread9 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_bc,))
        thread10 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_hd,))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
        thread8.start()
        thread9.start()
        thread10.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        thread8.join()
        thread9.join()
        thread10.join()


def load_graph_file(file_name):
    with open(file_name):
        return 0


def no_vaccination(graph):
    immune_group = defaultdict(int)

    return immune_group


def random_vaccination(graph):
    immune_group = defaultdict(int)

    return immune_group


def friend_vaccination(graph):
    immune_group = defaultdict(int)

    return immune_group


def bc_vaccination(graph):
    immune_group = defaultdict(int)

    return immune_group


def hd_vaccination(graph):
    immune_group = defaultdict(int)

    return immune_group


def sis(graph, disease, patient_zero, immune_group):
    infected_group = {patient_zero}

    while len(infected_group) > 0:
        temp = []
        for node in infected_group:
            for neighbor in list(graph.neighbors(node)):
                if infected_roller() == 0:
                    temp.append(neighbor)

        for node in infected_group:
            if infected_roller() == 1:
                infected_group.remove(node)

        for x in range(len(temp)):
            infected_group.add(temp[x])

    return 0


def sir(graph, disease, patient_zero, immune_group):
    infected_group = {patient_zero}

    while len(infected_group) > 0:
        temp = []
        for node in infected_group:
            for neighbor in list(graph.neighbors(node)):
                if infected_roller() == 0:
                    temp.append(neighbor)

        for node in infected_group:
            if infected_roller() == 1:
                infected_group.remove(node)
                immune_group.add(node)

        for x in range(len(temp)):
            infected_group.add(temp[x])
    return 0


def infected_roller():
    random_num = random.randint(0, 100) % 2
    return random_num


if __name__ == '__main__':
    main()
