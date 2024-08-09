#!/usr/bin/env python3
import os
import os.path
from Const import *
import csv
import difflib

def read_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def compare_files(file1_lines, file2_lines):
    if file1_lines is None or file2_lines is None:
        return None
    if file1_lines == file2_lines:
        return 1.00
    similarity_ratio = round(difflib.SequenceMatcher(None, file1_lines, file2_lines).ratio(),2)
    return similarity_ratio

def compare_reports(base_dirs):
    results = []
    sub_folders = set(os.listdir(base_dirs[0]))
    for base_dir in base_dirs[1:]:
        sub_folders &= set(os.listdir(base_dir))

    for sub_folder in sub_folders:
        sub_paths = [os.path.join(base_dir, sub_folder) for base_dir in base_dirs]
        file_names =  set(os.listdir(sub_paths[0])+os.listdir(sub_paths[1])+os.listdir(sub_paths[2]))
        file_names = list(filter(
            lambda t: t is not None,
            map(lambda file_name: file_name if file_name.startswith("rudra_report") else None, file_names)
        ))
        # print(file_names)
        for file_name in file_names:
            if not file_name.startswith("rudra_report"):
                continue
            file_paths = [os.path.join(sub_path, file_name) for sub_path in sub_paths]
            files_exist = tuple(os.path.exists(file_path) for file_path in file_paths)
            file_contents = [read_file(file_path) for file_path in file_paths]
            similarities = (
                compare_files(file_contents[0], file_contents[1]),
                compare_files(file_contents[0], file_contents[2]),
                compare_files(file_contents[1], file_contents[2])
            )
            results.append((sub_folder, file_name, files_exist, similarities))
    return results

def save_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['cve', 'file_name', 'is_exist (rudra1, rudra2, rudra3)', 'similarily (rudra1 vs rudra2, rudra1 vs rudra3, rudra2 vs rudra3)'])
        for sub_folder, file_name, files_exist, similarities in results:
            csv_writer.writerow([sub_folder, file_name, files_exist, similarities])

if __name__ == "__main__":
    base_dirs = [RUDRA1_REPORT_DIR, RUDRA2_REPORT_DIR, RUDRA3_REPORT_DIR]
    results = compare_reports(base_dirs)
    save_to_csv(results, 'rudra_report_comparison_results.csv')