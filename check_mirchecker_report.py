import os
import csv
from Const import *

root_dir = MIRCHECKER3_REPORT_DIR
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
"RUSTSEC-2020-0028, GHSA-8q2v-67v7-6vc6",
"RUSTSEC-2020-0048, GHSA-v3j6-xf77-8r9c",
"GHSA-6x52-88cq-55q5",
"GHSA-pf3p-x6qj-6j7q, RUSTSEC-2020-0081",
"RUSTSEC-2020-0059, GHSA-rh4w-94hh-9943",
"GHSA-67hm-27mx-9cg7",
"GHSA-p24j-h477-76q3, RUSTSEC-2021-0106",
"RUSTSEC-2021-0071",
"RUSTSEC-2020-0009, GHSA-c9h5-hf8r-m97x",
"RUSTSEC-2021-0124, GHSA-fg7r-2g4j-5cgr",
"GHSA-6mv3-wm7j-h4w5",
"GHSA-44mr-8vmm-wjhg, RUSTSEC-2022-0076",
"GHSA-2hvr-h6gw-qrxp",
"GHSA-8v4j-7jgf-5rg9, RUSTSEC-2022-0082",
"GHSA-8mj7-wxmc-f424, RUSTSEC-2022-0028",
"GHSA-6r8p-hpg7-825g",
"GHSA-4mq4-7rw3-vm5j",
"GHSA-r64r-5h43-26qv",
"GHSA-w3vp-jw9m-f9pm",
"RUSTSEC-2023-0064, GHSA-rrjw-j4m2-mf34",
"GHSA-vx24-x4mv-vwr5",
"RUSTSEC-2024-0336, GHSA-6g7w-8wpp-frhj",
"GHSA-3qx3-6hxr-j2ch",
"GHSA-52xf-5p2m-9wrv",
"GHSA-67fv-9r7g-432h",
]
for cve in specific_cve:
    target_report = next((report["total"] for report in results if report["cve_id"] == cve),None)
    print(target_report)
    # if target_report:
    #     print(target_report)