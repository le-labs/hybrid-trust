import networkx as nx
import matplotlib.pyplot as plt


# Graph
def new_add_edge(G, a, b):
    if (a, b) in G.edges:
        max_rad = max(x[2]['rad'] for x in G.edges(data=True) if sorted(x[:2]) == sorted([a, b]))
    else:
        max_rad = 0
    G.add_edge(a, b, rad=max_rad + 0.1)


def create_graph(mw, cas, cas_reversed):
    G = nx.MultiDiGraph()

    for key, ca in cas.items():
        if key != 'invalid':
            trusted_cas = mw.get_trusted_cas(ca)
            G.add_node(cas_reversed[ca])
            for trusted_ca in trusted_cas:
                if trusted_ca != '0x0000000000000000000000000000000000000000':
                    new_add_edge(G, cas_reversed[ca], cas_reversed[trusted_ca])
    plt.figure(figsize=(6, 6))

    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='#639cf7')
    nx.draw_networkx_labels(G, pos, font_size=16)

    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], connectionstyle=f'arc3, rad = {edge[2]["rad"]}')

    plt.show()
    return G


def find_shortest_path(G, source, target):
    return nx.shortest_path(G, source=source, target=target)


def ca_in_trust_path_radius(G, trusted_cas, target_cas, max_trust_path_length):
    best_shortest_path = []
    for trusted_ca in trusted_cas:
        for target_ca in target_cas:
            shortest_path = find_shortest_path(G, trusted_ca, target_ca)
            if len(shortest_path) <= max_trust_path_length:
                max_trust_path_length = len(shortest_path)
                best_shortest_path = shortest_path
    if best_shortest_path is not None:
        return best_shortest_path
    else:
        return "Not in trust path radius"

