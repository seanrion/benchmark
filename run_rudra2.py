#!/usr/bin/env python3
import os
import os.path
from Const import *
from TestCase import *
import Rudra2
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import threading
def run_test(test_case:TestCase):
    Rudra2.run_rudra_cmd(test_case)



if __name__ == "__main__":
    cve_dirs = [f.path for f in os.scandir(CVE_REPO_DIR) if f.is_dir()]

    # cve_dirs = list(filter(
    #     lambda t: t is not None,
    #     map(lambda path: path if ("['GHSA-rxr4-x558-x7hw', 'RUSTSEC-2018-0003']" in path) else None, cve_dirs)))


    cve_repos = [os.path.join(d,"buggy") for d in cve_dirs]
    cve_repos = [[f.path for f in os.scandir(d) if f.is_dir()][0] for d in cve_repos]
    rudra2_report_dir = [d.replace(CVE_REPO_DIR,RUDRA2_REPORT_DIR) for d in cve_dirs]
    for d in rudra2_report_dir:
        if not os.path.exists(d):
            os.makedirs(d)
    test_cases = filter(
        lambda t: t is not None,
        map(lambda path,report_path: TestCase.create_test_case(path,report_path), cve_repos,rudra2_report_dir)
    )

    progress_bar = tqdm(total=len(rudra2_report_dir), desc="Processing test cases")

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

