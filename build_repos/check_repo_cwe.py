import csv
import requests
from bs4 import BeautifulSoup


def get_cwe_text(short_id):
    base_url = f"https://github.com/advisories/{short_id}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # 检查请求是否成功，若不成功则抛出异常
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找data-hovercard-type="cwe"的链接元素
        cwe_link = soup.find('a', {'data-hovercard-type': 'cwe'})
        
        if cwe_link:
            # print(cwe_link.text.strip())
            return cwe_link.text.strip()
        return None
    except requests.RequestException as e:
        print(f"Error fetching data for {short_id}: {e}")
        return None


# 从data.csv文件中读取数据，假设文件中第一行是表头，包含'cve_id'列名，后续行是对应的数据
input_file = 'repos_info_with_stars.csv'
output_file = 'repos_info_with_cwe.csv'
res = []
fieldnames = []
with open(input_file, 'r', encoding='utf-8') as csvfile_in, open(output_file, 'w', encoding='utf-8', newline='') as csvfile_out:
    reader = csv.DictReader(csvfile_in)
    fieldnames = reader.fieldnames
    for row in reader:
        cve_ids = row['cve_id'].split(',')  # 按逗号分割获取多个ID
        cwe_texts = set()
        for cve_id in cve_ids:
            cve_id = cve_id.strip()  # 去除空格
            if cve_id.startswith('GHSA'):
                cwe_text = get_cwe_text(cve_id)
                cwe_texts.add(cwe_text)


        row['CWE'] = ', '.join([text for text in cwe_texts if text])  # 将获取到的CWE文本值用逗号连接，去除None值
        print(row['CWE'])
        res.append(row)
with open(output_file, 'w', encoding='utf-8') as csvfile_in, open(output_file, 'w', encoding='utf-8', newline='') as csvfile_out:
    fieldnames = fieldnames + ['CWE']  # 添加新列名'CWE'到表头
    writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in res:
        writer.writerow(row)