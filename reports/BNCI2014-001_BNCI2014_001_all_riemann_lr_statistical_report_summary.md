# Statistical reporting pack for `BNCI2014-001_BNCI2014_001_all_riemann_lr`

Generated from existing subject-summary CSV files only; no simulated or additional benchmark observations are used.

## Methods audit
| check | value | status |
| --- | --- | --- |
| n_rows_subject_summary | 72 | info |
| n_subjects | 9 | info |
| n_conditions | 8 | info |
| duplicate_subject_condition_rows | 0 | pass |
| missing_roc_auc | 0 | pass |
| out_of_range_0_1_roc_auc | 0 | pass |
| missing_balanced_accuracy | 0 | pass |
| out_of_range_0_1_balanced_accuracy | 0 | pass |
| missing_brier_score | 0 | pass |
| out_of_range_0_1_brier_score | 0 | pass |
| missing_ece | 0 | pass |
| out_of_range_0_1_ece | 0 | pass |
| min_subjects_per_condition | 9 | pass |
| max_subjects_per_condition | 9 | info |

## Paired stressor effects vs clean all-channel baseline
| condition | metric | metric_role | n_subjects | clean_mean | condition_mean | mean_delta_condition_minus_clean | delta_ci_low | delta_ci_high | median_delta_condition_minus_clean | cohens_dz | t_p_value_bh_fdr | wilcoxon_p_value_bh_fdr | sign_test_p_value_bh_fdr | shapiro_p_value_delta | pct_worse_than_clean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | balanced_accuracy | secondary | 9 | 0.8271 | 0.6251 | -0.202 | -0.2395 | -0.1644 | -0.2143 | -4.138 | 5.145e-06 | 0.004755 | 0.004755 | 0.142 | 1 |
| channel_dropout_0.2 | balanced_accuracy | secondary | 9 | 0.8271 | 0.5718 | -0.2553 | -0.3154 | -0.1951 | -0.2842 | -3.261 | 2.802e-05 | 0.004755 | 0.004755 | 0.1571 | 1 |
| channel_dropout_0.3 | balanced_accuracy | secondary | 9 | 0.8271 | 0.5392 | -0.2879 | -0.3588 | -0.217 | -0.3156 | -3.123 | 3.509e-05 | 0.004755 | 0.004755 | 0.1657 | 1 |
| channel_dropout_0.5 | balanced_accuracy | secondary | 9 | 0.8271 | 0.5127 | -0.3144 | -0.4009 | -0.228 | -0.3276 | -2.796 | 6.686e-05 | 0.004755 | 0.004755 | 0.4285 | 1 |
| cross_session_0 | balanced_accuracy | secondary | 9 | 0.8271 | 0.7716 | -0.0555 | -0.1226 | 0.01155 | -0.02789 | -0.6363 | 0.1038 | 0.009115 | 0.04557 | 0.0005981 | 0.8889 |
| reduced_montage_motor_core | balanced_accuracy | secondary | 9 | 0.8271 | 0.7143 | -0.1128 | -0.1499 | -0.07565 | -0.1106 | -2.336 | 0.0002238 | 0.004755 | 0.004755 | 0.03291 | 1 |
| reduced_montage_motor_extended | balanced_accuracy | secondary | 9 | 0.8271 | 0.7661 | -0.06102 | -0.0993 | -0.02273 | -0.03485 | -1.225 | 0.00835 | 0.004755 | 0.004755 | 0.05136 | 1 |
| channel_dropout_0.1 | roc_auc | primary | 9 | 0.8854 | 0.8546 | -0.03073 | -0.0469 | -0.01456 | -0.02824 | -1.461 | 0.003447 | 0.004755 | 0.004755 | 0.6068 | 1 |
| channel_dropout_0.2 | roc_auc | primary | 9 | 0.8854 | 0.8222 | -0.06314 | -0.08945 | -0.03684 | -0.07453 | -1.845 | 0.0009053 | 0.004755 | 0.004755 | 0.2462 | 1 |
| channel_dropout_0.3 | roc_auc | primary | 9 | 0.8854 | 0.7781 | -0.1072 | -0.1465 | -0.068 | -0.1102 | -2.101 | 0.0004057 | 0.004755 | 0.004755 | 0.5227 | 1 |
| channel_dropout_0.5 | roc_auc | primary | 9 | 0.8854 | 0.7199 | -0.1655 | -0.2095 | -0.1214 | -0.1536 | -2.888 | 5.715e-05 | 0.004755 | 0.004755 | 0.8262 | 1 |
| cross_session_0 | roc_auc | primary | 9 | 0.8854 | 0.8703 | -0.01511 | -0.02985 | -0.0003617 | -0.001775 | -0.7875 | 0.0534 | 0.1094 | 0.5687 | 0.04564 | 0.6667 |
| reduced_montage_motor_core | roc_auc | primary | 9 | 0.8854 | 0.7681 | -0.1173 | -0.169 | -0.06553 | -0.1287 | -1.742 | 0.001238 | 0.004755 | 0.004755 | 0.9282 | 1 |
| reduced_montage_motor_extended | roc_auc | primary | 9 | 0.8854 | 0.8282 | -0.05716 | -0.1015 | -0.01286 | -0.0308 | -0.9918 | 0.02255 | 0.004755 | 0.004755 | 0.1015 | 1 |

## Sensitivity summary
| condition | metric | available | role | n_subjects | mean_delta_condition_minus_clean | pct_worse_than_clean | ttest_fdr | wilcoxon_fdr | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | roc_auc | True | primary | 9 | -0.03073 | 1 | 0.003447 | 0.004755 | primary |
| channel_dropout_0.1 | balanced_accuracy | True | secondary | 9 | -0.202 | 1 | 5.145e-06 | 0.004755 | secondary |
| channel_dropout_0.1 | brier_score | True | calibration | 9 | 0.1639 | 1 | 7.55e-07 | 0.004755 | calibration_optional |
| channel_dropout_0.1 | ece | True | calibration | 9 | 0.1923 | 1 | 6.621e-07 | 0.004755 | calibration_optional |
| channel_dropout_0.2 | roc_auc | True | primary | 9 | -0.06314 | 1 | 0.0009053 | 0.004755 | primary |
| channel_dropout_0.2 | balanced_accuracy | True | secondary | 9 | -0.2553 | 1 | 2.802e-05 | 0.004755 | secondary |
| channel_dropout_0.2 | brier_score | True | calibration | 9 | 0.2285 | 1 | 1.489e-06 | 0.004755 | calibration_optional |
| channel_dropout_0.2 | ece | True | calibration | 9 | 0.2463 | 1 | 8.326e-09 | 0.004755 | calibration_optional |
| channel_dropout_0.3 | roc_auc | True | primary | 9 | -0.1072 | 1 | 0.0004057 | 0.004755 | primary |
| channel_dropout_0.3 | balanced_accuracy | True | secondary | 9 | -0.2879 | 1 | 3.509e-05 | 0.004755 | secondary |
| channel_dropout_0.3 | brier_score | True | calibration | 9 | 0.2584 | 1 | 1.489e-06 | 0.004755 | calibration_optional |
| channel_dropout_0.3 | ece | True | calibration | 9 | 0.2706 | 1 | 8.326e-09 | 0.004755 | calibration_optional |
| channel_dropout_0.5 | roc_auc | True | primary | 9 | -0.1655 | 1 | 5.715e-05 | 0.004755 | primary |
| channel_dropout_0.5 | balanced_accuracy | True | secondary | 9 | -0.3144 | 1 | 6.686e-05 | 0.004755 | secondary |
| channel_dropout_0.5 | brier_score | True | calibration | 9 | 0.3035 | 1 | 5.145e-06 | 0.004755 | calibration_optional |
| channel_dropout_0.5 | ece | True | calibration | 9 | 0.306 | 1 | 1.448e-08 | 0.004755 | calibration_optional |
| cross_session_0 | roc_auc | True | primary | 9 | -0.01511 | 0.6667 | 0.0534 | 0.1094 | primary |
| cross_session_0 | balanced_accuracy | True | secondary | 9 | -0.0555 | 0.8889 | 0.1038 | 0.009115 | secondary |
| cross_session_0 | brier_score | True | calibration | 9 | 0.02568 | 1 | 0.04942 | 0.004755 | calibration_optional |
| cross_session_0 | ece | True | calibration | 9 | 0.01314 | 0.4444 | 0.4991 | 0.6765 | calibration_optional |
| reduced_montage_motor_core | roc_auc | True | primary | 9 | -0.1173 | 1 | 0.001238 | 0.004755 | primary |
| reduced_montage_motor_core | balanced_accuracy | True | secondary | 9 | -0.1128 | 1 | 0.0002238 | 0.004755 | secondary |
| reduced_montage_motor_core | brier_score | True | calibration | 9 | 0.06023 | 1 | 0.0003987 | 0.004755 | calibration_optional |
| reduced_montage_motor_core | ece | True | calibration | 9 | 0.003732 | 0.4444 | 0.7694 | 0.9102 | calibration_optional |
| reduced_montage_motor_extended | roc_auc | True | primary | 9 | -0.05716 | 1 | 0.02255 | 0.004755 | primary |
| reduced_montage_motor_extended | balanced_accuracy | True | secondary | 9 | -0.06102 | 1 | 0.00835 | 0.004755 | secondary |
| reduced_montage_motor_extended | brier_score | True | calibration | 9 | 0.02593 | 1 | 0.007587 | 0.004755 | calibration_optional |
| reduced_montage_motor_extended | ece | True | calibration | 9 | -0.002617 | 0.4444 | 0.7218 | 0.6142 | calibration_optional |

## Channel-dropout slopes
| dataset | pipeline | metric | n_subjects | mean_slope_per_10pct_dropout | slope_ci_low | slope_ci_high | slope_sd | t_statistic_vs_zero | t_p_value_vs_zero | shapiro_p_value_slope | n_harmful_slope | pct_harmful_slope | t_p_value_vs_zero_bh_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BNCI2014-001 | riemann_lr | balanced_accuracy | 9 | -0.05522 | -0.0724 | -0.03804 | 0.02235 | -7.411 | 7.541e-05 | 0.5293 | 9 | 1 | 7.541e-05 |
| BNCI2014-001 | riemann_lr | brier_score | 9 | 0.055 | 0.04336 | 0.06665 | 0.01515 | 10.89 | 4.461e-06 | 0.4236 | 9 | 1 | 8.922e-06 |
| BNCI2014-001 | riemann_lr | ece | 9 | 0.0536 | 0.04755 | 0.05965 | 0.007872 | 20.43 | 3.45e-08 | 0.3723 | 9 | 1 | 1.38e-07 |
| BNCI2014-001 | riemann_lr | roc_auc | 9 | -0.03376 | -0.04284 | -0.02468 | 0.01181 | -8.575 | 2.641e-05 | 0.8435 | 9 | 1 | 3.521e-05 |

## Overclaim-risk flags
| flag | triggered | detail |
| --- | --- | --- |
| low_subject_count | True | n_subjects=9; population-level claims should be cautious below 20 subjects. |
| development_subset_prefix | False | Prefix contains 'dev'; treat as development output, not final population estimate. |
| missing_calibration_metrics | False | Missing optional calibration metrics: none |
| cross_session_absent | False | Cross-session stressor present. |
| skipped_subject_log_present | False | Found 0 failed-subject log files matching prefix. |
| uneven_or_low_paired_n | False | minimum paired n=9; total subject n=9. |

## Statistical notes
- Paired effects are computed within subject against the clean all-channel baseline.
- Confidence intervals for mean paired deltas and slopes use Student t intervals.
- Median-delta intervals use a distribution-free sign-test/order-statistic interval.
- Normality of paired deltas/slopes is screened with Shapiro-Wilk where sample size permits.
- Wilcoxon signed-rank and sign tests are reported as sensitivity checks for paired deltas.
- Benjamini-Hochberg false discovery rate correction is applied to paired t-test, Wilcoxon, and sign-test p-values.