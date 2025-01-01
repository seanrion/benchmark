import os
import pandas as pd

# 假设 cve_repos 是一个包含子目录路径的列表
cve_repos = os.listdir('./../cve_repos')

# # 读取 repos_info.csv 文件
repos_info_path = './bakrepos_info.csv' 
repos_info_df = pd.read_csv(repos_info_path)

cve_repos = set(cve_repos)

repos_in_csv = set(repos_info_df['cve_id'])

# # 找出 cve_repos 中不在 repos_info.csv 中的子目录
missing_repos = [repo for repo in cve_repos if repo not in repos_in_csv]

# # 打印结果
print("Subdirectories in cve_repos not in repos_info.csv:")
for repo in missing_repos:
    print(repo)

empty_buggy_dirs = []

for repo in cve_repos:
    buggy_dir = os.path.join("./../cve_repos", repo, "buggy")
    # print(buggy_dir)
    if os.path.isdir(buggy_dir) and not os.listdir(buggy_dir):
        empty_buggy_dirs.append(repo)

# 打印结果
print("Subdirectories with empty 'buggy' folders:")
for repo in empty_buggy_dirs:
    print(repo)