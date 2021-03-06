import copy
import sys

import numpy as numpy

from animation import *

max_iterations = 100
animations = True
debug = True
debug_type = 'rc'

def main():
    if not debug:
        if len(sys.argv) != 2:
            print("you forgot the network type: er rc ba")
            return

        run_simulation(sys.argv[1], 0, 0, 0.1, )
        # run_simulation("ba", 0, 0, 0.1,)
    else:
        if not animations:
            run_simulation('rc', 0, 0, 0.1, )
        else:
            animate()


def run_simulation(network_type, disease, patient_zero, vaccination_percentage):
    num_simulations = 10
    network_array = []

    immune_group_none = set()
    immune_group_random = set()
    immune_group_friend = set()
    immune_group_bc = set()
    immune_group_hd = set()
    if not animations:
        for x in range(0, num_simulations):
            network_array.append(load_graph_file(network_type + str(x) + '.gml'))

        count = 0

        for graph in network_array:
            count += 1
            # random_vaccination(graph, vaccination_percentage, immune_group_random)
            # friend_vaccination(graph, vaccination_percentage, immune_group_friend)
            bc_vaccination(graph, vaccination_percentage, immune_group_bc)
            # hd_vaccination(graph, vaccination_percentage, immune_group_hd)

            # sir(graph, disease, patient_zero, immune_group_none,str(network_type)+"-none-"+str(count))
            # sir(graph, disease, patient_zero, immune_group_random,str(network_type)+"-random-"+str(count))
            # sir(graph, disease, patient_zero, immune_group_friend,str(network_type)+"-friend-"+str(count))
            sir(graph, disease, patient_zero, immune_group_bc, str(network_type) + "-bc-" + str(count))
            # sir(graph, disease, patient_zero, immune_group_hd,str(network_type)+"-hd-"+str(count))
            # sis(graph, disease, patient_zero, immune_group_none,str(network_type)+"-none-"+str(count))
            # sis(graph, disease, patient_zero, immune_group_random,str(network_type)+"-random-"+str(count))
            # sis(graph, disease, patient_zero, immune_group_friend,str(network_type)+"-friend-"+str(count))
            sis(graph, disease, patient_zero, immune_group_bc, str(network_type) + "-bc-" + str(count))
            # sis(graph, disease, patient_zero, immune_group_hd,str(network_type)+"-hd-"+str(count))
    else:
        random = nx.erdos_renyi_graph(300, .030)
        ba = nx.barabasi_albert_graph(350, 1)
        rc = nx.relaxed_caveman_graph(20, 20, .09)

        bc_vaccination(rc, vaccination_percentage, immune_group_bc)
        animation_bc_sir = sir(rc, disease, patient_zero, immune_group_bc, 'ba-animation')
        # animation_bc_sis = sis(rc, disease, patient_zero, immune_group_bc, 'ba-animation')
        return animation_bc_sir, rc, len(animation_bc_sir)



def load_graph_file(file_name):
    with open("data/" + file_name) as file:
        graph = nx.parse_gml(file)
        file.close()
        return graph


def random_vaccination(graph, vaccination_percentage, immune_group):
    while len(immune_group) < vaccination_percentage * graph.number_of_nodes():
        immune_group.add(random.randint(0, graph.number_of_nodes()))


def friend_vaccination(graph, vaccination_percentage, immune_group):
    while len(immune_group) < vaccination_percentage * graph.number_of_nodes():
        node = random.randint(0, graph.number_of_nodes() - 1)
        neighbors = list(graph.neighbors(str(node)))
        friend = neighbors[random.randint(0, len(neighbors) - 1)]
        immune_group.add(friend)


def bc_vaccination(graph, vaccination_percentage, immune_group):
    betweeness_centrality = nx.betweenness_centrality(graph, 10)

    s = [(k, betweeness_centrality[k]) for k in
         sorted(betweeness_centrality, key=betweeness_centrality.get, reverse=True)]

    for node in s:
        immune_group.add(node[0])
        if len(immune_group) >= vaccination_percentage * graph.number_of_nodes():
            return

    # while len(immune_group) < vaccination_percentage * graph.number_of_nodes():
    #    betweeness_centrality = nx.betweenness_centrality(graph_copy,2000)
    #    current_max = -1
    #    for node, bc in betweeness_centrality.items():
    #        if bc > current_max:
    #            current_node = node
    #            current_max = bc
    #    immune_group.add(current_node)
    #    graph_copy.remove_node(current_node)
    #    print(vaccination_percentage * graph.number_of_nodes()-len(immune_group))

    return 0


def hd_vaccination(graph, vaccination_percentage, immune_group):
    graph_copy = copy.deepcopy(graph)

    while len(immune_group) < vaccination_percentage * graph.number_of_nodes():
        current_max = -1
        for node in graph_copy.nodes():
            if graph_copy.degree(node) > current_max:
                current_node = node
                current_max = graph_copy.degree(current_node)
        immune_group.add(current_node)
        graph_copy.remove_node(current_node)

    return 0


def sis(graph, disease, patient_zero, immune_group, output_filename):
    print("Beginning " + output_filename + "-sis.csv")

    output = open("results/" + output_filename + "-sis.csv", "w")

    output.write("Current infected count,Newly infected count,Newly Susceptible,Total Immune\n1,0,0," + str(
        len(immune_group)) + "\n")

    infected_group = {patient_zero}

    iteration_count = 0
    animation_array = list()

    while len(infected_group) > 0 and iteration_count < max_iterations:
        iteration_count += 1
        newly_infected = spread_disease(disease, infected_group, immune_group, graph)
        recovered = attempt_recovery(disease, infected_group)

        for x in range(len(recovered)):
            infected_group.remove(recovered[x])

        for x in newly_infected:
            infected_group.add(x)

        if not animations:
            output.write(str(len(infected_group)) + "," + str(len(newly_infected)) + "," + str(len(recovered)) + "," + str(
                len(immune_group)) + "\n")
        else:
            # green not infected - 0
            # yellow newly_infected - 1
            # red - 2 - infected
            # blue  recovered - 3
            # purple immune - 4
            animation_tick = list()
            for node in graph:
                if int(node) in immune_group:
                    animation_tick.append(int(4))
                elif int(node) in infected_group:
                    animation_tick.append(int(2))
                elif int(node) in newly_infected:
                    animation_tick.append(int(1))
                elif int(node) in recovered:
                    animation_tick.append(int(3))
                else:
                    animation_tick.append(int(0))
            animation_array.append(animation_tick)

    if not animations:
        print("Done with " + output_filename + "-sis.csv")
        return 0
    else:
        return animation_array


def sir(graph, disease, patient_zero, immune_group, output_filename):
    immune_group_copy = copy.deepcopy(immune_group)

    print("Beginning " + output_filename + "-sir.csv")

    infected_group = {patient_zero}

    output = open("results/" + output_filename + "-sir.csv", "w")

    output.write("Current infected count,Newly infected count,Recovered,Total Immune Count\n1,0,0," + str(
        len(immune_group_copy)) + "\n")

    iteration_count = 0

    animation_array = list()

    while len(infected_group) > 0 and iteration_count < max_iterations:
        iteration_count += 1
        newly_infected = spread_disease(disease, infected_group, immune_group_copy, graph)
        recovered = attempt_recovery(disease, infected_group)

        for x in range(len(recovered)):
            immune_group_copy.add(recovered[x])
            infected_group.remove(recovered[x])

        for x in newly_infected:
            infected_group.add(x)

        if not animations:
            output.write(str(len(infected_group)) + "," + str(len(newly_infected)) + "," + str(len(recovered)) + "," + str(
                len(immune_group_copy)) + "\n")
        else:
            # green not infected - 0
            # yellow newly_infected - 1
            # red - 2 - infected
            # blue  recovered - 3
            # purple immune - 4
            animation_tick = list()
            for node in graph:
                if int(node) in immune_group:
                    animation_tick.append(int(4))
                elif int(node) in infected_group:
                    animation_tick.append(int(2))
                elif int(node) in newly_infected:
                    animation_tick.append(int(1))
                elif int(node) in recovered:
                    animation_tick.append(int(3))
                else:
                    animation_tick.append(int(0))
            animation_array.append(animation_tick)

    if not animations:
        print("Done with " + output_filename + "-sir.csv")
        return 0
    else:
        return animation_array


def spread_disease(disease, infected_group, immune_group, graph):
    temp = set()
    for node in infected_group:
        for neighbor in list(graph.neighbors(node)):
            if neighbor not in infected_group and neighbor not in immune_group:
                if infected_roller(disease) >= 0:
                    temp.add(neighbor)
    return temp


def attempt_recovery(disease, infected_group):
    recovered = []
    for node in infected_group:
        if infected_roller(disease) < 0:
            recovered.append(node)
    return recovered


def infected_roller(disease):
    return numpy.random.normal(disease, 1)


def set_global_stuff():
    graph = nx.erdos_renyi_graph(15, .25)
    frames = 100
    return graph, frames


if __name__ == '__main__':
    main()
