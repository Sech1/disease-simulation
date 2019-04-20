import networkx as nx


def create_graphs():
    path = 'data/'
    for x in range(0, 10):
        random = nx.erdos_renyi_graph(14235, .007)
        ba = nx.barabasi_albert_graph(14235, 2)
        rc = nx.relaxed_caveman_graph(356, 40, .10)
        random_save_path = '{0}{1}{2}.gml'.format(path, 'er', x)
        nx.write_gml(random, random_save_path)
        ba_save_path = '{0}{1}{2}.gml'.format(path, 'ba', x)
        nx.write_gml(ba, ba_save_path)
        rc_save_path = '{0}{1}{2}.gml'.format(path, 'rc', x)
        nx.write_gml(rc, rc_save_path)
