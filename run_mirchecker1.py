#!/usr/bin/env python3
import os
import os.path
from Const import *
from TestCase import *
import Mirchecker1
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import threading
def run_test(test_case:TestCase):
    Mirchecker1.run_mirchecker_cmd(test_case)
    return test_case



if __name__ == "__main__":
    cve_dirs = [f.path for f in os.scandir(CVE_REPO_DIR) if f.is_dir()]
    # cve_dirs = list(filter(
    #     lambda t: t is not None,
    #     map(lambda path: path if ("RUSTSEC-2018-0004, GHSA-8c6g-4xc5-w96c" in path) else None, cve_dirs)))


    cve_repos = [os.path.join(d,"buggy") for d in cve_dirs]
    cve_repos = [[f.path for f in os.scandir(d) if f.is_dir()][0] for d in cve_repos]
    mirchecker1_report_dir = [d.replace(CVE_REPO_DIR,MIRCHECKER1_REPORT_DIR) for d in cve_dirs]
    for d in mirchecker1_report_dir:
        if not os.path.exists(d):
            os.makedirs(d)
    test_cases = filter(
        lambda t: t is not None,
        map(lambda path,report_path: TestCase.create_test_case(path,report_path), cve_repos, mirchecker1_report_dir)
    )
    
    progress_bar = tqdm(total=len(mirchecker1_report_dir), desc="Processing test cases")
    def update_progress_bar(result):
        with threading.Lock():
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

