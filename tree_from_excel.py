import pandas as pd
from anytree import Node, RenderTree

# Read Excel
df = pd.read_excel("КАТО_19.05.2025.xls", usecols=["te", "rus_name"])

# Format KATO codes as 9-digit strings
df["te"] = df["te"].astype(str).str.zfill(9)

# Create a dictionary for fast lookup
code_to_name = dict(zip(df["te"], df["rus_name"]))
code_to_node = {}

# Create root
root = Node("Kazakhstan", code="00")
code_to_node["00"] = root

# Sort codes to ensure parents come before children
for code in sorted(df["te"]):
    node = Node(code_to_name[code], code=code)
    code_to_node[code] = node

for code in sorted(df["te"]):
    node = code_to_node[code]
    parent_code = code[:-2] + "00"  
    
    if parent_code in code_to_node:
        node.parent = code_to_node[parent_code]
        else:
            node.parent = root
            if parent_code == code:
                print(f"Warning: node {code} has itself as parent. Skipping.")
                continue
    
    
    


with open("tree_excel.txt", "w", encoding="utf-8") as f:
    for pre, _, node in RenderTree(root):
        f.write(f"{pre}{node.name} \t ({node.code})\n")
