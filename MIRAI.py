from TestCase import *
from Const import *
from Env import *

def run_mirai_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = MIRAI_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = MIRAI_RUSTC_VERSION

    run_cmd(test_case,CARGO_MIRAI_CMD,env_dict,output_file=test_case.mirai_report,error_file=test_case.error_file)
