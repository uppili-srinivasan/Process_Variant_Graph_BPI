import matplotlib.pyplot as plt
import os
import csv

def plot_variant_distribution(pareto_variants, save_path="output/variant_distribution.png", max_display=50):
    """
    Plots a bar chart of the Pareto-filtered variants and saves the plot.
    Caps the height of the figure to avoid rendering issues with matplotlib.

    Parameters:
        pareto_variants (list): List of (variant_tuple, freq) tuples.
        save_path (str): File path to save the plot image.
        max_display (int): Max number of variants to show in the plot.
    """
    total_variants = len(pareto_variants)
    if total_variants > max_display:
        print(f"⚠️ Too many variants to display ({total_variants}). Truncating to top {max_display} for visualization.")
        pareto_variants = pareto_variants[:max_display]

    # Prepare variant strings and frequencies
    variants = [" → ".join(v[0]) for v in pareto_variants]
    freqs = [v[1] for v in pareto_variants]

    # Delete existing file if it exists
    if os.path.exists(save_path):
        os.remove(save_path)

    # Create horizontal bar chart
    height_per_variant = 0.4
    fig_height = max(4, height_per_variant * len(variants))
    fig_height = min(fig_height, 40)  # Cap max height to prevent overflow

    plt.figure(figsize=(12, fig_height))
    bars = plt.barh(range(len(variants)), freqs, color='skyblue')
    plt.yticks(range(len(variants)), variants, fontsize=8)
    plt.xlabel("Frequency")
    plt.title(f"Pareto-Based Variant Distribution (Top {len(variants)} Variants)")
    plt.gca().invert_yaxis()

    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2, f"{freqs[i]}", va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"📈 Variant distribution plot saved as: {save_path}")


def save_variants_to_csv(pareto_variants, csv_path="output/pareto_variants.csv"):
    """
    Saves the full list of Pareto-filtered variants and their frequencies to a CSV file.

    Parameters:
        pareto_variants (list): List of (variant_tuple, freq) tuples.
        csv_path (str): File path to save the CSV.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Variant", "Frequency"])

        for variant_tuple, freq in pareto_variants:
            variant_str = " → ".join(variant_tuple)
            writer.writerow([variant_str, freq])

    print(f"📄 Full Pareto variant list saved to: {csv_path}")
