import pandas as pd
from anytree import Node, RenderTree

def create_tree_from_excel():
    # 1. Read Excel
    df = pd.read_excel("КАТО_19.05.2025.xls", usecols=["te", "rus_name"])

    # 2. Format KATO codes as 9-digit strings
    df["te"] = df["te"].astype(str).str.zfill(9)

    # 3. Create lookup dicts
    code_to_name = dict(zip(df["te"], df["rus_name"]))
    code_to_node = {}

    # 4. Create root node
    root = Node("Kazakhstan", code="00")
    code_to_node["00"] = root

    # 5. Create all nodes without parents
    for code in df["te"]:
        node = Node(code_to_name[code], code=code)
        code_to_node[code] = node

    # 6. Assign parents only from existing nodes
    for code in df["te"]:
        node = code_to_node[code]
        temp_code = code

        while True:
            temp_code = temp_code[:-2]
            if len(temp_code) < 2:
                node.parent = root
                break

            parent_code = temp_code.ljust(9, '0')
            if parent_code == code:
                node.parent = root
                break

            if parent_code in code_to_node:
                node.parent = code_to_node[parent_code]
                break

        if node.parent is None:
            node.parent = root

    # 7. Export to file
    with open("tree_excel.txt", "w", encoding="utf-8") as f:
        for pre, _, node in RenderTree(root):
            f.write(f"{pre}{node.name} \t ({node.code})\n")

