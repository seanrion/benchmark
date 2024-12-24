import os
import csv
from Const import *

root_dir = PRUSTI_REPORT_DIR

# 创建一个列表用于存储结果
results = []
error_types = set()
# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "prusti_report")
        if os.path.exists(stdout_file):
            # 读取stdout文件并检查是否包含"failed to parse manifest"字符串
            with open(stdout_file, "r") as file:
                lines = file.readlines()
            row = dict()
            row["cve_id"] = subdir
            row["error: [Prusti: internal error]"] = 0
            for line in lines:

                if line.startswith('error: [Prusti: internal error]'):
                    row["error: [Prusti: internal error]"] += 1
            results.append(row)
                


# 如果需要查看具体的信息类型，可以打印集合
# print("不同的信息类型包括：")
# for error_type in error_types:
#     print(error_type+'\n')
output_file = "prusti_IE_results.csv"
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["cve_id","error: [Prusti: internal error]"])
    writer.writeheader()
    writer.writerows(results)

# print(f"Results have been written to {output_file}")
