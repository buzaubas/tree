import re
from collections import defaultdict

def get_level(line):
    """Estimate tree depth by counting indent (│, └, ├ and whitespace)."""
    match = re.match(r"^[\s│├└─]*", line)
    if match:
        return match.group(0).count("│") + match.group(0).count("    ") + match.group(0).count("─") // 2
    return 0

def compare_tree_files(file1_path, file2_path):
    with open(file1_path, "r", encoding="utf-8") as f1, open(file2_path, "r", encoding="utf-8") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    max_len = max(len(lines1), len(lines2))
    diffs = []
    level_diff_count = defaultdict(int)

    for i in range(max_len):
        line1 = lines1[i].rstrip() if i < len(lines1) else None
        line2 = lines2[i].rstrip() if i < len(lines2) else None

        if line1 != line2:
            level = get_level(line1 or line2 or "")
            level_diff_count[level] += 1
            diffs.append(f"Line {i+1} (Level {level}):\n"
                         f"  Tree1: {line1 if line1 is not None else '[Missing]'}\n"
                         f"  Tree2: {line2 if line2 is not None else '[Missing]'}")

    if not diffs:
        print("Trees are identical.")
    else:
        print("Differences found:\n")
        for diff in diffs:
            print(diff)

        print("\nSummary of Differences by Level:")
        for level in sorted(level_diff_count):
            print(f"  Level {level}: {level_diff_count[level]} difference(s)")
