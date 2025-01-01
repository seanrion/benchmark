import pandas as pd
from pydriller import Git
import sys
import os
import logging
import subprocess
from tqdm import tqdm

sys.path.append('../utils')
from utils import get_full_project_name, is_git_repo

dest = "../repos_mirror"
cve_repos = "../cve_repos"

def git_checkout(repo,commit):
    cmd = [
    "git",
    "checkout",
    commit,
    "-f"
    ]
    output = subprocess.run(
        args = cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        cwd = repo,
        # shell = True,
    )
    if not output.returncode == 0:
        print(output.stdout)
    return output.returncode
        

def git_clone(repo_dest_path, work_tree_path):
    if not os.path.exists(work_tree_path):
        os.makedirs(work_tree_path)
    cmd = [
        "git",
        "clone",
        repo_dest_path,
        work_tree_path,
        ]
    output = subprocess.run(
        args = cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        # shell = True,
    )
    if output.returncode==0:
        print(work_tree_path)



def main():
    success_list = []
    fail_list = []
    success_cnt = 0
    fail_cnt = 0
    success_cnt_fix = 0
    fail_cnt_fix = 0

    df_fixes = pd.read_csv('../data_extraction/fix_commits2.csv')
    # df_fixes = pd.read_csv('../data_extraction/fail_commits.csv')

    df_fixes.drop_duplicates(subset =['hash', 'repo_url'], keep = 'first', inplace = True)
    df_fixes['cve_id'] = df_fixes['cve_id'].str.replace(r"[\[\]']", '', regex=True)
    df_fixes = df_fixes.groupby('cve_id').agg({
        'hash': lambda x: ','.join(x),
        'repo_url': 'first'
    }).reset_index()
    df_fixes['buggy_commit'] = None
    df_fixes.rename(columns={
    'hash': 'fixed_commit',
    }, inplace=True)



    for index, row in tqdm(df_fixes.iterrows(),total=df_fixes.shape[0]):
        repo_url = row["repo_url"]
        cve_id = row["cve_id"]
        fixed_commits = row["fixed_commit"].split(",")

        # if repo_url != "https://github.com/paritytech/frontier":
        #     continue
        # outpath = compiler_result+package+"/"+cve_id
        # outpath_fix = compiler_result+package+"/"+cve_id+"_fix"
        full_project_name = get_full_project_name(repo_url)
        repo_dest_path = os.path.join(dest, full_project_name)
        print(repo_dest_path)
        cve_repo_path = os.path.join(cve_repos,cve_id)
        if os.path.exists(repo_dest_path):
            if is_git_repo(repo_dest_path):
                try:
                    
                    repo = Git(repo_dest_path)
                    fixed_commits = [repo.get_commit(hash) for hash in fixed_commits]
                    fixed_commit_hash = [commit.hash for commit in fixed_commits]
                    min_commit = min(fixed_commits, key=lambda commit: commit.committer_date)
                    buggy_commit_hash = min_commit.parents[0]
                    df_fixes.at[index, 'buggy_commit'] = buggy_commit_hash
                    df_fixes.at[index, 'fixed_commit'] = fixed_commit_hash

                    buggy_repo = os.path.join(cve_repo_path,"buggy",buggy_commit_hash)
                    git_clone(repo_dest_path, buggy_repo)
                    
                    if git_checkout(buggy_repo,buggy_commit_hash)==0:
                        success_cnt += 1
                    else:
                        os.system(f"rm -rf {buggy_repo}")
                        fail_cnt += 1
                        fail_list.append(buggy_repo)
                    
                    for hash in fixed_commit_hash:
                        fixed_repo = os.path.join(cve_repo_path,"fixed",hash)
                        git_clone(repo_dest_path, fixed_repo)
                        if git_checkout(fixed_repo,hash)==0:
                            success_list.append(cve_id)
                            success_cnt_fix += 1
                        else:
                            os.system(f"rm -rf {fixed_repo}")
                            fail_cnt_fix += 1
                            fail_list.append(fixed_repo)

                except Exception as e:
                    logging.warning('Problem while fetching the commits!')
                    fail_cnt += 1
                    fail_list.append(buggy_repo)
                    print(e)
                    pass
            
            else:
                logging.warning('Repos not cloned!')

    print("success: ",success_cnt)
    print("fail: ",fail_cnt)
    print("success_fix: ",success_cnt_fix)
    print("fail_fix: ",fail_cnt_fix)
    
    with open("fail", "w") as f:
        for l in fail_list:
            f.write(l+"\n")
    with open("success", "w") as f:
        for l in success_list:
            f.write(l+"\n")

    df_fixes.to_csv('./repos_info.csv', index=False)
    print("Data merged and saved successfully!")


if __name__ == '__main__':
    main()




