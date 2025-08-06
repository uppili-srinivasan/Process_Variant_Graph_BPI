def visualize_happy_path(variant, save_path="happy_path", format="svg"):
    from graphviz import Digraph
    import os

    # Ensure output directory exists
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

    dot = Digraph(format=format)
    dot.attr(rankdir='TB', dpi='300')  # Top to bottom (vertical), high resolution

    # Add nodes and edges
    for idx, event in enumerate(variant):
        node_id = f"{idx}"
        label = event
        dot.node(node_id, label, shape="box", style="filled", fillcolor="lightblue", fontsize="12")

        if idx > 0:
            dot.edge(f"{idx - 1}", node_id)

    # Render to file
    dot.render(filename=save_path, cleanup=True)
    print(f"✅ Saved {format.upper()} happy path to: {save_path}.{format}")
