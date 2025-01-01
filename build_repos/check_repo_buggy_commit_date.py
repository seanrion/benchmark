import pandas as pd
import requests
import datetime
from tqdm import tqdm
df = pd.read_csv('repos_info_with_published_date.csv')

def read_token_from_file(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip() 
    return token


token_file_path = 'github_token'  
token = read_token_from_file(token_file_path)

print("Token has been read from file.")

def get_commit_time(repo_url, commit_sha):
    """
    通过GitHub API获取指定仓库中某个commit的提交时间
    """
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits/{commit_sha}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_data = response.json()
        author_date = commit_data["commit"]["author"]["date"]
        # print(author_date)
        return datetime.datetime.fromisoformat(author_date.rstrip('Z'))
    return None
    
commit_times = []
with tqdm(total=len(df), desc="处理进度") as pbar:
    for index, row in df.iterrows():
        commit_time = get_commit_time(row['repo_url'], row['buggy_commit'])
        commit_times.append(commit_time)
        pbar.update(1)

df['buggy_commit_time'] = commit_times
df.to_csv('./repos_info_with_buggycommit_date.csv', index=False)
print("Data merged and saved successfully!")




