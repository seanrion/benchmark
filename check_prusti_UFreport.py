import os
import csv
from Const import *

root_dir = PRUSTI_REPORT_DIR
unsupported_features = [
"iterators are not fully supported yet",
"casts PtrToPtr are not supported",
"unions are not supported",
"determining the region of array indexing is not supported",
"mixed dereferencing and array indexing projections are not supported",
"two-phase borrows are not supported",
"Slicing is only supported for arrays/slices currently",
"type is not supported",
"mutably slicing is not fully supported yet",
"the encoding of pledges does not supporte this kind of reborrowing",
"unsupported type Alias",
"unsupported constant type",
"only calls to closures are supported",
"higher-ranked lifetimes and types are not supported",
"unsupported creation of shallow borrows (implicitly created when lowering matches)",
"slicing with RangeInclusive (e.g. [x..=y]) currently not supported",
"unsizing a",
"variadic functions are not supported",
"casts IntToFloat are not supported",
"array indexing is not supported in arbitrary operand positions. Try refactoring your code to have only an array access on the right-hand side of assignments using temporary variables",
"unsupported type Generator",
"determining the region of a dereferentiation is not supported",
"please use a local variable as argument for function",
"copy operation for an unsupported type Binder",
"raw pointers are not supported",
"unsupported type to extract lifetimes",
"unsupported type Binder",
"Non-slice LHS type",
"unsupported cast from type",
"raw addresses of expressions and casts from references to raw pointers are not supported",
"unsupported statement kind",
"casts FloatToInt are not supported",
"unsupported constant value",
"access to reference-typed fields is not supported",
"unsupported const kind",
"references to thread-local storage are not supported",
"casts FloatToFloat are not supported",
"the creation of loans in this loop is not supported",
"experimental and disabled by default",
"cast statements that create loans are not supported"
]
# 创建一个列表用于存储结果
results = []

# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "prusti_report")
        if os.path.exists(stdout_file):
            # 读取stdout文件并检查是否包含"failed to parse manifest"字符串
            with open(stdout_file, "r") as file:
                lines = file.readlines()
            row = dict.fromkeys(unsupported_features, 0)
            row["cve_id"] = subdir
            for line in lines:

                if line.startswith('error: [Prusti: unsupported feature]'):
                    error_info = line[len('error: [Prusti: unsupported feature]'):].strip()
                    for type in unsupported_features:
                        if type in error_info:
                            row[type] += 1
            results.append(row)
                


# 如果需要查看具体的信息类型，可以打印集合
# print("不同的信息类型包括：")
# for error_type in error_types:
#     print(error_type+'\n')

output_file = "prusti_UF_results.csv"
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["cve_id"]+unsupported_features)
    writer.writeheader()
    writer.writerows(results)


# print(f"Results have been written to {output_file}")
