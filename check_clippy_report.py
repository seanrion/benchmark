import os
import csv
from Const import *

root_dir = CLIPPY_REPORT_DIR
Clippy_warning = [
'wrong_transmute',
'while_immutable_condition',
'while_float',
'unwrap_used',
'unwrap_in_result',
'unsound_collection_transmute',
'unreachable',
'uninit_vec',
'uninit_assumed_init',
'uninhabited_references',
'unimplemented',
'unconditional_recursion',
'unchecked_duration_subtraction',
'transmuting_null',
'transmute_undefined_repr',
'transmute_num_to_bytes',
'transmute_null_to_fn',
'transmute_int_to_non_zero',
'transmute_int_to_float',
'transmute_int_to_char',
'transmute_float_to_int',
'transmute_float_to_int',
'transmute_bytes_to_str',
'todo',
'swap_ptr_to_ref',
'suboptimal_flops',
'significant_drop_in_scrutinee',
'reversed_empty_ranges',
'recursive_format_impl',
'permissions_set_readonly_false',
'path_ends_with_ext',
'panicking_unwrap',
'panic_in_result_fn',
'panic',
'overflow_check_conditional',
'out_of_bounds_indexing',
'option_env_unwrap',
'not_unsafe_ptr_arg_deref',
'non_send_fields_in_send_ty',
'non_octal_unix_permissions',
'modulo_one',
'missing_transmute_annotations',
'missing_assert_message',
'mem_replace_with_uninit',
'mem_forget',
'maybe_infinite_iter',
'match_on_vec_items',
'manual_strip',
'manual_slice_size_calculation',
'macro_metavars_in_unsafe',
'lines_filter_map_ok',
'join_absolute_paths',
'iterator_step_by_zero',
'iter_next_loop',
'invisible_characters',
'invalid_regex',
'invalid_null_ptr_usage',
'infinite_loop',
'infinite_iter',
'imprecise_flops',
'if_let_mutex',
'get_last_with_len',
'float_equality_without_abs',
'float_cmp_const',
'fallible_impl_from',
'excessive_precision',
'enum_clike_unportable_variant',
'empty_loop',
'eager_transmute',
'diverging_sub_expression',
'default_union_representation',
'cast_slice_different_sizes',
'cast_ptr_alignment',
'cast_precision_loss ',
'cast_abs_to_unsigned',
'case_sensitive_file_extension_comparisons',
'bad_bit_mask',
'arithmetic_side_effects',
'arc_with_non_send_sync',
'approx_constant',
]
# 创建一个列表用于存储结果
results = []
# error_types = set()
# 遍历所有二级文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        stdout_file = os.path.join(subdir_path, "clippy_report")
        if os.path.exists(stdout_file):
            # 读取stdout文件并检查是否包含"failed to parse manifest"字符串
            with open(stdout_file, "r") as file:
                lines = file.readlines()
            row = dict.fromkeys(Clippy_warning, 0)
            row["cve_id"] = subdir
            for line in lines:

                if '= help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html' in line:
                    error_info = line.split('#')[-1].strip()
                    for type in Clippy_warning:
                        if type == error_info:
                            row[type] += 1
            results.append(row)
                


# 如果需要查看具体的信息类型，可以打印集合
# print("不同的信息类型包括：")
# for error_type in error_types:
#     print(error_type+'\n')
output_file = "Clippy_results.csv"
# with open(output_file, "w", newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=["cve_id","error: [Prusti: internal error]"])
#     writer.writeheader()
#     writer.writerows(results)

with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["cve_id"]+Clippy_warning)
    writer.writeheader()
    writer.writerows(results)

# print(f"Results have been written to {output_file}")
