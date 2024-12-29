from TestCase import *
from Const import *
from Env import *

def run_rudra_cmd(test_case:TestCase,env_dict:dict):
    error_file = os.path.join(test_case.report_path, "stderr")
    if test_case.workspace_members_path == []:
        cmd = CARGO_RUDRA_CMD.copy()
        if len(test_case.cmd_excute_path) == 1:
            run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file,cwd=test_case.cmd_excute_path[0])
        else:
            for i in range(len(test_case.cmd_excute_path)):
                run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file,cwd=test_case.cmd_excute_path[i])

                    
    else:
        for member in test_case.workspace_members_path:
            cmd = CARGO_RUDRA_CMD.copy()
            run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file,cwd=member)                        


