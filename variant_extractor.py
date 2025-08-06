from collections import Counter

def extract_variants(df):
    """
    Extracts and counts all unique process variants from an event log DataFrame.

    Returns:
        - variants_dict: a dict of {variant_tuple: frequency}
        - sorted_variants: a list of (variant_tuple, frequency) sorted by frequency desc
    """
    # Sort by case and timestamp to preserve order of events
    df_sorted = df.sort_values(by=['case_id', 'timestamp'])

    # Group activities by case_id in order
    grouped = df_sorted.groupby('case_id')['activity'].apply(list)

    # Count unique activity sequences
    variant_counter = Counter(tuple(variant) for variant in grouped)

    # Sort variants by frequency
    sorted_variants = sorted(variant_counter.items(), key=lambda x: x[1], reverse=True)

    return dict(variant_counter), sorted_variants
