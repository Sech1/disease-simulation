import threading
from collections import defaultdict
import random
import numpy
import copy

import networkx as nx
import numpy as numpy


def main():
    #graph = nx.erdos_renyi_graph(50, .1)
    #sir(graph,0,0,set())
    #sis(graph,0,0,set())
    
    #thread1 = threading.Thread(target=run_simulation, args=("er", 0, 0, 0.1,))
    thread2 = threading.Thread(target=run_simulation, args=("ba", 0, 0, 0.1 ))
    #thread3 = threading.Thread(target=run_simulation, args=("rc", 0, 0, 0.1,))
    
    #thread1.start()
    thread2.start()
    #thread3.start()
    
    #thread1.join()
    thread2.join()
    #thread3.join()


def run_simulation(network_type, disease, patient_zero, vaccination_percentage):
    num_simulations = 1
    network_array = []
    
    immune_group_none = set()
    immune_group_random = set()
    immune_group_friend = set()
    immune_group_bc = set()
    immune_group_hd = set()
  
    for x in range(0, num_simulations):
        network_array.append(load_graph_file(network_type + str(x+1) + '.gml'))

    count=0

    for graph in network_array:
        count += 1
        thread1_graph = threading.Thread(target=random_vaccination, args=(graph, vaccination_percentage, immune_group_random, ))
        thread2_graph = threading.Thread(target=friend_vaccination, args=(graph, vaccination_percentage, immune_group_friend,))
        #thread3_graph = threading.Thread(target=bc_vaccination, args=(graph, vaccination_percentage, immune_group_bc,))
        thread4_graph = threading.Thread(target=hd_vaccination, args=(graph, vaccination_percentage, immune_group_hd,))

        thread1_graph.start()
        thread2_graph.start()
        #thread3_graph.start()
        thread4_graph.start()

        thread1_graph.join()
        thread2_graph.join()
        #thread3_graph.join()
        thread4_graph.join()

        thread1 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_none,str(network_type)+"-none-"+str(count),))
        thread2 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_random,str(network_type)+"-random-"+str(count),))
        thread3 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_friend,str(network_type)+"-friend-"+str(count),))
        #thread4 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_bc,str(network_type)+"-bc-"+str(count),))
        thread5 = threading.Thread(target=sir, args=(graph, disease, patient_zero, immune_group_hd,str(network_type)+"-hd-"+str(count),))
        #thread6 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_none,str(network_type)+"-none-"+str(count),))
        #thread7 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_random,str(network_type)+"-random-"+str(count),))
        #thread8 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_friend,str(network_type)+"-friend-"+str(count),))
        #thread9 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_bc,str(network_type)+"-bc-"+str(count),))
        #thread10 = threading.Thread(target=sis, args=(graph, disease, patient_zero, immune_group_hd,str(network_type)+"-hd-"+str(count),))

        thread1.start()
        thread2.start()
        #thread3.start()
        #thread4.start()
        thread5.start()
        #thread6.start()
        #thread7.start()
        #thread8.start()
        #thread9.start()
        #thread10.start()

        thread1.join()
        thread2.join()
        #thread3.join()
        #thread4.join()
        thread5.join()
        #thread6.join()
        #thread7.join()
        #thread8.join()
        #thread9.join()
        #thread10.join()


def load_graph_file(file_name):
    with open("data/"+file_name) as file:
        graph = nx.parse_gml(file)
        file.close()
        return graph

def random_vaccination(graph, vaccination_percentage, immune_group):
    while len(immune_group) < vaccination_percentage * graph.number_of_nodes():
        immune_group.add(random.randint(0, graph.number_of_nodes()))

def friend_vaccination(graph, vaccination_percentage, immune_group):
    while len(immune_group) < vaccination_percentage * graph.number_of_nodes():
        node = graph.node(random.randint(0,graph.number_of_nodes()))
        friend = graph[node][random.randint(0,len(graph.neighbors(str(node))))]
        immune_group.add(friend)


def bc_vaccination(graph, vaccination_percentage, immune_group):
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

    output = open("results/"+output_filename+"-sis.csv","w")
    
    output.write("Current infected count,Newly infected count,Newly Susceptible,Total Immune\n1,0,0,"+str(len(immune_group))+"\n")

    infected_group = {patient_zero}

    while len(infected_group) > 0:
        newly_infected = spread_disease(disease, infected_group, immune_group, graph)
        recovered = attempt_recovery(disease, infected_group)

        for x in range(len(recovered)):
            infected_group.remove(recovered[x])

        for x in newly_infected:
            infected_group.add(x)

        output.write(str(len(infected_group)) +"," + str(len(newly_infected)) + ","+str(len(recovered))+","+str(len(immune_group))+"\n")

    print("Done with " + output_filename + "-sis.csv")

    return 0

def spread_disease(disease, infected_group, immune_group, graph):
    temp = set()
    for node in infected_group:
        for neighbor in list(graph.neighbors(str(node))):
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

def sir(graph, disease, patient_zero, immune_group, output_filename):
    
    print("Beginning " + output_filename + "-sir.csv")
    
    infected_group = {patient_zero}

    output = open("results/"+output_filename+"-sir.csv", "w")

    output.write("Current infected count,Newly infected count,Recovered,Total Immune Count\n1,0,0,"+str(len(immune_group))+"\n")

    while len(infected_group) > 0:
        newly_infected = spread_disease(disease, infected_group, immune_group, graph)
        recovered = attempt_recovery(disease, infected_group)        

        for x in range(len(recovered)):
            immune_group.add(recovered[x])
            infected_group.remove(recovered[x])

        for x in newly_infected:
            infected_group.add(x)

        output.write(str(len(infected_group))+","+str(len(newly_infected))+","+str(len(recovered))+"," + str(len(immune_group))+ "\n")

    
    print("Done with " + output_filename + "-sir.csv")

    return 0

def infected_roller(disease):
    return numpy.random.normal(disease, 1)


if __name__ == '__main__':
    main()
