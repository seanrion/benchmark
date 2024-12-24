from TestCase import *
from Const import *
from Env import *

def run_rudra_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["RUDRA_REPORT_PATH"] = os.path.abspath(os.path.join(test_case.report_path, "rudra_report"))
    env_dict["LD_LIBRARY_PATH"] = RUDRA1_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = RUDRA1_RUSTC_VERSION
    env_dict["RUSTFLAGS"] = RUDRA1_RUSTFLAGS
    run_cmd(test_case,CARGO_RUDRA_CMD,env_dict,output_file=test_case.out_file,error_file=test_case.error_file)
    return test_case

def run_rudra_cmd(test_case:TestCase,env_dict:dict):
    
    if test_case.workspace_members_path == []:
        cmd = CARGO_RUDRA_CMD.copy()
        run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file)
                    
    else:
        for member in test_case.workspace_members_path:
            cmd = CARGO_RUDRA_CMD.copy()
            run_cmd(test_case,cmd,env_dict,output_file=test_case.out_file,error_file=test_case.error_file,cwd=member)                        


