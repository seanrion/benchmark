MEMORY_LIMIT_BYTES = 128 * 1024 * 1024 * 1024
THREAD_NUM = 4
TIMEOUT_ENABLE = True
TIMEOUT = 30*60
CSV_DATA_PATH = "./fix_commits2.csv"
CVE_REPO_DIR = "./cve_repos"
REPO_DIFF_DATA_DIR = "./diff_data"
RUDRA1_REPORT_DIR = "./rudra1_report"
RUDRA2_REPORT_DIR = "./rudra2_report"
RUDRA3_REPORT_DIR = "./rudra3_report"
CLIPPY_REPORT_DIR = "./clippy_report"
SEMGREP_REPORT_DIR = "./semgrep_report"
LOCKBUD_REPORT_DIR = "./lockbud_report"
MIRCHECKER1_REPORT_DIR = "./mirchecker1_report"
PRUSTI_REPORT_DIR = "./prusti_report"
MIRAI_REPORT_DIR = "./mirai_report"
MIRCHECKER_FUNC_NUM_LIMIT = -1

CARGO_CLEAN_CMD = [
    "cargo",
    "clean",
]

CARGO_MIRAI_CMD = [
    "cargo",
    "mirai",
]

CARGO_PRUSTI_CMD = [
    "cargo",
    "prusti",
]
CARGO_MIRCHECKER_CMD_GET_FUNC_LIST = [
    "cargo",
    "mir-checker",
    "--",
    "--show_entries",
    "--output_file",
]
CARGO_MIRCHECKER_CMD = [
    "cargo",
    "mir-checker",
    # "--message-format=json",
    "--",
    "--entry",
    ]


CARGO_RUDRA_CMD = [
    "cargo",
    "rudra",
    "--",
    "-Zrudra-enable-unsafe-destructor",
    "--crate-type",
    "lib"
]
CARGO_LOCKBUD_CMD_ALL = [
    "cargo",
    "lockbud",
    "-k",
    "all",
]
CARGO_LOCKBUD_CMD_PANIC = [
    "cargo",
    "lockbud",
    "-k",
    "panic",
]
SEMGREP_CMD = [
    "semgrep", 
    "scan",
    "--config",
    "p/rust",
    "--pro",
    "--json",
    # "--json-output=out.json"
]

CARGO_CLIPPY_CMD = [
"cargo", 
"clippy" ,
"--",
"-A clippy::all",
"-W clippy::fallible_impl_from",
"-W clippy::missing_assert_message",
"-W clippy::panic",
"-W clippy::panic_in_result_fn",
"-W clippy::todo",
"-W clippy::unimplemented",
"-W clippy::unreachable",
"-W clippy::unwrap_in_result",
"-W clippy::unwrap_used",
"-W clippy::diverging_sub_expression",
"-W clippy::iterator_step_by_zero",
"-W clippy::option_env_unwrap",
"-W clippy::panicking_unwrap",
"-W clippy::match_on_vec_items",
"-W clippy::get_last_with_len",
"-W clippy::manual_strip",
"-W clippy::swap_ptr_to_ref",
"-W clippy::out_of_bounds_indexing",
"-W clippy::reversed_empty_ranges",
"-W clippy::arithmetic_side_effects",
"-W clippy::unchecked_duration_subtraction",
"-W clippy::manual_slice_size_calculation",
"-W clippy::overflow_check_conditional",
"-W clippy::cast_abs_to_unsigned",
"-W clippy::modulo_one",
"-W clippy::transmute_undefined_repr",
"-W clippy::default_union_representation",
"-W clippy::cast_ptr_alignment",
"-W clippy::transmute_bytes_to_str",
"-W clippy::transmute_float_to_int",
"-W clippy::transmute_float_to_int",
"-W clippy::transmute_int_to_char",
"-W clippy::transmute_int_to_float",
"-W clippy::transmute_int_to_non_zero",
"-W clippy::transmute_num_to_bytes",
"-W clippy::missing_transmute_annotations",
"-W clippy::cast_slice_different_sizes",
"-W clippy::eager_transmute",
"-W clippy::transmute_null_to_fn",
"-W clippy::transmuting_null",
"-W clippy::unsound_collection_transmute",
"-W clippy::wrong_transmute ",
"-W clippy::cast_precision_loss ",
"-W clippy::suboptimal_flops",
"-W clippy::imprecise_flops",
"-W clippy::float_cmp_const",
"-W clippy::while_float",
"-W clippy::float_equality_without_abs",
"-W clippy::excessive_precision",
"-W clippy::enum_clike_unportable_variant",
"-W clippy::approx_constant",
"-W clippy::significant_drop_in_scrutinee",
"-W clippy::if_let_mutex",
"-W clippy::maybe_infinite_iter",
"-W clippy::infinite_loop",
"-W clippy::empty_loop",
"-W clippy::lines_filter_map_ok",
"-W clippy::infinite_iter",
"-W clippy::while_immutable_condition",
"-W clippy::uninhabited_references",
"-W clippy::invalid_null_ptr_usage",
"-W clippy::invalid_regex",
"-W clippy::invisible_characters",
"-W clippy::bad_bit_mask",
"-W clippy::iter_next_loop",
"-W clippy::mem_replace_with_uninit",
"-W clippy::uninit_assumed_init",
"-W clippy::uninit_vec",
"-W clippy::permissions_set_readonly_false",
"-W clippy::non_octal_unix_permissions",
"-W clippy::macro_metavars_in_unsafe",
"-W clippy::not_unsafe_ptr_arg_deref",
"-W clippy::unconditional_recursion",
"-W clippy::recursive_format_impl",
"-W clippy::non_send_fields_in_send_ty",
"-W clippy::arc_with_non_send_sync",
"-W clippy::path_ends_with_ext",
"-W clippy::case_sensitive_file_extension_comparisons",
"-W clippy::mem_forget",
"-W clippy::join_absolute_paths",
]

CARGO_CLIPPY_CMD_WITH_JSON_REPORT = [
"cargo", 
"clippy" ,
"--message-format",
"json",
"--",
"-A clippy::all",
"-W clippy::fallible_impl_from",
"-W clippy::missing_assert_message",
"-W clippy::panic",
"-W clippy::panic_in_result_fn",
"-W clippy::todo",
"-W clippy::unimplemented",
"-W clippy::unreachable",
"-W clippy::unwrap_in_result",
"-W clippy::unwrap_used",
"-W clippy::diverging_sub_expression",
"-W clippy::iterator_step_by_zero",
"-W clippy::option_env_unwrap",
"-W clippy::panicking_unwrap",
"-W clippy::match_on_vec_items",
"-W clippy::get_last_with_len",
"-W clippy::manual_strip",
"-W clippy::swap_ptr_to_ref",
"-W clippy::out_of_bounds_indexing",
"-W clippy::reversed_empty_ranges",
"-W clippy::arithmetic_side_effects",
"-W clippy::unchecked_duration_subtraction",
"-W clippy::manual_slice_size_calculation",
"-W clippy::overflow_check_conditional",
"-W clippy::cast_abs_to_unsigned",
"-W clippy::modulo_one",
"-W clippy::transmute_undefined_repr",
"-W clippy::default_union_representation",
"-W clippy::cast_ptr_alignment",
"-W clippy::transmute_bytes_to_str",
"-W clippy::transmute_float_to_int",
"-W clippy::transmute_float_to_int",
"-W clippy::transmute_int_to_char",
"-W clippy::transmute_int_to_float",
"-W clippy::transmute_int_to_non_zero",
"-W clippy::transmute_num_to_bytes",
"-W clippy::missing_transmute_annotations",
"-W clippy::cast_slice_different_sizes",
"-W clippy::eager_transmute",
"-W clippy::transmute_null_to_fn",
"-W clippy::transmuting_null",
"-W clippy::unsound_collection_transmute",
"-W clippy::wrong_transmute ",
"-W clippy::cast_precision_loss ",
"-W clippy::suboptimal_flops",
"-W clippy::imprecise_flops",
"-W clippy::float_cmp_const",
"-W clippy::while_float",
"-W clippy::float_equality_without_abs",
"-W clippy::excessive_precision",
"-W clippy::enum_clike_unportable_variant",
"-W clippy::approx_constant",
"-W clippy::significant_drop_in_scrutinee",
"-W clippy::if_let_mutex",
"-W clippy::maybe_infinite_iter",
"-W clippy::infinite_loop",
"-W clippy::empty_loop",
"-W clippy::lines_filter_map_ok",
"-W clippy::infinite_iter",
"-W clippy::while_immutable_condition",
"-W clippy::uninhabited_references",
"-W clippy::invalid_null_ptr_usage",
"-W clippy::invalid_regex",
"-W clippy::invisible_characters",
"-W clippy::bad_bit_mask",
"-W clippy::iter_next_loop",
"-W clippy::mem_replace_with_uninit",
"-W clippy::uninit_assumed_init",
"-W clippy::uninit_vec",
"-W clippy::permissions_set_readonly_false",
"-W clippy::non_octal_unix_permissions",
"-W clippy::macro_metavars_in_unsafe",
"-W clippy::not_unsafe_ptr_arg_deref",
"-W clippy::unconditional_recursion",
"-W clippy::recursive_format_impl",
"-W clippy::non_send_fields_in_send_ty",
"-W clippy::arc_with_non_send_sync",
"-W clippy::path_ends_with_ext",
"-W clippy::case_sensitive_file_extension_comparisons",
"-W clippy::mem_forget",
"-W clippy::join_absolute_paths",
]










RUDRA_TEST = [
'./rudra_tests/panic_safety/order_safe',
'./rudra_tests/panic_safety/insertion_sort',
'./rudra_tests/panic_safety/order_safe_if',
'./rudra_tests/panic_safety/vec_push_all',
'./rudra_tests/panic_safety/pointer_to_ref',
'./rudra_tests/panic_safety/order_unsafe_transmute',
'./rudra_tests/panic_safety/order_unsafe',
'./rudra_tests/panic_safety/order_safe_loop',
'./rudra_tests/panic_safety/order_unsafe_loop',

'./rudra_tests/send_sync/wild_sync',
'./rudra_tests/send_sync/okay_where',
'./rudra_tests/send_sync/wild_send',
'./rudra_tests/send_sync/sync_over_send_fp',
'./rudra_tests/send_sync/okay_ptr_like',
'./rudra_tests/send_sync/okay_channel',
'./rudra_tests/send_sync/no_generic',
'./rudra_tests/send_sync/okay_imm',
'./rudra_tests/send_sync/wild_channel',
'./rudra_tests/send_sync/wild_phantom',
'./rudra_tests/send_sync/okay_phantom',
'./rudra_tests/send_sync/okay_transitive',
'./rudra_tests/send_sync/okay_negative',

'./rudra_tests/unsafe_destructor/fp1',
'./rudra_tests/unsafe_destructor/normal1',
'./rudra_tests/unsafe_destructor/copy_filter',
'./rudra_tests/unsafe_destructor/ffi',
'./rudra_tests/unsafe_destructor/normal2'
]
