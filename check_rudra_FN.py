import os
import csv
import ast
from Const import *

root_dir = RUDRA3_REPORT_DIR
output_file = "rudra3_FN_results.csv"
# 创建一个列表用于存储结果
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
        report_files = [
            os.path.join(subdir_path, file_name) for file_name in files 
            if file_name.startswith('rudra_report') and os.path.isfile(os.path.join(subdir_path, file_name))
        ]
        for report_file in report_files:
            # report_file = report_files[0]
            with open(report_file, 'r', encoding='utf-8') as file:
                content = file.read()
                reports_content = content.split('[[reports]]')
                for report in reports_content[1:]:
                    lines = report.strip().split('\n')
                    parts = {}
                    for line in lines:
                        if ' = ' in line:
                            key, value = line.split(' = ', 1)
                            parts[key] = value

                    bug_type = parts.get('analyzer', '').split(':')[0].strip("'")
                    location = parts.get('location', '').split(':')[0].strip("'")
                    if location in commit_modified_files[cve_id]:
                        FN_results[cve_id] = False
                        break
# 将结果写入CSV文件

with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["cve_id","FN"])
    writer.writeheader()
    for cve_id in FN_results.keys():
        writer.writerow({"cve_id":cve_id,"FN":FN_results[cve_id]})

print(f"Results have been written to {output_file}")
exit()
