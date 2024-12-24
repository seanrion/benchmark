import pandas as pd
import requests
import datetime
from tqdm import tqdm
df = pd.read_csv('repos_info_with_published_date.csv')

token = "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"

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




