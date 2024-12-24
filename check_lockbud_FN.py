import os
import csv
import ast
from Const import *

root_dir = LOCKBUD2_REPORT_DIR
output_file = "lockbud2_FN_results.csv"
FN_results = {}
commit_modified_files = {}
with open("commit_modified_files.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        commit_modified_files[row["cve_id"]] = ast.literal_eval(row["modified_files"])


import re
import json

def extract_atomicity_violations(log_data):
    pattern = re.compile(r'"AtomicityViolation":\s*{(.*?)}\s*}', re.DOTALL)
    matches = pattern.findall(log_data)
    locationfile = set()
    for match in matches:
        json_data = '{' + match + '}'
        try:
            violation_info = json.loads(json_data)
            # print("AtomicityViolation Info:")
            # print(f"Bug Kind: {violation_info['bug_kind']}")
            # print(f"Possibility: {violation_info['possibility']}")
            # print(f"Function Name: {violation_info['diagnosis']['fn_name']}")
            # print(f"Atomic Reader: {violation_info['diagnosis']['atomic_reader']}")
            # print(f"Atomic Writer: {violation_info['diagnosis']['atomic_writer']}")
            # print(f"Dependency Kind: {violation_info['diagnosis']['dep_kind']}")
            # print(f"Explanation: {violation_info['explanation']}")
            # print("\n")
            locationfile.add(violation_info['diagnosis']['atomic_reader'].split(":")[0])
            locationfile.add(violation_info['diagnosis']['atomic_writer'].split(":")[0])
        except json.JSONDecodeError as e:
            print("AtomicityViolation Info:")
            print(f"Error decoding JSON: {e}")
            raise e
    return locationfile

def extract_use_after_free(log_data):
    pattern = re.compile(r'"UseAfterFree":\s*{(.*?)}\s*}', re.DOTALL)
    matches = pattern.findall(log_data)
    locationfile = set()
    for match in matches:
        json_data = '{' + match + '}'
        try:
            violation_info = json.loads(json_data)
            # print("UseAfterFree Info:")
            # print(f"Bug Kind: {violation_info['bug_kind']}")
            # print(f"Possibility: {violation_info['possibility']}")
            # print(f"Diagnosis: {violation_info['diagnosis']}")
            # print(f"Explanation: {violation_info['explanation']}")
            # print("\n")
            path_pattern = re.compile(r'(/[^:]+):\d+:\d+')
            path_matches = path_pattern.findall(violation_info['diagnosis'])
            for i, path in enumerate(path_matches, start=1):
                locationfile.add(path)
        except json.JSONDecodeError as e:
            print("UseAfterFree Info:")
            print(f"Error decoding JSON: {e}")
            raise e
    return locationfile

def extract_double_lock(log_data):
    pattern = re.compile(r'"DoubleLock":\s*{(.*?)}\s*}', re.DOTALL)
    matches = pattern.findall(log_data)
    locationfile = set()
    for match in matches:
        json_data = '{' + match + '}'
        try:
            violation_info = json.loads(json_data)
            # print("DoubleLock Info:")
            # print(f"Bug Kind: {violation_info['bug_kind']}")
            # print(f"Possibility: {violation_info['possibility']}")
            # print(f"First_lock_type: {violation_info['diagnosis']['first_lock_type']}")
            # print(f"First_lock_span: {violation_info['diagnosis']['first_lock_span']}")
            # print(f"Second_lock_type: {violation_info['diagnosis']['second_lock_type']}")
            # print(f"Second_lock_span: {violation_info['diagnosis']['second_lock_span']}")
            # print(f"Callchains: {violation_info['diagnosis']['callchains']}")
            # print(f"Explanation: {violation_info['explanation']}")
            # print("\n")
            locationfile.add(violation_info['diagnosis']['first_lock_span'].split(":")[0])
            locationfile.add(violation_info['diagnosis']['second_lock_span'].split(":")[0])
        except json.JSONDecodeError as e:
            print("DoubleLock Info:")
            print(f"Error decoding JSON: {e}")
            raise e
    return locationfile

def extract_conflict_lock(log_data):
    pattern = re.compile(r'"ConflictLock":\s*{(.*?)}\s*}', re.DOTALL)
    matches = pattern.findall(log_data)
    locationfile = set()
    for match in matches:
        json_data = '{' + match + '}'
        try:
            violation_info = json.loads(json_data)
            # print("ConflictLock Info:")
            # print(f"Bug Kind: {violation_info['bug_kind']}")
            # print(f"Possibility: {violation_info['possibility']}")
            for diagnosis in violation_info['diagnosis']:
                # print(f"First_lock_type: {diagnosis['first_lock_type']}")
                # print(f"First_lock_span: {diagnosis['first_lock_span']}")
                # print(f"Second_lock_type: {diagnosis['second_lock_type']}")
                # print(f"Second_lock_span: {diagnosis['second_lock_span']}")
                # print(f"Callchains: {diagnosis['callchains']}")
                locationfile.add(diagnosis['first_lock_span'].split(":")[0])
                locationfile.add(diagnosis['second_lock_span'].split(":")[0])
            # print(f"Explanation: {violation_info['explanation']}")
            # print("\n")
        except json.JSONDecodeError as e:
            print("ConflictLock Info:")
            print(f"Error decoding JSON: {e}")
            raise e
    return locationfile

def extract_condvar_deadlock(log_data):
    pattern = re.compile(r'"CondvarDeadlock":\s*{(.*?)}\s*}', re.DOTALL)
    matches = pattern.findall(log_data)
    locationfile = set()
    for match in matches:
        json_data = '{' + match + '}'
        try:
            violation_info = json.loads(json_data)
            # print("CondvarDeadlock Info:")
            # print(f"Bug Kind: {violation_info['bug_kind']}")
            # print(f"Possibility: {violation_info['possibility']}")
            # print(f"Condvar_wait_type: {violation_info['diagnosis']['condvar_wait_type']}")
            # print(f"Condvar_wait_callsite_span: {violation_info['diagnosis']['condvar_wait_callsite_span']}")
            # print(f"Condvar_notify_type: {violation_info['diagnosis']['condvar_notify_type']}")
            # print(f"Condvar_notify_callsite_span: {violation_info['diagnosis']['condvar_notify_callsite_span']}")
            # print(f"Deadlocks: {violation_info['diagnosis']['deadlocks']}")
            # print(f"Explanation: {violation_info['explanation']}")
            # print("\n")
            locationfile.add(violation_info['diagnosis']['condvar_wait_callsite_span'].split(":")[0])
            locationfile.add(violation_info['diagnosis']['condvar_notify_callsite_span'].split(":")[0])
        except json.JSONDecodeError as e:
            print("CondvarDeadlock Info:")
            print(f"Error decoding JSON: {e}")
            raise e
    return locationfile

def extract_invalid_free(log_data):
    pattern = re.compile(r'"InvalidFree":\s*{(.*?)}\s*}', re.DOTALL)
    matches = pattern.findall(log_data)
    locationfile = set()
    for match in matches:
        json_data = '{' + match + '}'
        try:
            violation_info = json.loads(json_data)
            # print("InvalidFree Info:")
            # print(f"Bug Kind: {violation_info['bug_kind']}")
            # print(f"Possibility: {violation_info['possibility']}")
            # print(f"Diagnosis: {violation_info['diagnosis']}")
            # print(f"Explanation: {violation_info['explanation']}")
            # print("\n")
            path_pattern = re.compile(r'(/[^:]+):\d+:\d+')
            path_matches = path_pattern.findall(violation_info['diagnosis'])
            for i, path in enumerate(path_matches, start=1):
                locationfile.add(path)
        except json.JSONDecodeError as e:
            print("InvalidFree Info:")
            print(f"Error decoding JSON: {e}")
            raise e
    return locationfile

for cve_id in commit_modified_files.keys():
    subdir_path = os.path.join(root_dir, cve_id)
    FN_results[cve_id] = True
    if os.path.isdir(subdir_path):
        file_list = os.listdir(subdir_path)
        for file_name in file_list:
            file_path = os.path.join(subdir_path, file_name)
            if os.path.isfile(file_path) and file_name.startswith("lockbud_all_report"):
                with open(file_path, "r") as file:
                    content = file.read()
                    try:
                        atomicity_violations_location_files = extract_atomicity_violations(content)
                        use_after_free_location_files = extract_use_after_free(content)
                        double_lock_location_files = extract_double_lock(content)
                        conflict_lock_location_files = extract_conflict_lock(content)
                        condvar_deadlock_location_files = extract_condvar_deadlock(content)
                        invalid_free_location_files = extract_invalid_free(content)
                        total_location_files = atomicity_violations_location_files | use_after_free_location_files | double_lock_location_files | conflict_lock_location_files | condvar_deadlock_location_files | invalid_free_location_files
                        for commit_modified_file in commit_modified_files[cve_id]:
                            for location_file in total_location_files:
                                if commit_modified_file != '' and commit_modified_file in location_file:
                                    FN_results[cve_id] = False
                                    break
                    except Exception as e:
                        print(file_path)

with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["cve_id","FN"])
    writer.writeheader()
    for cve_id in FN_results.keys():
        writer.writerow({"cve_id":cve_id,"FN":FN_results[cve_id]})

print(f"Results have been written to {output_file}")

