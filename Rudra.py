from TestCase import *
from Const import *
from Env import *

def run_rudra_cmd(test_case:TestCase,env_dict:dict):
    if test_case.workspace_members_path == []:
        cmd = CARGO_RUDRA_CMD.copy()
        run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file)
                    
    else:
        for member in test_case.workspace_members_path:
            cmd = CARGO_RUDRA_CMD.copy()
            run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file,cwd=member)                        


