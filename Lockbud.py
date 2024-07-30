from TestCase import *
from Const import *
from Env import *

def run_lockbud_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = LOCKBUD_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = LOCKBUD_RUSTC_VERSION

    if WASM_TARGET_ENABLE:
        env_dict["CARGO_BUILD_TARGET"] = WASM_TARGET

    if test_case.lockbud_checker == "all":
        run_cmd(test_case,CARGO_LOCKBUD_CMD_ALL,env_dict,test_case.lockbud_report)
    elif test_case.lockbud_checker == "panic":
        run_cmd(test_case,CARGO_LOCKBUD_CMD_PANIC,env_dict,test_case.lockbud_report)
