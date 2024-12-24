import os
import csv
from Const import *

root_dir = LOCKBUD2_REPORT_DIR

reports = []


for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        file_list = os.listdir(subdir_path)

        DoubleLock = 0
        ConflictLock = 0
        CondvarDeadlock = 0
        AtomicityViolation = 0
        InvalidFree = 0
        UseAfterFree = 0
        total = 0
        lockbud1 = False

        for file_name in file_list:
            file_path = os.path.join(subdir_path, file_name)
            if os.path.isfile(file_path) and file_name.startswith("lockbud_all_report"):
                with open(file_path, "r") as file:
                    content = file.read()
                    DoubleLock += content.count(r'"bug_kind": "DoubleLock"')
                    ConflictLock += content.count(r'"bug_kind": "ConflictLock"')
                    CondvarDeadlock += content.count(r'"bug_kind": "Deadlock before Condvar::wait and notify"')
                    AtomicityViolation += content.count(r'"bug_kind": "AtomicityViolation"')
                    InvalidFree += content.count(r'"bug_kind": "InvalidFree"')
                    UseAfterFree += content.count(r'"bug_kind": "UseAfterFree"')
                    total += DoubleLock + ConflictLock + CondvarDeadlock + AtomicityViolation + InvalidFree + UseAfterFree
                    lockbud1 = True
        reports.append([subdir, lockbud1, DoubleLock, ConflictLock, CondvarDeadlock, AtomicityViolation, InvalidFree, UseAfterFree, total])

# 
output_file = "lockbud_results.csv"
with open(output_file, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["cve_id",	"lockbud1",	"DoubleLock",	"ConflictLock", "CondvarDeadlock", "AtomicityViolation", "InvalidFree", "UseAfterFree", "total"])
    writer.writerows(reports)

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
    target_report = next((report[8] for report in reports if report[0] == cve),None)
    print(target_report)
    # if target_report:
    #     print(target_report)