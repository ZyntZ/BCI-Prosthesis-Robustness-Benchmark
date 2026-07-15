# Statistical reporting pack for `PhysionetMI_dev10`

Generated from existing subject-summary CSV files only; no simulated or additional benchmark observations are used.

## Methods audit
| check | value | status |
| --- | --- | --- |
| n_rows_subject_summary | 70 | info |
| n_subjects | 10 | info |
| n_conditions | 7 | info |
| duplicate_subject_condition_rows | 0 | pass |
| missing_roc_auc | 0 | pass |
| out_of_range_0_1_roc_auc | 0 | pass |
| missing_balanced_accuracy | 0 | pass |
| out_of_range_0_1_balanced_accuracy | 0 | pass |
| missing_brier_score | 70 | review |
| out_of_range_0_1_brier_score | 0 | pass |
| missing_ece | 70 | review |
| out_of_range_0_1_ece | 0 | pass |
| min_subjects_per_condition | 10 | pass |
| max_subjects_per_condition | 10 | info |

## Paired stressor effects vs clean all-channel baseline
| condition | metric | metric_role | n_subjects | clean_mean | condition_mean | mean_delta_condition_minus_clean | delta_ci_low | delta_ci_high | median_delta_condition_minus_clean | cohens_dz | t_p_value_bh_fdr | wilcoxon_p_value_bh_fdr | sign_test_p_value_bh_fdr | shapiro_p_value_delta | pct_worse_than_clean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | balanced_accuracy | secondary | 10 | 0.612 | 0.5307 | -0.0813 | -0.2033 | 0.0407 | -0.0315 | -0.4767 | 0.1992 | 0.3305 | 1 | 0.07218 | 0.5 |
| channel_dropout_0.2 | balanced_accuracy | secondary | 10 | 0.612 | 0.5119 | -0.1002 | -0.2375 | 0.03721 | -0.0505 | -0.5216 | 0.1992 | 0.3099 | 1 | 0.07915 | 0.5 |
| channel_dropout_0.3 | balanced_accuracy | secondary | 10 | 0.612 | 0.5154 | -0.0966 | -0.2356 | 0.04236 | -0.036 | -0.4973 | 0.1992 | 0.3516 | 1 | 0.1182 | 0.5 |
| channel_dropout_0.5 | balanced_accuracy | secondary | 10 | 0.612 | 0.5036 | -0.1085 | -0.2508 | 0.03394 | -0.05275 | -0.5448 | 0.1992 | 0.3099 | 1 | 0.1194 | 0.5 |
| reduced_montage_motor_core | balanced_accuracy | secondary | 10 | 0.612 | 0.6355 | 0.0235 | -0.1028 | 0.1498 | 0.045 | 0.1331 | 0.6837 | 0.4766 | 1 | 0.6274 | 0.4 |
| reduced_montage_motor_extended | balanced_accuracy | secondary | 10 | 0.612 | 0.687 | 0.075 | 0.01775 | 0.1323 | 0.0525 | 0.9371 | 0.08258 | 0.05859 | 0.3281 | 0.4278 | 0.1 |
| channel_dropout_0.1 | roc_auc | primary | 10 | 0.643 | 0.5844 | -0.0586 | -0.1184 | 0.001241 | -0.0525 | -0.7005 | 0.1296 | 0.1781 | 0.8705 | 0.8536 | 0.6 |
| channel_dropout_0.2 | roc_auc | primary | 10 | 0.643 | 0.5353 | -0.1076 | -0.196 | -0.01927 | -0.08475 | -0.8713 | 0.08258 | 0.05859 | 0.3281 | 0.5012 | 0.8 |
| channel_dropout_0.3 | roc_auc | primary | 10 | 0.643 | 0.5432 | -0.0998 | -0.1829 | -0.01667 | -0.08525 | -0.8588 | 0.08258 | 0.05859 | 0.3281 | 0.1498 | 0.8 |
| channel_dropout_0.5 | roc_auc | primary | 10 | 0.643 | 0.5147 | -0.1283 | -0.2388 | -0.01779 | -0.0965 | -0.8305 | 0.08258 | 0.05859 | 0.3281 | 0.1047 | 0.8 |
| reduced_montage_motor_core | roc_auc | primary | 10 | 0.643 | 0.689 | 0.046 | -0.07837 | 0.1704 | 0.065 | 0.2646 | 0.463 | 0.3013 | 0.825 | 0.05633 | 0.3 |
| reduced_montage_motor_extended | roc_auc | primary | 10 | 0.643 | 0.713 | 0.07 | -0.01184 | 0.1518 | 0.03 | 0.6119 | 0.17 | 0.3013 | 0.8705 | 0.169 | 0.3 |

## Sensitivity summary
| condition | metric | available | role | n_subjects | mean_delta_condition_minus_clean | pct_worse_than_clean | ttest_fdr | wilcoxon_fdr | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | roc_auc | True | primary | 10.0 | -0.0586 | 0.6 | 0.1296 | 0.1781 | primary |
| channel_dropout_0.1 | balanced_accuracy | True | secondary | 10.0 | -0.0813 | 0.5 | 0.1992 | 0.3305 | secondary |
| channel_dropout_0.1 | brier_score | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.1 | ece | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.2 | roc_auc | True | primary | 10.0 | -0.1076 | 0.8 | 0.08258 | 0.05859 | primary |
| channel_dropout_0.2 | balanced_accuracy | True | secondary | 10.0 | -0.1002 | 0.5 | 0.1992 | 0.3099 | secondary |
| channel_dropout_0.2 | brier_score | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.2 | ece | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.3 | roc_auc | True | primary | 10.0 | -0.0998 | 0.8 | 0.08258 | 0.05859 | primary |
| channel_dropout_0.3 | balanced_accuracy | True | secondary | 10.0 | -0.0966 | 0.5 | 0.1992 | 0.3516 | secondary |
| channel_dropout_0.3 | brier_score | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.3 | ece | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.5 | roc_auc | True | primary | 10.0 | -0.1283 | 0.8 | 0.08258 | 0.05859 | primary |
| channel_dropout_0.5 | balanced_accuracy | True | secondary | 10.0 | -0.1085 | 0.5 | 0.1992 | 0.3099 | secondary |
| channel_dropout_0.5 | brier_score | False | calibration |  |  |  |  |  |  |
| channel_dropout_0.5 | ece | False | calibration |  |  |  |  |  |  |
| reduced_montage_motor_core | roc_auc | True | primary | 10.0 | 0.046 | 0.3 | 0.463 | 0.3013 | primary |
| reduced_montage_motor_core | balanced_accuracy | True | secondary | 10.0 | 0.0235 | 0.4 | 0.6837 | 0.4766 | secondary |
| reduced_montage_motor_core | brier_score | False | calibration |  |  |  |  |  |  |
| reduced_montage_motor_core | ece | False | calibration |  |  |  |  |  |  |
| reduced_montage_motor_extended | roc_auc | True | primary | 10.0 | 0.07 | 0.3 | 0.17 | 0.3013 | primary |
| reduced_montage_motor_extended | balanced_accuracy | True | secondary | 10.0 | 0.075 | 0.1 | 0.08258 | 0.05859 | secondary |
| reduced_montage_motor_extended | brier_score | False | calibration |  |  |  |  |  |  |
| reduced_montage_motor_extended | ece | False | calibration |  |  |  |  |  |  |

## Channel-dropout slopes
| dataset | pipeline | metric | n_subjects | mean_slope_per_10pct_dropout | slope_ci_low | slope_ci_high | slope_sd | t_statistic_vs_zero | t_p_value_vs_zero | shapiro_p_value_slope | n_harmful_slope | pct_harmful_slope | t_p_value_vs_zero_bh_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PhysionetMotorImagery | csp_lda | balanced_accuracy | 10 | -0.01779 | -0.04061 | 0.005021 | 0.03189 | -1.764 | 0.1115 | 0.1274 | 5 | 0.5 | 0.1115 |
| PhysionetMotorImagery | csp_lda | roc_auc | 10 | -0.02346 | -0.04319 | -0.003729 | 0.02758 | -2.69 | 0.02481 | 0.07795 | 9 | 0.9 | 0.04962 |

## Overclaim-risk flags
| flag | triggered | detail |
| --- | --- | --- |
| low_subject_count | True | n_subjects=10; population-level claims should be cautious below 20 subjects. |
| development_subset_prefix | True | Prefix contains 'dev'; treat as development output, not final population estimate. |
| missing_calibration_metrics | True | Missing optional calibration metrics: brier_score, ece |
| cross_session_absent | True | Cross-session stressor absent. |
| skipped_subject_log_present | False | Found 0 failed-subject log files matching prefix. |
| uneven_or_low_paired_n | False | minimum paired n=10; total subject n=10. |

## Statistical notes
- Paired effects are computed within subject against the clean all-channel baseline.
- Confidence intervals for mean paired deltas and slopes use Student t intervals.
- Median-delta intervals use a distribution-free sign-test/order-statistic interval.
- Normality of paired deltas/slopes is screened with Shapiro-Wilk where sample size permits.
- Wilcoxon signed-rank and sign tests are reported as sensitivity checks for paired deltas.
- Benjamini-Hochberg false discovery rate correction is applied to paired t-test, Wilcoxon, and sign-test p-values.