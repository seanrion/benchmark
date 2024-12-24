import os
import csv
from Const import *

root_dir = LOCKBUD2_REPORT_DIR

reports = []


for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "lockbud_panic_report")
        if os.path.exists(stdout_file):
            with open(stdout_file, "r") as file:
                content = file.read()
                Panic = content.count(r'PANIC[')
                reports.append([subdir, True, Panic])

# 
output_file = "lockbud_panic_results.csv"
with open(output_file, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["cve_id",	"lockbud1",	"Panic"])
    writer.writerows(reports)

print(f"Results have been written to {output_file}")
