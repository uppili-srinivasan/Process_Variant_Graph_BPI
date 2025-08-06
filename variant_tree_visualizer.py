from graphviz import Digraph
import os

def visualize_variant_tree(tree, save_path="variant_tree"):
    """
    Visualizes the process variant tree using Graphviz in a vertical hierarchical layout.
    
    Args:
        tree: networkx.DiGraph object representing the tree.
        save_path: path prefix to save the visualization PNG (no extension).
    """
    dot = Digraph(format='png')
    dot.attr(rankdir='TB', size='8,10')  # Top to Bottom

    # Add nodes
    for node in tree.nodes():
        dot.node(node, shape='box', style='filled', fillcolor='lightblue')

    # Add edges with weights
    for u, v, data in tree.edges(data=True):
        weight = data.get('weight', 1)
        dot.edge(u, v, label=str(weight), penwidth=str(0.5 + 0.5 * (weight ** 0.5)))

    # Make sure directory exists
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

    # Render and overwrite
    dot.render(filename=save_path, cleanup=True)
