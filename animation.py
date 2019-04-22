import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as color
from matplotlib.animation import FuncAnimation
from main import run_simulation

color_map = ['g', 'y', 'r', 'b', 'm', 'k']
# green not infected
# yellow newly_infected
# red
# blue  recovered
# purple immune
plt.figure(figsize=(10, 10))
# number of nodes
# generate graph

# return animation_bc_sir, ba, len(animation_bc_sir)
color_rules, G, size = run_simulation('rc', 0, 0, 0.1, )

# generating input frames here, since my data is too big
# its important that the frames go as input and is not generated
# on the fly
colors = list()
count = 0
for x in range(size):
    frame_colors = list()
    length = len(color_rules[x])
    for i in range(length):
        node_color = color_map[color_rules[x][i]]
        node_color = color.to_hex(node_color)
        frame_colors.append(node_color)
    colors.append(frame_colors)
np_array = np.array(colors)
frame = np_array
for i in range(size):
    for k in range(len(color_map)):
        for x in range(G.number_of_nodes()):
            color_list = list()

# draw the topology of the graph, what changes during animation
# is just the color
pos = nx.spring_layout(G)
nodes = nx.draw_networkx_nodes(G, pos)
edges = nx.draw_networkx_edges(G, pos)
plt.axis('off')


# pass frames to funcanimation via update function
# this is where I get stuck, since I cannot break
# out of the loop, neither can I read every array of
# the ndarray without looping over it explicitly


def update(i):
    # for i in range(len(frame)):
    # instead of giving frame as input, if I randomly generate it, then it works
    nc = frame[i] # np.random.randint(2, size=200)
    nodes.set_color(nc)
    size = []
    for x in range(G.number_of_nodes()):
        size.append(50)
    size = np.array(size)
    nodes.set_sizes(size)
    return nodes,


def animate():
    # output animation; its important I save it
    fig = plt.gcf()
    ani = FuncAnimation(fig, update, interval=1, frames=range(size), blit=True)
    ani.save('crap.gif', writer='imagemagick',  savefig_kwargs={'facecolor':'white'}, fps=1)
