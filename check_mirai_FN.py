import os
import csv
from Const import *
import ast
import re
root_dir = MIRAI_REPORT_DIR
output_file = "mirai_FN_results.csv"
FN_results = {}
commit_modified_files = {}
with open("commit_modified_files.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        commit_modified_files[row["cve_id"]] = ast.literal_eval(row["modified_files"])

for cve_id in commit_modified_files.keys():
    subdir_path = os.path.join(root_dir, cve_id)
    FN_results[cve_id] = True
    if os.path.isdir(subdir_path):
        files = os.listdir(subdir_path)
        for file in files:
            if file.startswith("mirai_report"):
                with open(os.path.join(subdir_path, file), "r") as f:
                    content = f.read()
                    pattern = r'warning: \[MIRAI\].*?\n\s*-->\s*(.*?):\d+:\d+'
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if match in commit_modified_files[cve_id]:
                            FN_results[cve_id] = False
                            break
                


with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["cve_id","FN"])
    writer.writeheader()
    for cve_id in FN_results.keys():
        writer.writerow({"cve_id":cve_id,"FN":FN_results[cve_id]})

print(f"Results have been written to {output_file}")


