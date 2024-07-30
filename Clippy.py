from TestCase import *
from Const import *
from Env import *

def run_clippy_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    env_dict["LD_LIBRARY_PATH"] = CLIPPY_RUSTC_LD_LIBRARY_PATH
    env_dict["RUSTUP_TOOLCHAIN"] = CLIPPY_RUSTC_VERSION
    if test_case.report_format == "json":
        run_cmd(test_case,CARGO_CLIPPY_CMD_WITH_JSON_REPORT,env_dict,test_case.clippy_report)
    else:
        run_cmd(test_case,CARGO_CLIPPY_CMD,env_dict,test_case.clippy_report)
