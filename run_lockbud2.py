#!/usr/bin/env python3
import os
import os.path
from Const import *
from Env import *
from TestCase import *
import Lockbud
import csv
import pandas as pd
import ast
import shutil
import Worker


def run_test(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = LOCKBUD2_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = LOCKBUD2_RUSTC_VERSION
    if WASM_TARGET_ENABLE:
        env_dict["CARGO_BUILD_TARGET"] = WASM_TARGET
    Lockbud.run_lockbud_cmd(test_case,env_dict)
    return test_case



if __name__ == "__main__":
    metadata_file = "./metadata.csv"
    df = pd.read_csv(metadata_file)
    df['cmd_excute_path'] = df['cmd_excute_path'].apply(lambda x: ast.literal_eval(x))


    test_cases = []
    for index, row in df.iterrows():
        if not row['cve_id']=="GHSA-8v4j-7jgf-5rg9, RUSTSEC-2022-0082":
            continue
        cmd_excute_paths = row['cmd_excute_path']
        cve_repo_path = row['cve_repo_path']
        lockbud_report_path = os.path.dirname(os.path.dirname(cve_repo_path.replace(CVE_REPO_DIR,LOCKBUD2_REPORT_DIR)))
        if not os.path.exists(lockbud_report_path):
            os.makedirs(lockbud_report_path)
        else:
            shutil.rmtree(lockbud_report_path)
            os.makedirs(lockbud_report_path)
        test_case = TestCase.create_test_case(
            cve_repo_path,
            cmd_excute_paths,
            lockbud_report_path,
            )
        test_cases.append(test_case)

    
    report_state = Worker.run(test_cases,run_test)


    output_file = "lockbud2_reports_state.csv"
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["cve_id", "state", "success cnt", "failure cnt"])
        writer.writerows(report_state)

    print(f"Results have been written to {output_file}")