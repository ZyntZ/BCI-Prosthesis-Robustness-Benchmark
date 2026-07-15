# Statistical reporting pack for `BNCI2014-001_BNCI2014_001_all_csp_lda`

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
| channel_dropout_0.1 | balanced_accuracy | secondary | 9 | 0.7876 | 0.543 | -0.2446 | -0.3398 | -0.1494 | -0.2588 | -1.975 | 0.000697 | 0.006076 | 0.006076 | 0.6006 | 1 |
| channel_dropout_0.2 | balanced_accuracy | secondary | 9 | 0.7876 | 0.5232 | -0.2644 | -0.3692 | -0.1595 | -0.2813 | -1.938 | 0.000697 | 0.006076 | 0.006076 | 0.3979 | 1 |
| channel_dropout_0.3 | balanced_accuracy | secondary | 9 | 0.7876 | 0.5162 | -0.2714 | -0.3785 | -0.1642 | -0.331 | -1.946 | 0.000697 | 0.006076 | 0.006076 | 0.4318 | 1 |
| channel_dropout_0.5 | balanced_accuracy | secondary | 9 | 0.7876 | 0.5114 | -0.2761 | -0.3854 | -0.1669 | -0.3153 | -1.943 | 0.000697 | 0.006076 | 0.006076 | 0.4352 | 1 |
| cross_session_0 | balanced_accuracy | secondary | 9 | 0.7876 | 0.7569 | -0.03062 | -0.07482 | 0.01358 | -0.02787 | -0.5325 | 0.1737 | 0.1444 | 0.2012 | 0.5218 | 0.7778 |
| reduced_montage_motor_core | balanced_accuracy | secondary | 9 | 0.7876 | 0.703 | -0.08458 | -0.1265 | -0.0427 | -0.06244 | -1.553 | 0.002683 | 0.006076 | 0.006076 | 0.05334 | 1 |
| reduced_montage_motor_extended | balanced_accuracy | secondary | 9 | 0.7876 | 0.7519 | -0.03566 | -0.07139 | 7.428e-05 | -0.01798 | -0.7671 | 0.06717 | 0.01727 | 0.05469 | 0.008332 | 0.8889 |
| channel_dropout_0.1 | roc_auc | primary | 9 | 0.8414 | 0.7331 | -0.1084 | -0.1392 | -0.07754 | -0.1195 | -2.703 | 0.0001108 | 0.006076 | 0.006076 | 0.4671 | 1 |
| channel_dropout_0.2 | roc_auc | primary | 9 | 0.8414 | 0.7021 | -0.1393 | -0.182 | -0.09671 | -0.166 | -2.512 | 0.0001561 | 0.006076 | 0.006076 | 0.06742 | 1 |
| channel_dropout_0.3 | roc_auc | primary | 9 | 0.8414 | 0.646 | -0.1954 | -0.2521 | -0.1387 | -0.2176 | -2.65 | 0.0001162 | 0.006076 | 0.006076 | 0.457 | 1 |
| channel_dropout_0.5 | roc_auc | primary | 9 | 0.8414 | 0.6215 | -0.2199 | -0.2822 | -0.1576 | -0.2495 | -2.714 | 0.0001108 | 0.006076 | 0.006076 | 0.1061 | 1 |
| cross_session_0 | roc_auc | primary | 9 | 0.8414 | 0.853 | 0.01154 | -0.009758 | 0.03284 | 0.003895 | 0.4165 | 0.2658 | 0.3239 | 0.5469 | 0.5007 | 0.3333 |
| reduced_montage_motor_core | roc_auc | primary | 9 | 0.8414 | 0.7605 | -0.08096 | -0.1303 | -0.03163 | -0.077 | -1.261 | 0.008329 | 0.006076 | 0.006076 | 0.0161 | 1 |
| reduced_montage_motor_extended | roc_auc | primary | 9 | 0.8414 | 0.8054 | -0.03604 | -0.08536 | 0.01329 | -0.008196 | -0.5616 | 0.1589 | 0.09035 | 0.2012 | 0.001253 | 0.7778 |

## Sensitivity summary
| condition | metric | available | role | n_subjects | mean_delta_condition_minus_clean | pct_worse_than_clean | ttest_fdr | wilcoxon_fdr | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| channel_dropout_0.1 | roc_auc | True | primary | 9 | -0.1084 | 1 | 0.0001108 | 0.006076 | primary |
| channel_dropout_0.1 | balanced_accuracy | True | secondary | 9 | -0.2446 | 1 | 0.000697 | 0.006076 | secondary |
| channel_dropout_0.1 | brier_score | True | calibration | 9 | 0.2759 | 1 | 3.547e-05 | 0.006076 | calibration_optional |
| channel_dropout_0.1 | ece | True | calibration | 9 | 0.2968 | 1 | 2.74e-06 | 0.006076 | calibration_optional |
| channel_dropout_0.2 | roc_auc | True | primary | 9 | -0.1393 | 1 | 0.0001561 | 0.006076 | primary |
| channel_dropout_0.2 | balanced_accuracy | True | secondary | 9 | -0.2644 | 1 | 0.000697 | 0.006076 | secondary |
| channel_dropout_0.2 | brier_score | True | calibration | 9 | 0.2991 | 1 | 3.865e-05 | 0.006076 | calibration_optional |
| channel_dropout_0.2 | ece | True | calibration | 9 | 0.3173 | 1 | 2.74e-06 | 0.006076 | calibration_optional |
| channel_dropout_0.3 | roc_auc | True | primary | 9 | -0.1954 | 1 | 0.0001162 | 0.006076 | primary |
| channel_dropout_0.3 | balanced_accuracy | True | secondary | 9 | -0.2714 | 1 | 0.000697 | 0.006076 | secondary |
| channel_dropout_0.3 | brier_score | True | calibration | 9 | 0.3057 | 1 | 3.547e-05 | 0.006076 | calibration_optional |
| channel_dropout_0.3 | ece | True | calibration | 9 | 0.322 | 1 | 2.74e-06 | 0.006076 | calibration_optional |
| channel_dropout_0.5 | roc_auc | True | primary | 9 | -0.2199 | 1 | 0.0001108 | 0.006076 | primary |
| channel_dropout_0.5 | balanced_accuracy | True | secondary | 9 | -0.2761 | 1 | 0.000697 | 0.006076 | secondary |
| channel_dropout_0.5 | brier_score | True | calibration | 9 | 0.3112 | 1 | 2.601e-05 | 0.006076 | calibration_optional |
| channel_dropout_0.5 | ece | True | calibration | 9 | 0.3284 | 1 | 2.527e-06 | 0.006076 | calibration_optional |
| cross_session_0 | roc_auc | True | primary | 9 | 0.01154 | 0.3333 | 0.2658 | 0.3239 | primary |
| cross_session_0 | balanced_accuracy | True | secondary | 9 | -0.03062 | 0.7778 | 0.1737 | 0.1444 | secondary |
| cross_session_0 | brier_score | True | calibration | 9 | 0.0254 | 0.8889 | 0.06877 | 0.0696 | calibration_optional |
| cross_session_0 | ece | True | calibration | 9 | 0.0392 | 0.7778 | 0.01698 | 0.03646 | calibration_optional |
| reduced_montage_motor_core | roc_auc | True | primary | 9 | -0.08096 | 1 | 0.008329 | 0.006076 | primary |
| reduced_montage_motor_core | balanced_accuracy | True | secondary | 9 | -0.08458 | 1 | 0.002683 | 0.006076 | secondary |
| reduced_montage_motor_core | brier_score | True | calibration | 9 | 0.03875 | 0.7778 | 0.03318 | 0.02734 | calibration_optional |
| reduced_montage_motor_core | ece | True | calibration | 9 | -0.003456 | 0.5556 | 0.8572 | 1 | calibration_optional |
| reduced_montage_motor_extended | roc_auc | True | primary | 9 | -0.03604 | 0.7778 | 0.1589 | 0.09035 | primary |
| reduced_montage_motor_extended | balanced_accuracy | True | secondary | 9 | -0.03566 | 0.8889 | 0.06717 | 0.01727 | secondary |
| reduced_montage_motor_extended | brier_score | True | calibration | 9 | 0.01446 | 0.7778 | 0.2373 | 0.1444 | calibration_optional |
| reduced_montage_motor_extended | ece | True | calibration | 9 | -0.004586 | 0.4444 | 0.6414 | 0.6765 | calibration_optional |

## Channel-dropout slopes
| dataset | pipeline | metric | n_subjects | mean_slope_per_10pct_dropout | slope_ci_low | slope_ci_high | slope_sd | t_statistic_vs_zero | t_p_value_vs_zero | shapiro_p_value_slope | n_harmful_slope | pct_harmful_slope | t_p_value_vs_zero_bh_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BNCI2014-001 | csp_lda | balanced_accuracy | 9 | -0.04351 | -0.06092 | -0.02609 | 0.02266 | -5.76 | 0.0004241 | 0.4244 | 9 | 1 | 0.0004241 |
| BNCI2014-001 | csp_lda | brier_score | 9 | 0.04899 | 0.03852 | 0.05945 | 0.01362 | 10.79 | 4.792e-06 | 0.3421 | 9 | 1 | 9.585e-06 |
| BNCI2014-001 | csp_lda | ece | 9 | 0.05118 | 0.04449 | 0.05788 | 0.008709 | 17.63 | 1.095e-07 | 0.7359 | 9 | 1 | 4.38e-07 |
| BNCI2014-001 | csp_lda | roc_auc | 9 | -0.0415 | -0.05415 | -0.02885 | 0.01646 | -7.566 | 6.511e-05 | 0.255 | 9 | 1 | 8.682e-05 |

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