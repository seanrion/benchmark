from TestCase import *
from Const import *
from Env import *

def run_prusti_cmd(test_case:TestCase,env_dict:dict):
    prusti_report = os.path.join(test_case.report_path, "prusti_report")
    error_file = os.path.join(test_case.report_path, "stderr")

    if len(test_case.cmd_excute_path) == 1:
        run_cmd(test_case,CARGO_PRUSTI_CMD,env_dict,cwd=test_case.cmd_excute_path[0],output_file=prusti_report,error_file=error_file)
    else:
        for i in range(len(test_case.cmd_excute_path)):
            run_cmd(test_case,CARGO_PRUSTI_CMD,env_dict,cwd=test_case.cmd_excute_path[i],output_file=prusti_report+str(i),error_file=error_file+str(i))
