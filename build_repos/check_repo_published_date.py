import pandas as pd
import requests
import datetime
import tqdm
df1 = pd.read_csv('repos_info.csv')


df2 = pd.read_csv('output.csv')

def extract_first_part(cve_id):
    if isinstance(cve_id, str) and ',' in cve_id:
        return cve_id.split(',')[0].strip()
    return cve_id

# 对第一个表格的cve_id列应用函数进行提取操作
df1['short_id'] = df1['cve_id'].apply(extract_first_part)

# 用于存储匹配到的published列的数据
published_data = []

# 遍历第一个表格处理后的cve_id列数据
for cve_id in df1['short_id']:
    match = df2[df2['id'].str.contains(cve_id)]
    if not match.empty:
        published_data.append(match['published'].iloc[0])
    else:
        published_data.append(None)

# 将结果添加到第一个表格中作为新列（可选操作，可根据需求调整）
df1['published_date'] = published_data
# 将published列的数据类型转换为datetime类型（如果还不是的话）
df1['published_date'] = pd.to_datetime(df1['published_date'])

# 提取日期部分，只精确到日，会将时间部分丢弃，格式变为 'YYYY-MM-DD'
df1['published_date'] = df1['published_date'].dt.strftime('%Y-%m-%d')


# 查看处理后的第一个表格
df1.to_csv('./repos_info_with_published_date.csv', index=False)
print("Data merged and saved successfully!")