import os
import csv
from Const import *

root_dir = PRUSTI_REPORT_DIR
verify_errors = [
'assertion might fail with "attempt to multiply with overflow"',
'assertion might fail with "attempt to divide by zero"',
'the array or slice index may be out of bounds',
'assertion might fail with "attempt to negate with overflow"',
'implicit type invariant expected by the function call might not hold.',
'unreachable!(..) statement might be reachable',
'statement might panic',
'value might not fit into the target type.',
'the range end value may be out of bounds when slicing',
'assertion might fail with "attempt to subtract with overflow"',
'the asserted expression might not hold',
'panic!(..) statement might be reachable',
'assertion might fail with "attempt to add with overflow"',
'the range end may be smaller than the start when slicing',
'assertion might fail with "attempt to calculate the remainder with a divisor of zero"',
'unimplemented!(..) statement might be reachable',
]
# 创建一个列表用于存储结果
results = []
# error_types = set()
# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        row = dict.fromkeys(verify_errors, 0)
        row["cve_id"] = subdir

        for file_name in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file_name)
            if os.path.isfile(file_path) and file_name.startswith("prusti_report"):
                
                with open(file_path, "r") as file:
                    lines = file.readlines()
                for line in lines:
                    if line.startswith('warning: [Prusti: verification error]'):
                        error_info = line[len('warning: [Prusti: verification error]'):].strip()
                        
                        for type in verify_errors:
                            if type in error_info:
                                row[type] += 1
        total = 0
        for type in verify_errors:
            total += row[type]
        row["total"] = total
        results.append(row)
                


# 如果需要查看具体的信息类型，可以打印集合
# print("不同的信息类型包括：")
# for error_type in error_types:
#     print(error_type+'\n')
output_file = "prusti_VE_results.csv"
# with open(output_file, "w", newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=["cve_id","error: [Prusti: internal error]"])
#     writer.writeheader()
#     writer.writerows(results)

with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["cve_id"]+verify_errors+["total"])
    writer.writeheader()
    writer.writerows(results)

print(f"Results have been written to {output_file}")


specific_cve = [
"GHSA-cqpr-pcm7-m3jc, RUSTSEC-2020-0159",
"RUSTSEC-2020-0073, GHSA-9wgh-vjj7-7433",
"RUSTSEC-2020-0123, GHSA-gvcp-948f-8f2p",
"RUSTSEC-2020-0001, GHSA-4cww-f7w5-x525",
"GHSA-q9h2-4xhf-23xx, RUSTSEC-2020-0096",
"RUSTSEC-2021-0105, GHSA-5xg3-j2j6-rcx4",
"GHSA-f3pg-qwvg-p99c, RUSTSEC-2021-0078",
"RUSTSEC-2021-0037, GHSA-j8q9-5rp9-4mv9",
"RUSTSEC-2021-0043, GHSA-w9vv-q986-vj7x",
"GHSA-gx5w-rrhp-f436",
"GHSA-x4mq-m75f-mx8m, RUSTSEC-2022-0008",
"GHSA-2gg5-7c4v-6xx2, RUSTSEC-2022-0055, GHSA-m77f-652q-wwp4",
"RUSTSEC-2022-0038, GHSA-4rx6-g5vg-5f3j",
"RUSTSEC-2022-0037, GHSA-xq3c-8gqm-v648",
"RUSTSEC-2022-0013, GHSA-m5pq-gvj9-9vr8",
"RUSTSEC-2023-0064, GHSA-rrjw-j4m2-mf34",
"RUSTSEC-2023-0078, GHSA-8f24-6m29-wm2r",
"RUSTSEC-2023-0063, GHSA-q8wc-j5m9-27w3",
"RUSTSEC-2023-0076",
"RUSTSEC-2023-0065, GHSA-9mcr-873m-xcxp",
"GHSA-c2hf-vcmr-qjrf, RUSTSEC-2024-0358",
"GHSA-w277-wpqf-rcfv, RUSTSEC-2024-0010, GHSA-747x-5m58-mq97",
"GHSA-q445-7m23-qrmw, RUSTSEC-2024-0357",
"RUSTSEC-2024-0003, GHSA-8r5v-vm4m-4g25",
"RUSTSEC-2024-0356, GHSA-4qg4-cvh2-crgg",
]
for cve in specific_cve:
    target_report = next((report["total"] for report in results if report["cve_id"] == cve),None)
    print(target_report)
    # if target_report:
    #     print(target_report)