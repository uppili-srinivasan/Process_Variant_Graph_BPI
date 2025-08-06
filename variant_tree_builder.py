from graphviz import Digraph

class TrieNode:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.frequency = 0  # number of variants/cases passing through this node

def insert_variant(trie_root, variant_steps, frequency):
    node = trie_root
    node.frequency += frequency
    for step in variant_steps:
        if step not in node.children:
            node.children[step] = TrieNode(step)
        node = node.children[step]
        node.frequency += frequency

def build_trie_from_variants(variants_subset):
    """
    Builds a Trie from a subset of variants.
    Each path through the Trie represents a process variant.
    """
    root = TrieNode("START")
    for variant_tuple, freq in variants_subset:
        insert_variant(root, variant_tuple, freq)
    return root

def visualize_trie(trie_root, save_path="variant_trie_tree", dpi=300):
    """
    Visualizes the Trie using Graphviz and saves it as an image.
    """
    dot = Digraph(format='png')
    dot.attr(dpi=str(dpi))
    dot.attr(rankdir='TB')  # vertical layout

    def add_nodes_edges(node, parent_id=None):
        node_id = str(id(node))
        label = f"{node.name}\n({node.frequency})"
        dot.node(node_id, label=label, shape='box', style='filled', fillcolor='lightblue')

        if parent_id:
            dot.edge(parent_id, node_id)

        for child in node.children.values():
            add_nodes_edges(child, node_id)

    add_nodes_edges(trie_root)

    dot.render(filename=save_path, cleanup=True)
    print(f"✅ Trie-based process variant tree saved to {save_path}.png")

def build_and_visualize_trie(variants_subset, top_n=None, save_path="variant_trie_tree"):
    """
    Main entry: builds and visualizes the Trie from the filtered variants.

    Parameters:
        variants_subset: List of (variant_tuple, frequency)
        top_n: Optional integer – only use top N variants
        save_path: Output path prefix (without extension)
    """
    if top_n is not None:
        variants_subset = variants_subset[:top_n]
        print(f"📦 Building Trie from top {top_n} variants.")
    else:
        print(f"📦 Building Trie from full variant set ({len(variants_subset)} variants).")

    trie_root = build_trie_from_variants(variants_subset)
    visualize_trie(trie_root, save_path=save_path)
