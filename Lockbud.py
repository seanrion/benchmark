from TestCase import *
from Const import *
from Env import *

def run_lockbud_cmd(test_case:TestCase,env_dict:dict):
    lockbud_report = None
    error_file = os.path.join(test_case.report_path, "stderr")

    if len(test_case.cmd_excute_path) == 1:
        lockbud_report = os.path.join(test_case.report_path, "lockbud_all_report")
        run_cmd(test_case,CARGO_LOCKBUD_CMD_ALL,env_dict,cwd=test_case.cmd_excute_path[0],output_file=lockbud_report,error_file=error_file)
        lockbud_report = os.path.join(test_case.report_path, "lockbud_panic_report")
        run_cmd(test_case,CARGO_LOCKBUD_CMD_PANIC,env_dict,cwd=test_case.cmd_excute_path[0],output_file=lockbud_report,error_file=error_file)

    else:
        for i in range(len(test_case.cmd_excute_path)):
            lockbud_report = os.path.join(test_case.report_path, "lockbud_all_report")
            run_cmd(test_case,CARGO_LOCKBUD_CMD_ALL,env_dict,cwd=test_case.cmd_excute_path[i],output_file=lockbud_report+str(i),error_file=error_file+str(i))
            lockbud_report = os.path.join(test_case.report_path, "lockbud_panic_report")
            run_cmd(test_case,CARGO_LOCKBUD_CMD_PANIC,env_dict,cwd=test_case.cmd_excute_path[i],output_file=lockbud_report+str(i),error_file=error_file+str(i))



