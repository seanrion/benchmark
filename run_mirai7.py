#!/usr/bin/env python3
import os
import os.path
from Const import *
from Env import *
from TestCase import *
import MIRAI
import csv
import pandas as pd
import ast
import shutil
import Worker


def run_test(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = MIRAI7_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = MIRAI7_RUSTC_VERSION
    env_dict["MIRAI_FLAGS"] = "--diag=library"
    # env_dict["MIRAI_LOG"] = "debug"
    # env_dict["RUSTC_WRAPPER"] = "mirai"
    
    MIRAI.run_mirai_cmd(test_case,env_dict)
    return test_case



if __name__ == "__main__":
    metadata_file = "./metadata.csv"
    df = pd.read_csv(metadata_file)
    df['cmd_excute_path'] = df['cmd_excute_path'].apply(lambda x: ast.literal_eval(x))


    test_cases = []
    for index, row in df.iterrows():
        # if not row['cve_id']=="GHSA-pf3p-x6qj-6j7q, RUSTSEC-2020-0081":
        #     continue
        cmd_excute_paths = row['cmd_excute_path']
        cve_repo_path = row['cve_repo_path']
        mirai_report_path = os.path.dirname(os.path.dirname(cve_repo_path.replace(CVE_REPO_DIR,MIRAI7_REPORT_DIR)))
        if not os.path.exists(mirai_report_path):
            os.makedirs(mirai_report_path)
        else:
            shutil.rmtree(mirai_report_path)
            os.makedirs(mirai_report_path)
        test_case = TestCase.create_test_case(
            cve_repo_path,
            cmd_excute_paths,
            mirai_report_path,
            )
        test_cases.append(test_case)

    
    report_state = Worker.run(test_cases,run_test)


    output_file = "mirai7_reports_state.csv"
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["cve_id", "state", "success cnt", "failure cnt"])
        writer.writerows(report_state)

    print(f"Results have been written to {output_file}")