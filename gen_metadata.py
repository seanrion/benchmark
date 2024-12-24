#!/usr/bin/env python3
import os
import os.path
from Const import *
from TestCase import *
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import csv
import threading
import re
from urllib.parse import unquote
cve_ids = [
"RUSTSEC-2020-0028, GHSA-8q2v-67v7-6vc6",
"RUSTSEC-2020-0048, GHSA-v3j6-xf77-8r9c",
"GHSA-6x52-88cq-55q5",
"GHSA-pf3p-x6qj-6j7q, RUSTSEC-2020-0081",
"RUSTSEC-2020-0059, GHSA-rh4w-94hh-9943",
"GHSA-67hm-27mx-9cg7",
"GHSA-p24j-h477-76q3, RUSTSEC-2021-0106",
"RUSTSEC-2021-0071",
"RUSTSEC-2020-0009, GHSA-c9h5-hf8r-m97x",
"RUSTSEC-2021-0124, GHSA-fg7r-2g4j-5cgr",
"GHSA-6mv3-wm7j-h4w5",
"GHSA-44mr-8vmm-wjhg, RUSTSEC-2022-0076",
"GHSA-2hvr-h6gw-qrxp",
"GHSA-8v4j-7jgf-5rg9, RUSTSEC-2022-0082",
"GHSA-8mj7-wxmc-f424, RUSTSEC-2022-0028",
"GHSA-6r8p-hpg7-825g",
"GHSA-4mq4-7rw3-vm5j",
"GHSA-r64r-5h43-26qv",
"GHSA-w3vp-jw9m-f9pm",
"RUSTSEC-2023-0064, GHSA-rrjw-j4m2-mf34",
"GHSA-vx24-x4mv-vwr5",
"RUSTSEC-2024-0336, GHSA-6g7w-8wpp-frhj",
"GHSA-3qx3-6hxr-j2ch",
"GHSA-52xf-5p2m-9wrv",
"GHSA-67fv-9r7g-432h",
]
specific_path = [
    {
        "cve_id":"RUSTSEC-2020-0009, GHSA-c9h5-hf8r-m97x",
        "cmd_excute_paths":[
            "rust/flatbuffers",
            "rust/flexbuffers",
        ],
    },
    {
        "cve_id":"GHSA-52xf-5p2m-9wrv",
        "cmd_excute_paths":[
            "bindings/rust"
        ],
    }
]
import subprocess
import toml

def get_workspace_members(cargo_toml_path):
    # 读取Cargo.toml文件
    with open(cargo_toml_path, 'r') as file:
        cargo_toml = toml.load(file)
    
    # 提取workspace成员
    workspace = cargo_toml.get('workspace', {})
    members = workspace.get('members', [])

    return members
# def list_cargo_workspaces(directory):
#     ans = []
#     try:
#         result = subprocess.check_output(["cargo", "metadata", "--format-version", "1"], cwd = directory)
#         metadata = json.loads(result.decode("utf - 8"))
#         if "workspace_members" in metadata:
#             for member in metadata["workspace_members"]:
#                 match = re.search(r"path\+file://(.*?)#", member)
#                 if match:
#                     path = match.group(1)
#                     ans.append(unquote(path))
#     except subprocess.CalledProcessError:
#         pass
#     except json.JSONDecodeError:
#         pass
#     return ans



if __name__ == "__main__":

    cve_dirs = [f.path for f in os.scandir(CVE_REPO_DIR) if f.is_dir()
                 and f.name in cve_ids
                 ]

    cve_repo_paths = [os.path.join(d,"buggy") for d in cve_dirs]
    cve_repo_paths = [[f.path for f in os.scandir(d) if f.is_dir()] for d in cve_repo_paths]
    cve_repo_paths = list(filter(
        lambda t: t is not None,
        map(lambda path: None if not path else path[0], cve_repo_paths)))


    headers = ["cve_id", "cve_repo_path", "cmd_excute_path","workspace_members_path"]
    output_file = 'metadata.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        row = dict()
        for i in range(len(cve_ids)):
            row["cve_id"] = cve_ids[i]
            repo_path = next((d for d in cve_repo_paths if cve_ids[i] in d), None)
            row["cve_repo_path"] = repo_path
            target_item = next((d for d in specific_path if d.get("cve_id") == cve_ids[i]), None)
            if target_item:
                relative_paths = target_item.get("cmd_excute_paths")
                absolute_paths = [os.path.join(repo_path,path) for path in relative_paths]
                row["cmd_excute_path"] = absolute_paths
            else:
                row["cmd_excute_path"] = [repo_path]
            row["workspace_members_path"] = []
            for path in row["cmd_excute_path"]:
                workspace_members = get_workspace_members(os.path.join(path,"Cargo.toml"))
                workspace_members_path = [os.path.join(path,member) for member in workspace_members]
                row["workspace_members_path"].extend(workspace_members_path)
            
            writer.writerow(row)

    print(f"Metadata have been written to {output_file}")