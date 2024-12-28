#!/usr/bin/env python3
import os
import os.path
from TestCase import *
import csv
import shutil
import tempfile
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
import threading

success_cnt = 0
failure_cnt = 0
semgrep_report_dir_cmd = {
    "./semgrep0.77.0":"conda run -n semgrep0.77.0 semgrep scan --config p/rust --json --output".split(),
    "./semgrep0.86.5":"conda run -n semgrep0.86.5 semgrep scan --config p/rust --json --output".split(),
    "./semgrep0.101.1":"conda run -n semgrep0.101.1 semgrep scan --config p/rust --json --output".split(),
    "./semgrep0.115.0":"conda run -n semgrep0.115.0 semgrep scan --config p/rust --json --output".split(),
    "./semgrep1.2.1":"conda run -n semgrep1.2.1 semgrep scan --config p/rust --json --output".split(),
    "./semgrep1.16.0":"conda run -n semgrep1.16.0 semgrep scan --config p/rust --pro --json --output".split(),
    "./semgrep1.30.0":"conda run -n semgrep1.30.0 semgrep scan --config p/rust --pro --json --output".split(),
    "./semgrep1.42.0":"conda run -n semgrep1.42.0 semgrep scan --config p/rust --pro --json --output".split(),
    "./semgrep1.54.3":"conda run -n semgrep1.54.3 semgrep scan --config p/rust --pro --json --output".split(),
    "./semgrep1.67.0":"conda run -n semgrep1.67.0 semgrep scan --config p/rust --pro --json --output".split(),
    "./semgrep1.78.0":"conda run -n semgrep1.78.0 semgrep scan --config p/rust --pro --json --json-output".split(),
    "./semgrep1.90.0":"conda run -n semgrep1.90.0 semgrep scan --config p/rust --pro --json --json-output".split(),
    "./semgrep1.101.0":"conda run -n semgrep1.101.0 semgrep scan --config p/rust --pro --json --json-output".split(),
}
def run_test(test_case:TestCase,cmd):
    env_dict = dict(os.environ)    
    run_semgrep_cmd(test_case,env_dict,cmd)
    return test_case

def run_semgrep_cmd(test_case:TestCase,env_dict:dict,cmd):
    cmd = cmd.copy()
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        cmd.append(os.path.abspath(temp_file.name))
    run_cmd(test_case,cmd,env_dict,cwd=test_case.repo_path,output_file=test_case.out_file,error_file=test_case.error_file)
    with open(temp_file.name, 'rb') as temp_file:
        with open(test_case.semgrep_report, 'wb') as destination_file:
            shutil.copyfileobj(temp_file, destination_file)

def run(test_cases,cmd,run_test):
    progress_bar = tqdm(total=len(test_cases), desc="Processing test cases")
    report_state = []
    def update_progress_bar(test_case:TestCase):
        with threading.Lock():
            global success_cnt,failure_cnt
            success_cnt += test_case.success_cnt
            failure_cnt += test_case.failure_cnt
            report_state.append([os.path.basename(test_case.report_path),test_case.success,test_case.success_cnt,test_case.failure_cnt])
            progress_bar.update()

    with ThreadPool(THREAD_NUM) as pool:
        results = []
        for test_case in test_cases:
            results.append(
                pool.apply_async(run_test, (test_case,cmd), 
                                 callback=update_progress_bar
                                 ))
        
        for result in results:
            result.get()
    return report_state

def test(report_dir,cmd):
    cve_repos = {os.path.join(CVE_REPO_DIR, d): os.path.join(report_dir, d) for d in os.listdir(CVE_REPO_DIR) if os.path.isdir(os.path.join(CVE_REPO_DIR, d))}

    
    for repo in list(cve_repos.keys()):
        buggy_dir = os.path.join(repo, "buggy")
        value = cve_repos.pop(repo)
        if os.path.isdir(buggy_dir):
            first_buggy_subdir = next((os.path.join(buggy_dir, d) for d in os.listdir(buggy_dir) if os.path.isdir(os.path.join(buggy_dir, d))), None)
            if first_buggy_subdir:
                new_key = first_buggy_subdir
                cve_repos[new_key] = value
            else:
                print(f"No buggy subdirectory found for {repo}")

    test_cases = []
    for cve_repo_path,semgrep_report_path in cve_repos.items():
        if not os.path.exists(semgrep_report_path):
            os.makedirs(semgrep_report_path)
        else:
            shutil.rmtree(semgrep_report_path)
            os.makedirs(semgrep_report_path)
        test_case = TestCase.create_test_case(
            cve_repo_path,
            cve_repo_path,
            semgrep_report_path,
            )
        test_cases.append(test_case)

    report_state = run(test_cases,cmd,run_test)
    

    output_file = report_dir+"_reports_state.csv"
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["cve_id", "state", "success cnt", "failure cnt"])
        writer.writerows(report_state)

    print(f"Results have been written to {output_file}")

if __name__ == "__main__":
    for report_dir,cmd in reversed(list(semgrep_report_dir_cmd.items())):
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        test(report_dir,cmd)
