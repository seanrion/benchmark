import os
import csv
import json
from Const import *
import pandas as pd
import openpyxl


unique_bug_types = set()
class SemgrepParser():
    def parse(self, report_path):
        categorized_results = {}
        if os.path.exists(report_path):
            with open(report_path, "r") as file:
                try:
                    data = json.load(file)
                    for result in data["results"]:
                        bug_type = result['check_id']
                        unique_bug_types.add(bug_type)
                        if bug_type not in categorized_results:
                            categorized_results[bug_type] = []

                        parsed_result = {
                            "bug_type": result['check_id'],
                            "locations": [{
                                "file_path": result['path'],
                                "start_line_num": result['start']['line'],
                                "start_col_num": result['start']['col'],
                                "end_line_num": result['end']['line'],
                                "end_col_num": result['end']['col']
                            }]
                        }
                        categorized_results[bug_type].append(parsed_result)
                except Exception as e:
                    print(report_path)
                    print(e)
                    return {}
        return categorized_results

if __name__ == "__main__":
    root_dirs = [
        "./semgrep0.101.1", 
        "./semgrep0.115.0", 
        "./semgrep1.2.1", 
        "./semgrep1.16.0",
        "./semgrep1.30.0",
        "./semgrep1.42.0",
        "./semgrep1.54.3",
        "./semgrep1.67.0",
        "./semgrep1.78.0",
        "./semgrep1.90.0",
        "./semgrep1.101.0",
        ]
    datas = {}
    parser = SemgrepParser()
    for root_dir in root_dirs:
        results = []
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)
            if os.path.isdir(subdir_path):
                stdout_file = os.path.join(subdir_path, "semgrep_report.json")
                row = dict()
                row["cve_id"] = subdir
                row["details"] = parser.parse(stdout_file)
                results.append(row)

        result_csv = []
        for result in results:
            if result["details"] == {}:
                result_csv.append({"cve_id":result["cve_id"], "bug_type":"total", "num":0})
            else:
                total_num = 0
                for bug_type, itemlist in result["details"].items():
                    result_csv.append({"cve_id":result["cve_id"], "bug_type":bug_type, "num":len(itemlist)})
                    total_num += len(itemlist)
                result_csv.append({"cve_id":result["cve_id"], "bug_type":"total", "num":total_num})

        
        df = pd.DataFrame(result_csv)
        pivot_df = df.pivot_table(index='cve_id', columns='bug_type', values='num', fill_value=0)
        pivot_df = pivot_df.reset_index()
        output_csv = root_dir+"_results.csv"
        pivot_df.to_csv(output_csv, index=False)
        print(f"Results have been written to {output_csv}")

        output_json = root_dir+"_results.json"
        with open(output_json, "w", newline='') as jsonfile:
            json.dump(results, jsonfile)
        print(f"Results have been written to {output_json}")
        print(unique_bug_types)

        datas[root_dir] = result_csv
    
    bug_type_data = {}
    for root_dir, results in datas.items():
        for item in results:
            bug_type = item['bug_type']
            if bug_type not in bug_type_data:
                bug_type_data[bug_type] = {}
            if item['cve_id'] not in bug_type_data[bug_type]:
                bug_type_data[bug_type][item['cve_id']] = {}
            bug_type_data[bug_type][item['cve_id']][root_dir] = item['num']

    excel_file = "./semgrep_regression_csv/all_bug_types.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for bug_type, cve_data in bug_type_data.items():
            df = pd.DataFrame.from_dict(cve_data, orient='index')
            for root_dir in root_dirs:
                if root_dir not in df.columns:
                    df[root_dir] = 0
                    
            df = df[root_dirs]
            df = df.fillna(0)
            sheet_name = bug_type[:31] 
            df.to_excel(writer, sheet_name=sheet_name)

        print(f"All results have been written to {excel_file}")