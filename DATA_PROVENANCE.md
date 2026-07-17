# Data provenance

This repository contains code and example benchmark outputs derived from EEG datasets accessed through MOABB/MNE wrappers.

Included example outputs:

- `BNCI2014-001_BNCI2014_001_all_csp_lda*`: BNCI2014-001 subjects 1-9 with CSP+LDA.
- `BNCI2014-001_BNCI2014_001_all_riemann_lr*`: BNCI2014-001 subjects 1-9 with a Riemannian tangent-space logistic regression baseline.

Raw EEG data are not bundled. Reproduction requires downloading datasets through MOABB/MNE and following the dataset providers' license requirements.


## Full PhysioNet release outputs

- `PhysionetMI_PhysionetMI_all_csp_lda*`: 109 participants; fold-level and participant-level outputs are included.
- `PhysionetMI_PhysionetMI_all_riemann_lr*`: 109 participants; participant-level outputs are included, but the fold-level `results.csv` is unavailable. It was not reconstructed or fabricated.
- The legacy Riemann-LR participant summary retains regional dropout fractions but not anatomical region names. Direct model comparison therefore uses matched 3/64 and 9/64 channel-dropout fractions; separate left/right effects cannot be recovered.
- PhysioNet cross-session rows were not available. Cross-session results in the manuscript are restricted to BNCI2014-001 (`n=9`).
