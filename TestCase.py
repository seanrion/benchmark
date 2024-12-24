import os
import subprocess
from Const import *
import resource
import signal
class TestCase:

    def __init__(self, repo_path, cmd_excute_path, report_path, report_format, workspace_members_path=None):
        # self.rudra_config = rudra_config
        self.success_cnt = 0
        self.failure_cnt = 0
        self.repo_path = repo_path
        self.cmd_excute_path = cmd_excute_path
        self.report_path = report_path
        self.out_file = os.path.join(report_path, "stdout")
        self.error_file = os.path.join(report_path, "stderr")
        self.rudra_report = os.path.join(report_path, "rudra_report")
        self.semgrep_report = os.path.join(report_path, "semgrep_report.json")
        self.report_format = report_format
        if report_format=="json":
            self.clippy_report = os.path.join(report_path, "clippy_report.json")
        else:
            self.clippy_report = os.path.join(report_path, "clippy_report")

        self.prusti_report = os.path.join(report_path, "prusti_report")
        self.mirai_report = os.path.join(report_path, "mirai_report")

        self.success = False
        self.run_message = None
        self.mirchecker_funclist = os.path.join(report_path, "funclist")
        self.mirchecker_report = os.path.join(report_path, "mirchecker_report")
        self.workspace_members_path = workspace_members_path
    
    @classmethod
    def create_test_case(cls, repo_path, cmd_excute_path, report_path, report_format=None, workspace_members_path=None):
        # rudra_config_path = os.path.join(path,"rudra_config.toml")
        # if not os.path.exists(rudra_config_path):
        #     rudra_config = None
        # else:
        #     with open(rudra_config_path) as f:
        #         rudra_config = tomlkit.load(f)
        # return cls(path,report_path,rudra_config,report_format)
        return cls(os.path.abspath(repo_path),cmd_excute_path,os.path.abspath(report_path),report_format, workspace_members_path)


    def is_success(self):
        return self.success is True

    def __repr__(self):
        return "TestCase(%s)" % self.report_path

    def __str__(self):
        if self.is_success():
            # return "\u001b[32;1mSUCCESS       \u001b[0m  {}".format(self.report_path, self.run_message)
            return "\u001b[32;1mSUCCESS       \u001b[0m  "
        else:
            # return "\u001b[31;1mFAIL          \u001b[0m  {}".format(self.report_path, self.run_message)
            return "\u001b[31;1mFAIL          \u001b[0m  "
        



def set_memory_limit(limit_bytes):
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))

def kill_command(p):
    os.killpg(os.getpgid(p.pid),signal.SIGTERM)



def run_cmd(test_case:TestCase,cmd:list,env:dict,cwd=None,output_file=None,error_file=None):
    # print(cmd)
    # print(' '.join(cmd))

    try:
        process = subprocess.Popen(
            args = ' '.join(CARGO_CLEAN_CMD),
            cwd=cwd if cwd else test_case.repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            shell=True,
            start_new_session=True,
        )
        process.wait()

        process = subprocess.Popen(
            args = ' '.join(cmd),
            preexec_fn=lambda: set_memory_limit(MEMORY_LIMIT_BYTES),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=cwd if cwd else test_case.repo_path,
            shell=True,
            start_new_session=True,
        )
        # print(cmd)
        # print(env)
        stdout,stderr = process.communicate(timeout=TIMEOUT if TIMEOUT_ENABLE else None)


        returncode = process.poll()

        if not output_file==None:
            with open(output_file,'w') as f:
                f.write(stdout.decode('utf-8'))
        if not error_file==None and not stderr==None:
            with open(error_file,'w') as f:
                f.write(stderr.decode('utf-8'))

        if returncode==0:
            test_case.success = True
            test_case.success_cnt += 1
        else:
            test_case.success = False
            test_case.failure_cnt += 1

        print(str(test_case)+"  ",output_file)

    except subprocess.TimeoutExpired as e:

        kill_command(process)
        test_case.success = False
        test_case.failure_cnt += 1
        test_case.run_message = "TIMEOUT after "+str(TIMEOUT)+" seconds"
        if not output_file==None:
            with open(output_file,'w') as f:
                f.write(test_case.run_message)
                if not e.stdout==None:
                    f.write(e.stdout.decode('utf-8'))
        if not error_file==None:
            with open(error_file,'w') as f:
                f.write(test_case.run_message)
                if not e.stderr==None:
                    f.write(e.stderr.decode('utf-8'))
        print(str(test_case)+"  ",output_file)
    except subprocess.CalledProcessError as e:

        kill_command(process)
        test_case.success = False
        test_case.failure_cnt += 1
        test_case.run_message = "CalledProcessError"
        if not output_file==None:
            with open(output_file,'w') as f:
                f.write(test_case.run_message)
                if not e.stdout==None:
                    f.write(e.stdout.decode('utf-8'))
        if not error_file==None:
            with open(error_file,'w') as f:
                f.write(test_case.run_message)
                if not e.stderr==None:
                    f.write(e.stderr.decode('utf-8'))
        print(str(test_case)+"  ",output_file)
