from TestCase import *
from Const import *
from Env import *

def run_mirai_cmd(test_case:TestCase,env_dict:dict):
    mirai_report = os.path.join(test_case.report_path, "mirai_report")
    error_file = os.path.join(test_case.report_path, "stderr")

    if len(test_case.cmd_excute_path) == 1:
        run_cmd(test_case,CARGO_MIRAI_CMD,env_dict,cwd=test_case.cmd_excute_path[0],output_file=mirai_report,error_file=error_file)
    else:
        for i in range(len(test_case.cmd_excute_path)):
            run_cmd(test_case,CARGO_MIRAI_CMD,env_dict,cwd=test_case.cmd_excute_path[i],output_file=mirai_report+str(i),error_file=error_file+str(i))


