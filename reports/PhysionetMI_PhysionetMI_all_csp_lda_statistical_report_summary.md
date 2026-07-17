# Statistical reporting pack for `PhysionetMI_PhysionetMI_all_csp_lda`

Generated from existing subject-summary CSV files only; no simulated or additional benchmark observations are used.

## Methods audit
| check | value | status |
| --- | --- | --- |
| n_rows_subject_summary | 1090 | info |
| n_subjects | 109 | info |
| n_conditions | 10 | info |
| duplicate_subject_condition_rows | 0 | pass |
| missing_roc_auc | 0 | pass |
| out_of_range_0_1_roc_auc | 0 | pass |
| missing_balanced_accuracy | 0 | pass |
| out_of_range_0_1_balanced_accuracy | 0 | pass |
| missing_brier_score | 0 | pass |
| out_of_range_0_1_brier_score | 0 | pass |
| missing_ece | 0 | pass |
| out_of_range_0_1_ece | 0 | pass |
| min_subjects_per_condition | 109 | pass |
| max_subjects_per_condition | 109 | info |

## Paired stressor effects vs clean all-channel baseline
| condition | metric | metric_role | n_subjects | clean_mean | condition_mean | mean_delta_condition_minus_clean | delta_ci_low | delta_ci_high | median_delta_condition_minus_clean | cohens_dz | t_p_value_bh_fdr | wilcoxon_p_value_bh_fdr | sign_test_p_value_bh_fdr | shapiro_p_value_delta | pct_worse_than_clean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5251 | -0.09421 | -0.1163 | -0.07211 | -0.0855 | -0.8093 | 2.468e-13 | 1.371e-11 | 1.727e-09 | 0.3059 | 0.789 |
| channel_dropout_0.2 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5122 | -0.107 | -0.1319 | -0.08216 | -0.0885 | -0.8168 | 1.811e-13 | 1.19e-11 | 1.824e-08 | 0.0848 | 0.7706 |
| channel_dropout_0.3 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5074 | -0.1118 | -0.1374 | -0.0862 | -0.0915 | -0.8287 | 1.001e-13 | 1.046e-11 | 5.735e-09 | 0.06725 | 0.7798 |
| channel_dropout_0.5 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5047 | -0.1146 | -0.1408 | -0.08839 | -0.097 | -0.8304 | 9.679e-14 | 8.77e-12 | 2.711e-08 | 0.04821 | 0.7615 |
| reduced_montage_motor_core | balanced_accuracy | secondary | 109 | 0.6193 | 0.612 | -0.007217 | -0.03173 | 0.0173 | -0.005 | -0.0559 | 0.5767 | 0.6206 | 0.9234 | 0.9559 | 0.5046 |
| reduced_montage_motor_extended | balanced_accuracy | secondary | 109 | 0.6193 | 0.6307 | 0.01139 | -0.01036 | 0.03314 | 0.015 | 0.09942 | 0.329 | 0.2717 | 0.186 | 0.8585 | 0.422 |
| region_dropout_left_motor_strip_0.140625 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5318 | -0.08751 | -0.1104 | -0.0646 | -0.075 | -0.7253 | 1.819e-11 | 2.171e-10 | 1.976e-07 | 0.004668 | 0.7339 |
| region_dropout_midline_motor_strip_0.046875 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5323 | -0.08699 | -0.1086 | -0.06533 | -0.075 | -0.7627 | 2.629e-12 | 2.936e-11 | 1.743e-09 | 0.03097 | 0.7706 |
| region_dropout_right_motor_strip_0.140625 | balanced_accuracy | secondary | 109 | 0.6193 | 0.5294 | -0.08983 | -0.112 | -0.06766 | -0.085 | -0.7691 | 1.943e-12 | 6.435e-11 | 1.312e-10 | 0.07927 | 0.789 |
| channel_dropout_0.1 | roc_auc | primary | 109 | 0.655 | 0.5898 | -0.0652 | -0.08047 | -0.04994 | -0.062 | -0.8108 | 2.383e-13 | 1.698e-11 | 1.727e-09 | 0.9737 | 0.789 |
| channel_dropout_0.2 | roc_auc | primary | 109 | 0.655 | 0.5532 | -0.1018 | -0.1232 | -0.0804 | -0.1025 | -0.9033 | 1.951e-15 | 1.364e-12 | 3.402e-11 | 0.6121 | 0.8165 |
| channel_dropout_0.3 | roc_auc | primary | 109 | 0.655 | 0.5433 | -0.1117 | -0.1348 | -0.08862 | -0.115 | -0.9179 | 9.96e-16 | 6.944e-13 | 1.824e-08 | 0.48 | 0.7706 |
| channel_dropout_0.5 | roc_auc | primary | 109 | 0.655 | 0.5273 | -0.1277 | -0.1534 | -0.102 | -0.1295 | -0.944 | 2.55e-16 | 4.938e-13 | 4.979e-10 | 0.438 | 0.7982 |
| reduced_montage_motor_core | roc_auc | primary | 109 | 0.655 | 0.6483 | -0.006707 | -0.03465 | 0.02123 | -0.02 | -0.04558 | 0.6351 | 0.5467 | 0.6454 | 0.8705 | 0.5138 |
| reduced_montage_motor_extended | roc_auc | primary | 109 | 0.655 | 0.6687 | 0.01365 | -0.01312 | 0.04042 | 0.02 | 0.09684 | 0.3327 | 0.2078 | 0.186 | 0.2523 | 0.4128 |
| region_dropout_left_motor_strip_0.140625 | roc_auc | primary | 109 | 0.655 | 0.5974 | -0.05765 | -0.07704 | -0.03826 | -0.05 | -0.5645 | 5.604e-08 | 6.17e-07 | 0.0001779 | 0.1594 | 0.6514 |
| region_dropout_midline_motor_strip_0.046875 | roc_auc | primary | 109 | 0.655 | 0.6066 | -0.04839 | -0.06558 | -0.0312 | -0.05 | -0.5345 | 2.228e-07 | 2.447e-07 | 1.285e-05 | 0.4809 | 0.6789 |
| region_dropout_right_motor_strip_0.140625 | roc_auc | primary | 109 | 0.655 | 0.5936 | -0.06138 | -0.08334 | -0.03943 | -0.045 | -0.5308 | 2.563e-07 | 1.964e-06 | 1.285e-05 | 0.08966 | 0.6789 |

## Sensitivity summary
| condition | metric | available | role | n_subjects | mean_delta_condition_minus_clean | pct_worse_than_clean | ttest_fdr | wilcoxon_fdr | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | roc_auc | True | primary | 109 | -0.0652 | 0.789 | 2.383e-13 | 1.698e-11 | primary |
| channel_dropout_0.1 | balanced_accuracy | True | secondary | 109 | -0.09421 | 0.789 | 2.468e-13 | 1.371e-11 | secondary |
| channel_dropout_0.1 | brier_score | True | calibration | 109 | 0.1418 | 0.9725 | 2.886e-31 | 2.781e-18 | calibration_optional |
| channel_dropout_0.1 | ece | True | calibration | 109 | 0.1105 | 0.8991 | 7.692e-21 | 2.146e-16 | calibration_optional |
| channel_dropout_0.2 | roc_auc | True | primary | 109 | -0.1018 | 0.8165 | 1.951e-15 | 1.364e-12 | primary |
| channel_dropout_0.2 | balanced_accuracy | True | secondary | 109 | -0.107 | 0.7706 | 1.811e-13 | 1.19e-11 | secondary |
| channel_dropout_0.2 | brier_score | True | calibration | 109 | 0.1634 | 0.9725 | 1.965e-31 | 2.781e-18 | calibration_optional |
| channel_dropout_0.2 | ece | True | calibration | 109 | 0.1271 | 0.8991 | 5.413e-21 | 1.487e-16 | calibration_optional |
| channel_dropout_0.3 | roc_auc | True | primary | 109 | -0.1117 | 0.7706 | 9.96e-16 | 6.944e-13 | primary |
| channel_dropout_0.3 | balanced_accuracy | True | secondary | 109 | -0.1118 | 0.7798 | 1.001e-13 | 1.046e-11 | secondary |
| channel_dropout_0.3 | brier_score | True | calibration | 109 | 0.1692 | 0.9633 | 1.965e-31 | 2.781e-18 | calibration_optional |
| channel_dropout_0.3 | ece | True | calibration | 109 | 0.1315 | 0.9083 | 4.088e-21 | 8.998e-17 | calibration_optional |
| channel_dropout_0.5 | roc_auc | True | primary | 109 | -0.1277 | 0.7982 | 2.55e-16 | 4.938e-13 | primary |
| channel_dropout_0.5 | balanced_accuracy | True | secondary | 109 | -0.1146 | 0.7615 | 9.679e-14 | 8.77e-12 | secondary |
| channel_dropout_0.5 | brier_score | True | calibration | 109 | 0.1754 | 0.9725 | 1.965e-31 | 2.781e-18 | calibration_optional |
| channel_dropout_0.5 | ece | True | calibration | 109 | 0.1371 | 0.9083 | 1.883e-21 | 9.109e-17 | calibration_optional |
| reduced_montage_motor_core | roc_auc | True | primary | 109 | -0.006707 | 0.5138 | 0.6351 | 0.5467 | primary |
| reduced_montage_motor_core | balanced_accuracy | True | secondary | 109 | -0.007217 | 0.5046 | 0.5767 | 0.6206 | secondary |
| reduced_montage_motor_core | brier_score | True | calibration | 109 | -0.06713 | 0.1835 | 3.848e-13 | 1.501e-11 | calibration_optional |
| reduced_montage_motor_core | ece | True | calibration | 109 | -0.06416 | 0.2569 | 1.607e-09 | 6.039e-09 | calibration_optional |
| reduced_montage_motor_extended | roc_auc | True | primary | 109 | 0.01365 | 0.4128 | 0.3327 | 0.2078 | primary |
| reduced_montage_motor_extended | balanced_accuracy | True | secondary | 109 | 0.01139 | 0.422 | 0.329 | 0.2717 | secondary |
| reduced_montage_motor_extended | brier_score | True | calibration | 109 | -0.04152 | 0.2844 | 4.863e-07 | 6.497e-07 | calibration_optional |
| reduced_montage_motor_extended | ece | True | calibration | 109 | -0.02214 | 0.3486 | 0.0126 | 0.007985 | calibration_optional |
| region_dropout_left_motor_strip_0.140625 | roc_auc | True | primary | 109 | -0.05765 | 0.6514 | 5.604e-08 | 6.17e-07 | primary |
| region_dropout_left_motor_strip_0.140625 | balanced_accuracy | True | secondary | 109 | -0.08751 | 0.7339 | 1.819e-11 | 2.171e-10 | secondary |
| region_dropout_left_motor_strip_0.140625 | brier_score | True | calibration | 109 | 0.1255 | 0.9266 | 1.854e-22 | 1.752e-17 | calibration_optional |
| region_dropout_left_motor_strip_0.140625 | ece | True | calibration | 109 | 0.09754 | 0.8624 | 1.951e-15 | 3.534e-14 | calibration_optional |
| region_dropout_midline_motor_strip_0.046875 | roc_auc | True | primary | 109 | -0.04839 | 0.6789 | 2.228e-07 | 2.447e-07 | primary |
| region_dropout_midline_motor_strip_0.046875 | balanced_accuracy | True | secondary | 109 | -0.08699 | 0.7706 | 2.629e-12 | 2.936e-11 | secondary |
| region_dropout_midline_motor_strip_0.046875 | brier_score | True | calibration | 109 | 0.1297 | 0.9358 | 3.207e-26 | 3.844e-18 | calibration_optional |
| region_dropout_midline_motor_strip_0.046875 | ece | True | calibration | 109 | 0.09933 | 0.8073 | 7.417e-17 | 1.099e-14 | calibration_optional |
| region_dropout_right_motor_strip_0.140625 | roc_auc | True | primary | 109 | -0.06138 | 0.6789 | 2.563e-07 | 1.964e-06 | primary |
| region_dropout_right_motor_strip_0.140625 | balanced_accuracy | True | secondary | 109 | -0.08983 | 0.789 | 1.943e-12 | 6.435e-11 | secondary |
| region_dropout_right_motor_strip_0.140625 | brier_score | True | calibration | 109 | 0.1262 | 0.9083 | 1.901e-25 | 1.762e-17 | calibration_optional |
| region_dropout_right_motor_strip_0.140625 | ece | True | calibration | 109 | 0.1001 | 0.8716 | 1.502e-17 | 1.099e-14 | calibration_optional |

## Channel-dropout slopes
| dataset | pipeline | metric | n_subjects | mean_slope_per_10pct_dropout | slope_ci_low | slope_ci_high | slope_sd | t_statistic_vs_zero | t_p_value_vs_zero | shapiro_p_value_slope | n_harmful_slope | pct_harmful_slope | t_p_value_vs_zero_bh_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PhysionetMotorImagery | csp_lda | balanced_accuracy | 109 | -0.01864 | -0.0229 | -0.01437 | 0.02246 | -8.663 | 4.986e-14 | 0.01154 | 85 | 0.7798 | 4.986e-14 |
| PhysionetMotorImagery | csp_lda | brier_score | 109 | 0.02862 | 0.02525 | 0.032 | 0.01777 | 16.82 | 6.176e-32 | 0.009897 | 106 | 0.9725 | 2.47e-31 |
| PhysionetMotorImagery | csp_lda | ece | 109 | 0.02238 | 0.01872 | 0.02604 | 0.01929 | 12.11 | 7.554e-22 | 0.004765 | 100 | 0.9174 | 1.511e-21 |
| PhysionetMotorImagery | csp_lda | roc_auc | 109 | -0.02353 | -0.02826 | -0.01881 | 0.02489 | -9.871 | 9.153e-17 | 0.3653 | 88 | 0.8073 | 1.22e-16 |

## Overclaim-risk flags
| flag | triggered | detail |
| --- | --- | --- |
| low_subject_count | False | n_subjects=109; population-level claims should be cautious below 20 subjects. |
| development_subset_prefix | False | Prefix contains 'dev'; treat as development output, not final population estimate. |
| missing_calibration_metrics | False | Missing optional calibration metrics: none |
| cross_session_absent | True | Cross-session stressor absent. |
| skipped_subject_log_present | False | Found 0 failed-subject log files matching prefix. |
| uneven_or_low_paired_n | False | minimum paired n=109; total subject n=109. |

## Statistical notes
- Paired effects are computed within subject against the clean all-channel baseline.
- Confidence intervals for mean paired deltas and slopes use Student t intervals.
- Median-delta intervals use a distribution-free sign-test/order-statistic interval.
- Normality of paired deltas/slopes is screened with Shapiro-Wilk where sample size permits.
- Wilcoxon signed-rank and sign tests are reported as sensitivity checks for paired deltas.
- Benjamini-Hochberg false discovery rate correction is applied to paired t-test, Wilcoxon, and sign-test p-values.