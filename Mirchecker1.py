from TestCase import *
from Const import *
from Env import *
import random
def run_mirchecker_cmd_get_funclist(test_case:TestCase,env_dict:dict):
    cmd = CARGO_MIRCHECKER_CMD_GET_FUNC_LIST.copy()
    cmd.append(repr(test_case.mirchecker_funclist))
    run_cmd(test_case,cmd,env_dict)


def run_mirchecker_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = MIRCHECKER1_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = MIRCHECKER1_RUSTC_VERSION
    run_mirchecker_cmd_get_funclist(test_case,env_dict)
    if os.path.exists(test_case.mirchecker_funclist):
        with open(test_case.mirchecker_funclist) as file:
            lines = [line.strip() for line in file.readlines()]
            if MIRCHECKER_FUNC_NUM_LIMIT>0:
                content = lines if len(lines) <= MIRCHECKER_FUNC_NUM_LIMIT else random.sample(lines, MIRCHECKER_FUNC_NUM_LIMIT)
            else:
                content = lines
            for func in content:
                cmd = CARGO_MIRCHECKER_CMD.copy()
                cmd.append(func)
                run_cmd(test_case,cmd,env_dict,output_file=test_case.mirchecker_report+"_"+func)
        

