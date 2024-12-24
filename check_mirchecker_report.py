import os
import csv
from Const import *

root_dir = MIRCHECKER2_REPORT_DIR
verify_errors = [
'which would overflow',
]
# 创建一个列表用于存储结果
results = []
error_types = set()
# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        row = dict()
        row["cve_id"] = subdir
        row['total'] = 0
        for root, dirs, files in os.walk(subdir_path):
            for file in files:
                if file.startswith("mirchecker"):
                    file_path = os.path.join(root, file)
                    # print(file_path)

                    with open(file_path, "r") as file:
                        lines = file.readlines()
                    
                    
                    for line in lines:
                        if line.startswith('warning: [MirChecker]'):
                            error_info = line[len('warning: [MirChecker]'):].strip()


                            if 'which would overflow' in error_info: 
                                error_types.add('overflow')
                                row['overflow'] = row.get('overflow', 0) + 1
                            elif 'index out of bound' in error_info:
                                error_types.add('index out of bound')
                                row['index out of bound'] = row.get('index out of bound', 0) + 1
                            elif 'with a divisor of zero' in error_info or 'by zero' in error_info:
                                error_types.add('ZeroDivision')
                                row['ZeroDivision'] = row.get('ZeroDivision', 0) + 1
                            elif 'run into panic code' in error_info:
                                error_types.add('panic')
                                row['panic'] = row.get('panic', 0) + 1
                            elif 'double-free or use-after-free' in error_info:
                                error_types.add('double-free or use-after-free')
                                row['double-free or use-after-free'] = row.get('double-free or use-after-free', 0) + 1
                            else:
                                error_types.add(error_info)
                                row[error_info] = row.get(error_info, 0) + 1

                            row['total'] += 1
        results.append(row)
                


# 如果需要查看具体的信息类型，可以打印集合
# print("不同的信息类型包括：")
# print(len(error_types))
# for error_type in error_types:
#     print(error_type+'\n')
output_file = "mirchecker_results.csv"
# with open(output_file, "w", newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=["cve_id","error: [Prusti: internal error]"])
#     writer.writeheader()
#     writer.writerows(results)

all_keys = sorted(error_types)
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["cve_id"]+all_keys)
    writer.writeheader()
    for d in results:
        # 使用字典推导式设置缺失的键为 0
        row = {key: d.get(key, 0) for key in ['cve_id']+all_keys}
        writer.writerow(row)
    # writer.writerows(results)
    # writer = csv.writer(csvfile)
    # for e in error_types:
    #     writer.writerow([e])
print(f"Results have been written to {output_file}")

specific_cve = [
"GHSA-pf3p-x6qj-6j7q, RUSTSEC-2020-0081",
"RUSTSEC-2021-0071",
]
for cve in specific_cve:
    target_report = next((report["total"] for report in results if report["cve_id"] == cve),None)
    print(target_report)
    # if target_report:
    #     print(target_report)