from graphviz import Digraph


def parse_tree_txt(file_path):
    tree = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            visual, label = parts
            indent = visual.count("│") + visual.count("    ") + visual.count("─") // 2
            name = visual.strip("├└─│ ")
            code = label.strip("()")
            tree.append((indent, name, code))
    return tree


def build_node_map(tree):
    """Returns a flat map of level -> node and node relationships."""
    level_stack = {}
    edges = []
    nodes = set()

    for level, name, code in tree:
        node_id = f"{name} ({code})"
        nodes.add(node_id)
        level_stack[level] = node_id
        if level > 0 and (level - 1) in level_stack:
            parent = level_stack[level - 1]
            edges.append((parent, node_id))

    return nodes, edges


def compare_and_visualize_trees(file1, file2, output="tree_comparison", fmt="png", max_nodes=None):
    tree1 = parse_tree_txt(file1)
    tree2 = parse_tree_txt(file2)

    nodes1, edges1 = build_node_map(tree1)
    nodes2, edges2 = build_node_map(tree2)

    all_nodes = nodes1.union(nodes2)

    dot = Digraph(name="Comparison")
    dot.attr(rankdir="LR")  # Left to right layout
    dot.attr("node", shape="box", style="filled", fontname="Arial", fontsize="10")

    # Virtual root for clarity
    dot.node("EXCEL_TREE", label="Excel Tree", fillcolor="lightblue")
    dot.node("API_TREE", label="API Tree", fillcolor="lightgreen")

    count = 0
    for node in all_nodes:
        if max_nodes and count >= max_nodes:
            break
        in1 = node in nodes1
        in2 = node in nodes2

        if in1 and in2:
            color = "white"
        else:
            color = "red"

        dot.node(node, fillcolor=color)
        count += 1

    for src, dst in edges1:
        if max_nodes and (src not in dot.body or dst not in dot.body):
            continue
        dot.edge(src, dst)
        if src not in nodes2:
            dot.edge("EXCEL_TREE", src)

    for src, dst in edges2:
        if max_nodes and (src not in dot.body or dst not in dot.body):
            continue
        dot.edge(src, dst)
        if src not in nodes1:
            dot.edge("API_TREE", src)

    dot.render(filename=output, format=fmt, cleanup=True)
    print(f"Comparison tree saved to {output}.{fmt}")
