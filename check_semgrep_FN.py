import os
import csv
import json
from Const import *
import ast
root_dir = SEMGREP_REPORT_DIR
output_file = "semgrep_FN_results.csv"
FN_results = {}
commit_modified_files = {}
with open("commit_modified_files.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        commit_modified_files[row["cve_id"]] = ast.literal_eval(row["modified_files"])
# 创建一个列表用于存储结果
results = []
warning_types = set()
# 遍历所有二级文件夹

for cve_id in commit_modified_files.keys():
    subdir_path = os.path.join(root_dir, cve_id)
    FN_results[cve_id] = True
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "semgrep_report.json")
        path = set()
        if os.path.exists(stdout_file):
            with open(stdout_file, "r") as file:
                data = json.load(file)
                for result in data["results"]:
                    # if result['path'] == 'rust.lang.security.unsafe-usage.unsafe-usage':
                    #     continue
                    path = result['path']
                    if path in commit_modified_files[cve_id]:
                        FN_results[cve_id] = False
                        break

with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["cve_id","FN"])
    writer.writeheader()
    for cve_id in FN_results.keys():
        writer.writerow({"cve_id":cve_id,"FN":FN_results[cve_id]})

print(f"Results have been written to {output_file}")
exit()
