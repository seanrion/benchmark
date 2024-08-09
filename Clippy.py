from TestCase import *
from Const import *
from Env import *

def run_clippy_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = CLIPPY_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = CLIPPY_RUSTC_VERSION
    if test_case.report_format == "json":
        run_cmd(test_case,CARGO_CLIPPY_CMD_WITH_JSON_REPORT,env_dict,output_file=test_case.clippy_report,error_file=test_case.error_file)
    else:
        run_cmd(test_case,CARGO_CLIPPY_CMD,env_dict,output_file=test_case.clippy_report,error_file=test_case.error_file)
