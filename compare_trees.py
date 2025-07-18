from anytree import Node

def compare_tree_files(file1_path, file2_path):
    with open(file1_path, "r", encoding="utf-8") as f1, open(file2_path, "r", encoding="utf-8") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    max_len = max(len(lines1), len(lines2))
    diffs = []

    for i in range(max_len):
        line1 = lines1[i].strip() if i < len(lines1) else None
        line2 = lines2[i].strip() if i < len(lines2) else None

        if line1 != line2:
            diffs.append(f"Line {i+1}:\n"
                         f"  Tree1: {line1 if line1 is not None else '[Missing]'}\n"
                         f"  Tree2: {line2 if line2 is not None else '[Missing]'}")

    if not diffs:
        print("✅ Trees are identical.")
    else:
        print("❌ Differences found:")
        for diff in diffs:
            print(diff)
