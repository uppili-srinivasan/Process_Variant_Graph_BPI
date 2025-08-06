import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def build_process_graph(variants_subset, top_n=None):
    """
    Builds a compressed graph (trie-inspired) from a subset of variants.
    Each node is an activity; repeated activities across variants are not duplicated.

    Parameters:
        variants_subset (list): List of (variant, count) tuples
        top_n (int or None): If given, use only the top_n variants
    """
    if top_n is not None:
        variants_subset = variants_subset[:top_n]
        print(f"📦 Building process graph from top {top_n} variants.")
    else:
        print(f"📦 Building process graph from full variant set ({len(variants_subset)} variants).")

    G = nx.DiGraph()
    G.add_node("START")
    G.add_node("END")

    edge_weights = defaultdict(int)

    for variant, count in variants_subset:
        prev_node = "START"

        for step in variant:
            if not G.has_node(step):
                G.add_node(step)

            edge_weights[(prev_node, step)] += count
            G.add_edge(prev_node, step, weight=edge_weights[(prev_node, step)])

            prev_node = step

        edge_weights[(prev_node, "END")] += count
        G.add_edge(prev_node, "END", weight=edge_weights[(prev_node, "END")])

    return G


def draw_process_graph(G, save_path="output/variant_dag.png"):
    try:
        import pygraphviz
        from networkx.drawing.nx_agraph import to_agraph
    except ImportError:
        raise ImportError("PyGraphviz is required. Install via `pip install pygraphviz`")

    # Convert to AGraph for better control
    A = to_agraph(G)

    # Styling
    A.graph_attr.update(
        dpi="300",
        label="🧭 Process Graph",
        labelloc="t",
        fontsize="20",
        fontname="Arial",
        bgcolor="white"
    )

    A.node_attr.update(
        shape="circle",
        style="filled",
        fillcolor="skyblue",
        fontname="Arial",
        fontsize="12"
    )

    A.edge_attr.update(
        fontsize="10",
        fontname="Arial",
        color="gray",
        arrowsize="0.8"
    )

    # Add edge labels (frequency)
    for u, v in G.edges():
        weight = G[u][v]['weight']
        edge = A.get_edge(u, v)
        edge.attr['label'] = str(weight)

    # Draw graph using Graphviz's 'dot' layout
    A.layout(prog="dot")
    A.draw(save_path)

    print(f"✅ Graph saved to {save_path}")
