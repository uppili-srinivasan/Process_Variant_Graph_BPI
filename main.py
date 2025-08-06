import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
from collections import defaultdict

from data_loader import load_event_log
from variant_extractor import extract_variants
from variant_visualizer import plot_variant_distribution, save_variants_to_csv
from happy_path_visualizer import visualize_happy_path
from variant_tree_builder import build_and_visualize_trie
from variant_tree_visualizer import visualize_variant_tree
from variant_dag_builder import build_process_graph, draw_process_graph
from pareto_cutoff_variants import pareto_cutoff_variants
from variant_hierarchy_builder import (
    build_and_visualize_data_driven_tree,
)
from variant_tree_checker import analyze_variant_tree

def process_similarity_tree(pareto_variants, top_n):
    """
    Process variants and create a similarity-based hierarchical tree.
    """
    top_variants = pareto_variants[:top_n]
    nodes, tree = build_and_visualize_data_driven_tree(
    top_variants,      # your list of (variant, freq)
    max_levels=10,         # set as needed
    max_clusters=20,      # set as needed
    min_cluster_size=2   # set as needed
)
    return nodes, tree

def main():
    df = load_event_log('data/BPI_Challenge_2017.xes.gz')

    print("✅ Event log loaded.")
    print("🔍 Preview:")
    print(df.head())

    print(f"📊 Total cases: {df['case_id'].nunique()}")
    print(f"⚙️ Total events: {len(df)}")

    # 🔍 Extract variants
    variants_dict, sorted_variants = extract_variants(df)

    print(f"\n🧬 Total unique variants: {len(variants_dict)}")

    print("\n🔎 Sample from sorted_variants:")
    for i, item in enumerate(sorted_variants[:5], 1):
        print(f"{i}: {item}")

    # 📊 Compute Pareto (80%) cutoff variants
    pareto_variants = pareto_cutoff_variants(sorted_variants, total_cases=df['case_id'].nunique())

    print(f"\n🎯 Number of variants covering 80% of cases: {len(pareto_variants)}")
    total_covered = sum([count for _, count in pareto_variants])
    print(f"✅ Cases covered by these variants: {total_covered} ({(total_covered / df['case_id'].nunique()):.2%})")


    # 📈 Plot and save variant distribution
    plot_variant_distribution(pareto_variants, save_path="output/variant_distribution.png")
    save_variants_to_csv(pareto_variants, csv_path="output/pareto_variants.csv")

    # 🎯 Extract and print happy path
    most_common_variant = list(pareto_variants[0][0])  # Ensure it's a list
    print("\n🎯 Happy Path (Most Common Variant):")
    print(" → ".join(most_common_variant))
    print(f"📏 Number of events in happy path: {len(most_common_variant)}")
    
    visualize_happy_path(most_common_variant, save_path="output/happy_path", format="svg")

    # 🌳 Build and visualize the process variant tree
    build_and_visualize_trie(pareto_variants, top_n=50, save_path="output/variant_trie_tree")
    #visualize_variant_tree(tree, save_path="variant_tree")
    graph = build_process_graph(pareto_variants, top_n=50)
    draw_process_graph(graph, save_path="output/variant_dag.png")
    print("🗺️ Variant DAG saved to variant_dag.png")

    #process_similarity_tree(pareto_variants, top_n=100)

    CSV_PATH = "output/variant_hierarchy_details.csv"

    if not os.path.exists(CSV_PATH):
        print("⚠️ variant_hierarchy_details.csv not found. Building variant tree now...")
        process_similarity_tree(pareto_variants, top_n=len(pareto_variants))  # Adjust top_n as needed

        # Check again after generation
        if os.path.exists(CSV_PATH):
            print("✅ Tree successfully built. Proceeding to analysis...")
            analyze_variant_tree(CSV_PATH)
        else:
            print("❌ Tree generation failed. File still not found.")
    else:
        print("✅ CSV file found. Proceeding to analysis...")
        analyze_variant_tree(CSV_PATH)

if __name__ == "__main__":
    main()
