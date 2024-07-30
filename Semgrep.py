from TestCase import *
from Const import *
from Env import *
import tempfile
import shutil
def run_semgrep_cmd(test_case:TestCase):
    env_dict = dict(os.environ)
    cmd = SEMGREP_CMD.copy()
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        cmd.append("--json-output="+os.path.abspath(temp_file.name))
    run_cmd(test_case,cmd,env_dict)
    with open(temp_file.name, 'rb') as temp_file:
        with open(test_case.semgrep_report, 'wb') as destination_file:
            shutil.copyfileobj(temp_file, destination_file)