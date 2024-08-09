from TestCase import *
from Const import *
from Env import *

def run_prusti_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = PRUSTI_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = PRUSTI_RUSTC_VERSION
    env_dict["PRUSTI_VERIFY_ERRORS_AS_WARNINGS"] = "true"


    run_cmd(test_case,CARGO_PRUSTI_CMD,env_dict,output_file=test_case.prusti_report,error_file=test_case.error_file)
