from TestCase import *
from Const import *
from Env import *
import random
from tqdm import tqdm
def run_mirchecker_cmd_get_funclist(test_case:TestCase,env_dict:dict,cwd=None):
    cmd = CARGO_MIRCHECKER_CMD_GET_FUNC_LIST.copy()
    cmd.append(repr(test_case.mirchecker_funclist))
    run_cmd(test_case,cmd,env_dict,cwd=cwd,output_file=test_case.out_file,error_file=test_case.error_file)

def run_mirchecker_cmd_default(test_case:TestCase,env_dict:dict):
    cmd = CARGO_MIRCHECKER_CMD_DEFAULT.copy()
    if test_case.workspace_members_path == []:
        if len(test_case.cmd_excute_path) == 1:
            run_cmd(test_case,cmd,env_dict,output_file=test_case.mirchecker_report,error_file=test_case.error_file,cwd=test_case.cmd_excute_path[0])
        else:
            for i in range(len(test_case.cmd_excute_path)):
                run_cmd(test_case,cmd,env_dict,output_file=test_case.mirchecker_report,error_file=test_case.error_file,cwd=test_case.cmd_excute_path[i])
    else:
        for member_path in test_case.workspace_members_path:
            member_name = member_path.split("/")[-1]
            output_file=test_case.mirchecker_report+"_"+member_name
            run_cmd(test_case,cmd,env_dict,cwd=member_path,output_file=output_file)

def run_mirchecker_cmd(test_case:TestCase,env_dict:dict):
    
    if test_case.workspace_members_path == []:
        if len(test_case.cmd_excute_path) == 1:
            run_mirchecker_cmd_get_funclist(test_case,env_dict,cwd=test_case.cmd_excute_path[0])
            if os.path.exists(test_case.mirchecker_funclist):
                with open(test_case.mirchecker_funclist) as file:
                    lines = [line.strip() for line in file.readlines()]
                    if MIRCHECKER_FUNC_NUM_LIMIT>0:
                        content = lines if len(lines) <= MIRCHECKER_FUNC_NUM_LIMIT else random.sample(lines, MIRCHECKER_FUNC_NUM_LIMIT)
                    else:
                        content = lines
                    progress_bar = tqdm(content, desc="Processing func")
                    for func in progress_bar:
                        cmd = CARGO_MIRCHECKER_CMD.copy()
                        cmd.append(func)
                        run_cmd(test_case,cmd,env_dict,output_file=test_case.mirchecker_report+"_"+func,error_file=test_case.error_file,cwd=test_case.cmd_excute_path[0])
        else:
            for i in range(len(test_case.cmd_excute_path)):
                run_mirchecker_cmd_get_funclist(test_case,env_dict,cwd=test_case.cmd_excute_path[i])
                if os.path.exists(test_case.mirchecker_funclist):
                    with open(test_case.mirchecker_funclist) as file:
                        lines = [line.strip() for line in file.readlines()]
                        if MIRCHECKER_FUNC_NUM_LIMIT>0:
                            content = lines if len(lines) <= MIRCHECKER_FUNC_NUM_LIMIT else random.sample(lines, MIRCHECKER_FUNC_NUM_LIMIT)
                        else:
                            content = lines
                        progress_bar = tqdm(content, desc="Processing func")
                        for func in progress_bar:
                            cmd = CARGO_MIRCHECKER_CMD.copy()
                            cmd.append(func)
                            run_cmd(test_case,cmd,env_dict,output_file=test_case.mirchecker_report+"_"+func,error_file=test_case.error_file,cwd=test_case.cmd_excute_path[i])
    else:
        rootpath = test_case.repo_path
        rootfunclist = test_case.mirchecker_funclist
        for member in test_case.workspace_members_path:
            test_case.mirchecker_funclist = rootfunclist+"_"+member.split("/")[-1]
            run_mirchecker_cmd_get_funclist(test_case,env_dict,cwd=member)
            if os.path.exists(test_case.mirchecker_funclist):
                with open(test_case.mirchecker_funclist) as file:
                    lines = [line.strip() for line in file.readlines()]
                    if MIRCHECKER_FUNC_NUM_LIMIT>0:
                        content = lines if len(lines) <= MIRCHECKER_FUNC_NUM_LIMIT else random.sample(lines, MIRCHECKER_FUNC_NUM_LIMIT)
                    else:
                        content = lines
                    progress_bar = tqdm(content, desc="Processing func")
                    for func in progress_bar:
                        cmd = CARGO_MIRCHECKER_CMD.copy()
                        cmd.append(func)
                        run_cmd(test_case,cmd,env_dict,output_file=test_case.mirchecker_report+"_"+func,error_file=test_case.error_file,cwd=member)

