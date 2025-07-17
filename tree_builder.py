from anytree import Node

def build_tree(data):
    root = Node("Казахстан", code=0)
    id_to_node = {}

    for item in data:
        if item.get('IsMarkedToDelete'):
            continue
        code = item.get('Code')
        name = item.get('NameRus') or item.get('NameKaz')
        node_id = item.get('Id')
        node = Node(name, code=code)
        id_to_node[node_id] = node

    for item in data:
        if item.get('IsMarkedToDelete'):
            continue

        node_id = item.get('Id')
        parent_id = item.get('Parent')
        node = id_to_node.get(node_id)

        if node is None:
            continue

        if parent_id in (None, "", 0):
            node.parent = root
        elif parent_id == node_id:
            print(f"⚠️ Warning: node {node_id} has itself as parent. Skipping.")
            continue
        else:
            parent_node = id_to_node.get(parent_id)
            if parent_node:
                node.parent = parent_node
            else:
                print(f"⚠️ Warning: parent {parent_id} not found for node {node.name} (id={node_id})")

    return root
