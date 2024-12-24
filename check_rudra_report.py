import os
import csv
from Const import *

root_dir = RUDRA3_REPORT_DIR

# 创建一个列表用于存储结果
reports = []

# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    # if not subdir=="ash-0.31.0":
    #     continue
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        files = os.listdir(subdir_path)
        report_files = [
            os.path.join(subdir_path, file_name) for file_name in files 
            if file_name.startswith('rudra_report') and os.path.isfile(os.path.join(subdir_path, file_name))
        ]
        report_stat = {
            "cve_id":subdir,
            "report_exist":False,
        }
        bug_counts = {
            "UnsafeDestructor":0,
            "SendSyncVariance":0,
            "UnsafeDataflow":0,
            "total":0
        }
        unique_locations = set()
        if report_files:
            report_stat["report_exist"] = True
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
                    location = parts.get('location', '')
                    if location and not location in unique_locations:
                        unique_locations.add(location)
                        if bug_type:
                            bug_counts[bug_type] += 1
                            bug_counts["total"] += 1

                    
        report_stat.update(bug_counts)
        reports.append(report_stat)




# 将结果写入CSV文件
output_file = "rudra1_report_results.csv"
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["cve_id",	"report_exist",	"UnsafeDestructor", "SendSyncVariance", "UnsafeDataflow", "total"])
    writer.writeheader()
    for row in reports:
        # print(row)
        writer.writerow(row)

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
    target_report = next((report for report in reports if report["cve_id"] == cve),None)
    print(target_report["total"])
    # if target_report:
    #     print(target_report)