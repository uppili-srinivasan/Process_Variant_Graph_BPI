def pareto_cutoff_variants(sorted_variants, total_cases, threshold=0.8):
    cumulative = 0
    top_variants = []
    
    for variant, count in sorted_variants:
        cumulative += count
        top_variants.append((variant, count))
        if cumulative / total_cases >= threshold:
            break
    return top_variants
