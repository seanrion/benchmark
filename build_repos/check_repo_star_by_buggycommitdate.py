import pandas as pd
import requests
from collections import defaultdict
import datetime
import os
from tqdm import tqdm
from urllib.parse import urlparse
import csv

def read_token_from_file(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip() 
    return token


token_file_path = 'github_token'  
ACCESS_TOKEN = read_token_from_file(token_file_path)

print("Token has been read from file.")

GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
CUTOFF_DATE_STR = "2024-08-01"
CUTOFF_DATE = datetime.datetime.strptime(CUTOFF_DATE_STR, '%Y-%m-%d').date()

def parse_repo_info(repo_url):
    """
    解析仓库URL，获取仓库的所有者和仓库名
    """
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    return path_parts[0], path_parts[1]


def get_star_count_history_cumulative(owner, repo, cutoff_date,progress_bar):
    """
    获取截止到指定截止时间点前的累加star数量历史数据，对stargazers按STARRED_AT排序
    如果use_saved_data为True且已存在对应仓库的历史数据文件，则直接读取文件数据返回，否则执行GraphQL查询获取数据
    """
    saved_data_file = f"stars_history/{owner}_{repo}.csv"
    headers = {
        "Authorization": f"bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    query = """
    query($owner: String!, $repo: String!, $cursor: String) {
        repository(owner: $owner, name: $repo) {
            stargazers(first: 100, after: $cursor, orderBy: {field: STARRED_AT, direction: ASC}) {
                edges {
                    starredAt
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
    """
    variables = {
        "owner": owner,
        "repo": repo
    }
    star_count_history = defaultdict(int)
    has_next_page = True
    cursor = None

    while has_next_page:
        variables["cursor"] = cursor
        response = requests.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["data"]["repository"] is None:
                break
            stargazers = data["data"]["repository"]["stargazers"]["edges"]
            if stargazers:
                # 获取每页第一个stargazers的starredAt日期，并计算和cutoff_date的差值
                first_stargazer_date = datetime.datetime.fromisoformat(stargazers[0]["starredAt"][:-1]).date()
                date_diff = (cutoff_date - first_stargazer_date).days
                progress_bar.write(f" 当前获取进度：与截止日期相差 {date_diff} 天")
            should_continue = True
            for stargazer in stargazers:
                starred_at = stargazer["starredAt"]
                date = datetime.datetime.fromisoformat(starred_at[:-1]).date()
                if date <= cutoff_date:
                    star_count_history[date] += 1
                else:
                    should_continue = False
                    break
            if not should_continue:
                break
            page_info = data["data"]["repository"]["stargazers"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            cursor = page_info["endCursor"]
        else:
            break

    min_date = min(star_count_history.keys()) if star_count_history else cutoff_date
    all_dates = [min_date + datetime.timedelta(days=i) for i in range((cutoff_date - min_date).days + 1)]

    cumulative_star_count = defaultdict(int)
    cumulative_sum = 0
    prev_count = 0
    for date in all_dates:
        if date in star_count_history:
            cumulative_sum += star_count_history[date]
            prev_count = cumulative_sum
        cumulative_star_count[date] = prev_count

    history = []
    for date in all_dates:
        history.append({
            "date": date,
            "cumulative_star_count": cumulative_star_count[date]
        })
    return history

def read_saved_history_data(file_path):
    """
    读取已保存的历史数据文
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
            data.append({
                "date": date,
                "cumulative_star_count": int(row['cumulative_star_count'])
            })
    return data


def get_specific_date_data(history, specific_date):
    """
    从历史数据中获取特定时间的数据
    """
    for item in history:
        if item["date"] == specific_date:
            return item
    return None


def save_data_to_csv(history, owner, repo):
    """
    将历史数据保存为CSV文件，保存到stars_history文件夹下
    """
    # 判断stars_history文件夹是否存在，不存在则创建
    if not os.path.exists('stars_history'):
        os.makedirs('stars_history')

    file_name = os.path.join('stars_history', f"{owner}_{repo}.csv")
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'cumulative_star_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in history:
            writer.writerow(item)
    print(f"star 数量历史数据已成功保存至 {file_name} 文件中。")


def process_csv(input_csv_path, output_csv_path):
    """
    处理输入的CSV文件，为每一行仓库数据获取star历史数据并保存文件，同时添加特定时间的star数量到新列后输出到新的CSV文件
    """
    # 读取CSV文件为DataFrame
    df = pd.read_csv(input_csv_path)

    # 检查列名是否存在
    required_columns = ["repo_url", "buggy_commit_time"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV file must contain columns: {', '.join(required_columns)}")

    # 添加新列用于存储特定时间的star数量
    df["stars_at_buggy_commit_time"] = None



    repo_urls_processed = {}  # 用于记录已经处理过的仓库URL及对应的最晚buggy_commit_time
    for index, row in df.iterrows():
        repo_url = row["repo_url"]
        buggy_commit_time_str = str(row["buggy_commit_time"])
        # 提取日期部分，只关心日期
        buggy_commit_time = datetime.datetime.strptime(buggy_commit_time_str[:10], '%Y-%m-%d').date()

        owner, repo = parse_repo_info(repo_url)

        if repo_url not in repo_urls_processed:
            repo_urls_processed[repo_url] = buggy_commit_time
        else:
            # 如果repo_url已存在，更新为较晚的buggy_commit_time
            repo_urls_processed[repo_url] = max(repo_urls_processed[repo_url], buggy_commit_time)



    # 获取数据行数用于进度条显示
    total_rows = len(df)
    progress_bar = tqdm(repo_urls_processed.items(), desc="Processing rows")
    for repo_url, cutoff_date in progress_bar:
        owner, repo = parse_repo_info(repo_url)
        # 假如有这个csv文件
        if os.path.exists(os.path.join('stars_history', f"{owner}_{repo}.csv")):
            star_count_history_cumulative = read_saved_history_data(os.path.join('stars_history', f"{owner}_{repo}.csv"))
        else:
            star_count_history_cumulative = get_star_count_history_cumulative(owner, repo, cutoff_date,progress_bar)
            # 保存历史数据到CSV文件
            save_data_to_csv(star_count_history_cumulative, owner, repo)

        # 获取对应repo_url的所有行索引
        row_indices = df[df["repo_url"] == repo_url].index

        for index in row_indices:
            buggy_commit_time_str = df.at[index, "buggy_commit_time"]
            # 提取日期部分，只关心日期
            buggy_commit_time = datetime.datetime.strptime(buggy_commit_time_str[:10], '%Y-%m-%d').date()
            specific_date_data = get_specific_date_data(star_count_history_cumulative, buggy_commit_time)
            
            if specific_date_data:
                df.at[index, "stars_at_buggy_commit_time"] = specific_date_data["cumulative_star_count"]

    # 保存处理后的DataFrame到新的CSV文件
    df.to_csv(output_csv_path, index=False)
    print("数据处理完成，已保存到新的CSV文件中。")


# 读取的原始CSV文件路径
input_csv_path = "repos_info_with_buggycommit_date.csv"
# 处理后保存的CSV文件路径
output_csv_path = "repos_info_with_stars.csv"

process_csv(input_csv_path, output_csv_path)
