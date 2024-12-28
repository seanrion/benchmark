#!/usr/bin/env python3
import os
import os.path
from Const import *
from Env import *
from TestCase import *
import Rudra
import csv
import pandas as pd
import ast
import shutil
import Worker

def run_test(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["RUDRA_REPORT_PATH"] = os.path.abspath(os.path.join(test_case.report_path, "rudra_report"))
    env_dict["LD_LIBRARY_PATH"] = RUDRA3_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = RUDRA3_RUSTC_VERSION
    env_dict["RUSTFLAGS"] = RUDRA3_RUSTFLAGS
    env_dict["PATH"] = RUDRA3_PATH + ":" + env_dict["PATH"]

    Rudra.run_rudra_cmd(test_case,env_dict)
    return test_case



if __name__ == "__main__":
    metadata_file = "./metadata.csv"
    df = pd.read_csv(metadata_file)
    df['cmd_excute_path'] = df['cmd_excute_path'].apply(lambda x: ast.literal_eval(x))
    df['workspace_members_path'] = df['workspace_members_path'].apply(lambda x: ast.literal_eval(x))

    test_cases = []
    for index, row in df.iterrows():
        # if not row['cve_id']=="GHSA-6x52-88cq-55q5":
        #     continue
        cve_id = row['cve_id']
        cmd_excute_paths = row['cmd_excute_path']
        cve_repo_path = row['cve_repo_path']
        workspace_members_path = row['workspace_members_path']
        rudra_report_path = os.path.dirname(os.path.dirname(cve_repo_path.replace(CVE_REPO_DIR,RUDRA3_REPORT_DIR)))
        if not os.path.exists(rudra_report_path):
            os.makedirs(rudra_report_path)
        else:
            shutil.rmtree(rudra_report_path)
            os.makedirs(rudra_report_path)
        test_case = TestCase.create_test_case(
            cve_repo_path,
            cmd_excute_paths,
            rudra_report_path,
            workspace_members_path=workspace_members_path
            )
        test_cases.append(test_case)

    
    report_state = Worker.run(test_cases,run_test)


    output_file = "rudra3_reports_state.csv"
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["cve_id", "state", "success cnt", "failure cnt"])
        writer.writerows(report_state)

    print(f"Results have been written to {output_file}")
