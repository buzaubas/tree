import svgwrite

def parse_tree_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    tree = []
    stack = [(tree, -1)]

    for line in lines:
        cleaned = line.lstrip("│").lstrip("├└─ ")
        # Кол-во отступов: считаем каждый блок из 4 пробелов или символ '│'
        indent = (len(line) - len(line.lstrip(' │'))) // 4
        node = {"name": cleaned, "children": []}

        while stack and indent <= stack[-1][1]:
            stack.pop()
        stack[-1][0].append(node)
        stack.append((node["children"], indent))

    return tree

def flatten_tree(tree, prefix=''):
    result = []
    for node in tree:
        full_name = prefix + node["name"]
        result.append(full_name)
        result.extend(flatten_tree(node["children"], prefix + '  '))
    return result

def draw_tree(dwg, tree, x, y, missing_nodes=None, line_height=20, indent=20):
    def _draw(node_list, level, y_offset):
        for node in node_list:
            color = "red" if missing_nodes and node["name"] in missing_nodes else "black"
            dwg.add(dwg.text("  " * level + node["name"], insert=(x + level * indent, y_offset), fill=color, font_size="14px", font_family="Arial"))
            y_offset += line_height
            y_offset = _draw(node["children"], level + 1, y_offset)
        return y_offset

    return _draw(tree, 0, y)

def compare_and_draw_svg(file1, file2, output_svg="comparison.svg"):
    tree1 = parse_tree_file(file1)
    tree2 = parse_tree_file(file2)

    flat1 = set(flatten_tree(tree1))
    flat2 = set(flatten_tree(tree2))

    missing_in_1 = flat2 - flat1
    missing_in_2 = flat1 - flat2

    dwg = svgwrite.Drawing(output_svg, profile='full', size=("2000px", "400000px"))
    dwg.add(dwg.text("API Мин Цифры", insert=(50, 20), font_size="18px", font_weight="bold"))
    dwg.add(dwg.text("Бюро Нац Статистики", insert=(1050, 20), font_size="18px", font_weight="bold"))

    draw_tree(dwg, tree1, x=50, y=40, missing_nodes=missing_in_2)
    draw_tree(dwg, tree2, x=1050, y=40, missing_nodes=missing_in_1)

    dwg.save()
    print(f"SVG saved to {output_svg}")

