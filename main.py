import os
import requests
import json
from urllib.parse import quote
from dotenv import load_dotenv
from collections import defaultdict
from tree_builder import build_tree
from downloader import fetch_data

from tree_from_excel import create_tree_from_excel

from compare_trees import compare_tree_files


load_dotenv()
API_KEY = os.getenv("API_KEY")

page_size = 100
offset = 0

all_results = fetch_data(API_KEY, offset, page_size)


tree_root = build_tree(all_results)

from anytree import RenderTree

# for pre, fill, node in RenderTree(tree_root):
#     if node.depth <= 1: 
#         print(f"{pre}{node.name} ({node.code})")

with open("tree_output.txt", "w", encoding="utf-8") as f:
    for pre, fill, node in RenderTree(tree_root):
        f.write(f"{pre}{node.name} \t ({node.code})\n")

create_tree_from_excel()

compare_tree_files("tree_excel.txt", "tree_output.txt")










