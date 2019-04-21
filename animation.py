import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as color
from matplotlib.animation import FuncAnimation
from main import set_global_stuff

color_map = ['g', 'y', 'r', 'b', 'm', 'k']
# green
# yellow
# red
# blue
# purple
plt.figure(figsize=(10, 10))
# number of nodes
# generate graph
G, size = set_global_stuff()
size = G.number_of_nodes() * len(color_map)

# generating input frames here, since my data is too big
# its important that the frames go as input and is not generated
# on the fly
colors = list()
count = 0
for k in range(size):
    for i in range(len(color_map)):
        for j in range(G.number_of_nodes()):
            frame_colors = list()
            for x in range(G.number_of_nodes()):
                if count >= x:
                    random_color = color_map[i]
                    node = color.to_hex(random_color)
                    frame_colors.append(node)
                else:
                    random_color = color_map[5]
                    node = color.to_hex(random_color)
                    frame_colors.append(node)
            colors.append(frame_colors)
            count = count + 1
            if count >= G.number_of_nodes():
                count = 0
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
    return nodes,


def animate():
    # output animation; its important I save it
    fig = plt.gcf()
    ani = FuncAnimation(fig, update, interval=1, frames=range(size), blit=True)
    ani.save('crap.gif', writer='imagemagick',  savefig_kwargs={'facecolor':'white'}, fps=1)
