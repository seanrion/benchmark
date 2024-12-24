import TestCase
import threading
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from Const import *
import os
success_cnt = 0
failure_cnt = 0

def run(test_cases,run_test):
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
    return report_state