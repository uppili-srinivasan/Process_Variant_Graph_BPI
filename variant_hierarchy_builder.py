import os
import csv
from graphviz import Digraph
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import MiniBatchKMeans, AgglomerativeClustering

# ---------- Variant Encoding ----------
def encode_variants(variants_subset, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    variant_texts = [" ".join(variant) for variant, _ in variants_subset]
    embeddings = model.encode(variant_texts, convert_to_numpy=True, show_progress_bar=True)
    return variant_texts, embeddings

# ---------- Data-Driven Recursive Tree Construction ----------
def build_data_driven_tree(
    variants_subset,
    max_levels=4,
    max_clusters=10,
    min_cluster_size=10,
    model_name="all-MiniLM-L6-v2"
):
    variant_texts, embeddings = encode_variants(variants_subset, model_name=model_name)
    nodes, tree = [], {}
    node_id_counter = [1]  # Start from 1, as 0 will be root

    # Always create a single root node (most frequent variant)
    root_idx = max(range(len(variants_subset)), key=lambda i: variants_subset[i][1])
    root_id = 0
    nodes.append({
        "id": root_id,
        "variant": variants_subset[root_idx][0],
        "freq": variants_subset[root_idx][1],
        "parent": None,
        "level": 0,
    })
    tree[None] = [root_id]

    # Remove root from indices for recursion
    all_indices = list(range(len(variants_subset)))
    all_indices.remove(root_idx)

    def recursive_build(variant_indices, parent_id, level):
        if not variant_indices:
            return
        if level > max_levels or len(variant_indices) <= min_cluster_size:
            for idx in variant_indices:
                node_id = node_id_counter[0]
                nodes.append({
                    "id": node_id,
                    "variant": variants_subset[idx][0],
                    "freq": variants_subset[idx][1],
                    "parent": parent_id,
                    "level": level,
                })
                if parent_id not in tree:
                    tree[parent_id] = []
                tree[parent_id].append(node_id)
                node_id_counter[0] += 1
            return

        # Clustering
        n_clusters = min(max_clusters, len(variant_indices))
        if len(variant_indices) > 1000:
            clustering = MiniBatchKMeans(n_clusters=n_clusters, batch_size=1000)
        else:
            clustering = AgglomerativeClustering(n_clusters=n_clusters)
        sub_embeddings = embeddings[variant_indices]
        cluster_labels = clustering.fit_predict(sub_embeddings)

        for cluster_id in range(n_clusters):
            cluster_indices = [variant_indices[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
            if not cluster_indices:
                continue
            # Choose the most frequent variant as the cluster representative
            best_idx = max(cluster_indices, key=lambda idx: variants_subset[idx][1])
            node_id = node_id_counter[0]
            nodes.append({
                "id": node_id,
                "variant": variants_subset[best_idx][0],
                "freq": variants_subset[best_idx][1],
                "parent": parent_id,
                "level": level,
            })
            if parent_id not in tree:
                tree[parent_id] = []
            tree[parent_id].append(node_id)
            node_id_counter[0] += 1

            # Remove the representative from the cluster for recursion
            child_indices = [idx for idx in cluster_indices if idx != best_idx]
            if child_indices:
                recursive_build(child_indices, node_id, level + 1)

    # Start recursion from root
    recursive_build(all_indices, root_id, 1)
    return nodes, tree

# ---------- CSV Export ----------
def save_hierarchical_tree_to_csv(nodes, tree, csv_path="output/variant_hierarchy_details.csv"):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Variant ID", "Level", "Frequency", "Parent ID", "Event Path"])
        for node in nodes:
            writer.writerow([
                node["id"],
                node.get("level", 0),
                node["freq"],
                node["parent"] if node["parent"] is not None else "ROOT",
                " → ".join(node["variant"])
            ])
    print(f"📄 Hierarchical tree CSV saved to {csv_path}")

# ---------- Visualization ----------
def visualize_data_driven_tree(nodes, tree, save_path="output/data_driven_tree", dpi=300):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    dot = Digraph(format='svg', engine='dot')
    dot.attr(dpi=str(dpi))
    dot.attr(rankdir='TB')
    dot.attr('graph', splines='true', ranksep='0.5', nodesep='0.2', concentrate='true')

    # Color scheme for levels
    level_colors = [
        '#FF6B6B',  # Level 0 (root)
        '#4ECDC4',  # Level 1
        '#45B7D1',  # Level 2
        '#96CEB4',  # Level 3
        '#FFD166',  # Level 4
        '#B388FF',  # Level 5+
    ]

    for node in nodes:
        level = node.get('level', 0)
        color = level_colors[level] if level < len(level_colors) else level_colors[-1]
        dot.node(
            str(node['id']),
            label="",
            fillcolor=color,
            style='filled',
            shape='circle',
            width='0.08',
            height='0.08',
            fixedsize='true'
        )

    for node in nodes:
        if node["parent"] is not None:
            dot.edge(str(node["parent"]), str(node["id"]), color='#CCCCCC', penwidth='0.5')

    dot.attr('graph', label=f"Data-Driven Variant Tree ({len(nodes)} nodes)")
    rendered_path = dot.render(filename=save_path, cleanup=True)
    print(f"✅ Data-driven tree saved to {rendered_path}")

# ---------- Main Callable ----------
def build_and_visualize_data_driven_tree(
    variants_subset,
    max_levels=4,
    max_clusters=10,
    min_cluster_size=10,
    model_name="all-MiniLM-L6-v2"
):
    nodes, tree = build_data_driven_tree(
        variants_subset,
        max_levels=max_levels,
        max_clusters=max_clusters,
        min_cluster_size=min_cluster_size,
        model_name=model_name
    )
    visualize_data_driven_tree(nodes, tree)
    save_hierarchical_tree_to_csv(nodes, tree)
    return nodes, tree