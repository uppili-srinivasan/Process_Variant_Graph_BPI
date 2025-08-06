import os
import pandas as pd
from collections import defaultdict


def analyze_variant_tree(csv_path):
    df = pd.read_csv(csv_path)

    # Total number of variants
    total_variants = len(df)

    # Handle level analysis directly using the 'Level' column
    level_counts = df['Level'].value_counts().to_dict()
    max_level = df['Level'].max()

    # Build parent-child map
    tree = defaultdict(list)
    for _, row in df.iterrows():
        parent = None if row['Parent ID'] == "ROOT" else int(row['Parent ID'])
        tree[parent].append(int(row['Variant ID']))

    # Number of clusters = number of children under root
    num_clusters = len(tree[None])

    # Output summary
    print("\n📊 Variant Tree Analysis:")
    print(f"🔢 Total variants: {total_variants}")
    print(f"🌲 Tree depth (max level): {max_level}")
    print(f"🌿 Number of clusters (children of most common variant): {num_clusters}")
    print(f"🧱 Nodes per level:")
    for level in sorted(level_counts):
        print(f"  - Level {level}: {level_counts[level]} nodes")