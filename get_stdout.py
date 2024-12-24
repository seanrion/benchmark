import os
import csv
from Const import *

root_dir = RUDRA2_REPORT_DIR

# 创建一个列表用于存储结果
results = []

# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "stdout")
        if os.path.exists(stdout_file):
            # 读取stdout文件并检查是否包含"failed to parse manifest"字符串
            with open(stdout_file, "r") as file:
                content = file.read()
                if "failed to parse the `edition` key" in content:
                    results.append([subdir, "error", "编译器版本过低", "failed to parse the `edition` key"])
                elif "cannot be built because it requires rustc" in content:
                    results.append([subdir, "error", "编译器版本过低", "cannot be built because it requires rustc"])
                elif "failed to load manifest for workspace member" in content:
                    results.append([subdir, "error", "仓库配置", "failed to load manifest for workspace member"])
                elif "failed to parse manifest" in content:
                    results.append([subdir, "error", "编译器版本过低", "failed to parse manifest"])
                elif "use of unstable library feature" in content:
                    results.append([subdir, "error", "编译器版本过低", "use of unstable library feature"])
                elif "could not find `Cargo.toml`" in content:
                    results.append([subdir, "error", "找不到cargo.toml文件", "could not find `Cargo.toml`"])
                elif "failed to select a version for the requirement" in content:
                    results.append([subdir, "error", "依赖版本", "failed to select a version for the requirement"])
                elif "This seems to be a workspace, which is not supported by cargo-rudra" in content:
                    results.append([subdir, "error", "rudra不支持workspace", "This seems to be a workspace, which is not supported by cargo-rudra"])
                elif "error[E0512]: cannot transmute between types of different sizes, or dependently-sized types" in content:
                    results.append([subdir, "error", "不同大小的类型之间进行transmute", "error[E0512]: cannot transmute between types of different sizes, or dependently-sized types"])
                else:
                    results.append([subdir, None, None, None])

# 将结果写入CSV文件
output_file = "report_results.csv"
with open(output_file, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["cve_id",	"rudra1",	"kind",	"detail"])
    writer.writerows(results)

print(f"Results have been written to {output_file}")
