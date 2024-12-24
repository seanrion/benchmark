import os
import csv
import json
from Const import *

root_dir = SEMGREP_REPORT_DIR
Semgrep_warning = [
'rust.actix.command-injection.rust-actix-command-injection.rust-actix-command-injection',
'rust.actix.path-traversal.tainted-path.tainted-path',
'rust.actix.ssrf.reqwest-taint.reqwest-taint',
'rust.hyper.path-traversal.tainted-path.tainted-path',
'rust.lang.security.args-os.args-os',
'rust.lang.security.args.args',
'rust.lang.security.current-exe.current-exe',
'rust.lang.security.insecure-hashes.insecure-hashes',
'rust.lang.security.rustls-dangerous.rustls-dangerous',
'rust.lang.security.temp-dir.temp-dir',
'rust.lang.security.unsafe-usage.unsafe-usage'
]
# 创建一个列表用于存储结果
results = []
warning_types = set()
# 遍历所有二级文件夹

for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "semgrep_report.json")
        row = dict.fromkeys(Semgrep_warning, 0)
        row["cve_id"] = subdir
        row["total"] = 0
        if os.path.exists(stdout_file):

            with open(stdout_file, "r") as file:
                data = json.load(file)
                for result in data["results"]:
                    warning_types.add(result['check_id'])
                    row[result['check_id']] += 1
                    row["total"] += 1
        results.append(row)
                


# 如果需要查看具体的信息类型，可以打印集合
# print("不同的信息类型包括：")
# for error_type in warning_types:
#     print(error_type+'\n')
output_file = "Semgrep_results.csv"
# with open(output_file, "w", newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=["cve_id","error: [Prusti: internal error]"])
#     writer.writeheader()
#     writer.writerows(results)

with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["cve_id"]+Semgrep_warning+["total"])
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
    target_report = next((report for report in results if report["cve_id"] == cve),None)
    print(target_report["total"] - target_report['rust.lang.security.unsafe-usage.unsafe-usage'])
    # if target_report:
    #     print(target_report)
