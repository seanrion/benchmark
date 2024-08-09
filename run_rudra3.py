#!/usr/bin/env python3
import os
import os.path
from Const import *
from TestCase import *
import Rudra3
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import threading
def run_test(test_case:TestCase):
    Rudra3.run_rudra_cmd(test_case)
    return test_case


if __name__ == "__main__":
    cve_dirs = [f.path for f in os.scandir(CVE_REPO_DIR) if f.is_dir()]

    # cve_dirs = list(filter(
    #     lambda t: t is not None,
    #     map(lambda path: path if ("RUSTSEC-2020-0094, GHSA-39xg-8p43-h76x" in path) else None, cve_dirs)))


    cve_repos = [os.path.join(d,"buggy") for d in cve_dirs]
    cve_repos = [[f.path for f in os.scandir(d) if f.is_dir()] for d in cve_repos]
    cve_repos = list(filter(
        lambda t: t is not None,
        map(lambda path: None if not path else path[0], cve_repos)))
    



    rudra3_report_dir = [os.path.dirname(os.path.dirname(d.replace(CVE_REPO_DIR,RUDRA3_REPORT_DIR))) for d in cve_repos]
    for d in rudra3_report_dir:
        if not os.path.exists(d):
            os.makedirs(d)
    test_cases = list(filter(
        lambda t: t is not None,
        map(lambda path,report_path: TestCase.create_test_case(path,report_path), cve_repos,rudra3_report_dir)
    ))

    success_cnt = 0
    failure_cnt = 0
    progress_bar = tqdm(total=len(test_cases), desc="Processing test cases")
    def update_progress_bar(test_case:TestCase):
        with threading.Lock():
            global success_cnt,failure_cnt
            success_cnt += test_case.success_cnt
            failure_cnt += test_case.failure_cnt
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
    with open("./rudra3.result",'w') as f:
        f.write("success cnt:"+str(success_cnt)+"\n")
        f.write("failure cnt:"+str(failure_cnt))
