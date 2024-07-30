import os
import subprocess
from Const import *
import resource
class TestCase:

    def __init__(self, path, report_path, report_format, lockbud_checker="all"):
        # self.rudra_config = rudra_config
        self.path = path
        self.report_path = report_path
        self.rudra_report = os.path.join(report_path, "rudra_report")
        self.semgrep_report = os.path.join(report_path, "semgrep_report.json")
        self.report_format = report_format
        if report_format=="json":
            self.clippy_report = os.path.join(report_path, "clippy_report.json")
        else:
            self.clippy_report = os.path.join(report_path, "clippy_report")
        self.lockbud_checker = lockbud_checker
        if lockbud_checker=="all":
            self.lockbud_report = os.path.join(report_path, "lockbud_all_report")
        elif lockbud_checker=="panic":
            self.lockbud_report = os.path.join(report_path, "lockbud_panic_report")
        else:
            raise Exception("Wrong lockbud_checker!")
        self.success = False
        self.run_message = None
        self.mirchecker_funclist = os.path.join(report_path, "funclist.txt")
        self.mirchecker_report = os.path.join(report_path, "mirchecker_report")
    
    @classmethod
    def create_test_case(cls, path, report_path, report_format=None, lockbud_checker="all"):
        # rudra_config_path = os.path.join(path,"rudra_config.toml")
        # if not os.path.exists(rudra_config_path):
        #     rudra_config = None
        # else:
        #     with open(rudra_config_path) as f:
        #         rudra_config = tomlkit.load(f)
        # return cls(path,report_path,rudra_config,report_format)
        return cls(os.path.abspath(path),os.path.abspath(report_path),report_format, lockbud_checker)


    def is_success(self):
        return self.success is True

    def __repr__(self):
        return "TestCase(%s)" % self.path

    def __str__(self):
        if self.is_success():
            return "\u001b[32;1mSUCCESS       \u001b[0m  {}".format(self.path, self.run_message)
        else:
            return "\u001b[31;1mFAIL          \u001b[0m  {}\n\n{}".format(self.path, self.run_message)
        


def set_memory_limit(limit_bytes):
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))

def run_cmd(test_case:TestCase,cmd:list,env:dict,output_file=None):
    print(cmd)
    try:
        process = subprocess.Popen(
            args = ' '.join(CARGO_CLEAN_CMD),
            cwd=test_case.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            shell=True,
        )
        process.wait()
        process = subprocess.Popen(
            args = ' '.join(cmd),
            preexec_fn=lambda: set_memory_limit(MEMORY_LIMIT_BYTES),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=test_case.path,
            shell=True,
        )
        
        stdout,stderr = process.communicate(timeout=TIMEOUT if TIMEOUT_ENABLE else None)
        returncode = process.poll()
        if not output_file==None:
            with open(output_file,'w') as f:
                f.write(stdout.decode('utf-8'))
        if returncode==0:
            test_case.success = True
        else:
            test_case.success = False
        test_case.run_message = stdout.decode('utf-8')
        print(str(test_case))
    except subprocess.TimeoutExpired as e:
        process.kill()
        process.wait()
        test_case.success = False
        
        test_case.run_message = "TIMEOUT after "+str(TIMEOUT)+" seconds"
        if not output_file==None:
            with open(output_file+".timeout",'w') as f:
                pass
        print(str(test_case))
    # except subprocess.CalledProcessError as e:
    #     test_case.success = True
    #     test_case.run_message = "CalledProcessError"