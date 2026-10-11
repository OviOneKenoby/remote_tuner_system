# Isolated compiler experiment matrix

| Experiment | Exit | Seconds | Observed process-tree RSS bytes |
| --- | --- | --- | --- |
| confirmed_identical_copy_1 | 0 | 0.6023 | 54091776 |
| confirmed_identical_copy_2 | 0 | 0.5484 | 54296576 |
| confirmed_identical_copy_3 | 0 | 0.5548 | 53989376 |
| confirmed_installed_1 | 0 | 0.586 | 54362112 |
| confirmed_installed_2 | 0 | 0.5631 | 53968896 |
| confirmed_installed_3 | 0 | 0.5651 | 53915648 |
| confirmed_official_fresh_1 | 0 | 0.5664 | 54509568 |
| confirmed_official_fresh_2 | 0 | 0.5471 | 54407168 |
| confirmed_official_fresh_3 | 0 | 0.5523 | 54390784 |
| fixed_response_stability_1 | 1 | 0.3468 | 51433472 |
| fixed_response_stability_2 | 1 | 0.3673 | 49553408 |
| fixed_response_stability_3 | 1 | 0.342 | 49856512 |
| output_presence_control_1 | 1 | 0.3591 | 50946048 |
| output_presence_control_2 | 1 | 0.3513 | 51453952 |
| output_presence_control_3 | 0 | 0.5581 | 54116352 |
| output_presence_control_4 | 1 | 0.3559 | 50946048 |
| preprocess_hash_recheck | 0 | 0.2632 | 26411008 |
| compiler_version | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| compiler_verbose | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| compiler_target | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| compiler_dumpversion | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| smoke_default | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| smoke_target_ABI | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| smoke_emit_assembly | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| smoke_assemble | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| smoke_objdump | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| smoke_assembled_objdump | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocess_valid | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| dependency_only | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| syntax_original | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| exact_original_direct | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_original_1 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_original_2 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_original_3 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| short_path_same_TEMP | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| short_path_short_TEMP | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| byte_identical_copy_1 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| byte_identical_copy_2 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| byte_identical_copy_3 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| official_fresh_1 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| official_fresh_2 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| official_fresh_3 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| original_exact_repeat_1 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| original_exact_repeat_2 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| original_exact_repeat_3 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_actual_SCons_ENV_1 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_actual_SCons_ENV_2 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_actual_SCons_ENV_3 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_actual_SCons_ENV_4 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_actual_SCons_ENV_5 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| preprocessed_actual_SCons_ENV_6 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| original_response_actual_SCons_ENV_1 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| original_response_actual_SCons_ENV_2 | 0 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |
| original_response_actual_SCons_ENV_3 | 1 | UNKNOWN; aggregate capture gap | UNKNOWN; capture gap |

Original full build1 -j8 and fresh build2 -j1: exit1 each (BUILD_ATTEMPTS.json); no complete artifacts. Original SCons single-object target and external-observer-config single-object target: exit0 each, not full builds. Full raw command/log/environment retained only locally. See EXACT_COMPILER_COMMAND_SANITIZED.json and EXPERIMENT_MATRIX.json for retained commands and safe error lines.

10ms polling RSS is a lower bound, not guaranteed true peak. Earlier aggregate collector reset lost some duration/RSS metadata; raw logs/hash/exit summaries remain. Observer/preprocessing helper failures before valid compiler invocation are disclosed in COLLECTION_NOTES.json and are not compiler ICE experiments. Optimization variants NOT RUN: frozen .i never crashed, so deterministic-input precondition not met. Two new complete clean builds NOT RUN: exact original source command still intermittently fails.
