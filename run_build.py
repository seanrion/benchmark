#!/usr/bin/env python3
import os
import os.path
from Const import *
from Env import *
from TestCase import *
import Prusti
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import threading
import csv
def run_test(test_case:TestCase):
    env_dict = dict(os.environ)

    env_dict["LD_LIBRARY_PATH"] = RUDRA3_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = RUDRA3_RUSTC_VERSION
    env_dict["PRUSTI_VERIFY_ERRORS_AS_WARNINGS"] = "true"


    run_cmd(test_case,CARGO_BUILD_CMD,env_dict,output_file=test_case.out_file,error_file=test_case.error_file)
    return test_case



if __name__ == "__main__":
    cve_dirs = [f.path for f in os.scandir(CVE_REPO_DIR) if f.is_dir()]

    cve_dirs = list(filter(
        lambda t: t is not None,
        map(lambda path: path if ("GHSA-44mr-8vmm-wjhg, RUSTSEC-2022-0076" in path) else None, cve_dirs)))


    cve_repos = [os.path.join(d,"buggy") for d in cve_dirs]
    cve_repos = [[f.path for f in os.scandir(d) if f.is_dir()] for d in cve_repos]
    cve_repos = list(filter(
        lambda t: t is not None,
        map(lambda path: None if not path else path[0], cve_repos)))



    
    build_out_dir = [os.path.dirname(os.path.dirname(d.replace(CVE_REPO_DIR,BUILD_OUT_DIR))) for d in cve_repos]

    for d in build_out_dir:
        if not os.path.exists(d):
            os.makedirs(d)
    test_cases = list(filter(
        lambda t: t is not None,
        map(lambda path,report_path: TestCase.create_test_case(path,report_path), cve_repos,build_out_dir)
    ))

    success_cnt = 0
    failure_cnt = 0
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
                pool.apply_async(run_test, (test_case,), 
                                 callback=update_progress_bar
                                 ))
        
        for result in results:
            result.get()

    print("success cnt:"+str(success_cnt))
    print("failure cnt:"+str(failure_cnt))
    with open("./build.result",'w') as f:
        f.write("success cnt:"+str(success_cnt)+"\n")
        f.write("failure cnt:"+str(failure_cnt))

    output_file = "build.csv"
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["cve_id", "state", "success cnt", "failure cnt"])
        writer.writerows(report_state)