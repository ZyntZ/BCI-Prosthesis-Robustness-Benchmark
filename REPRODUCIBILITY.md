# Reproducibility guide

## Environment

```bash
conda env create -f environment.yml
conda activate bci-robustness-benchmark
```

or

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Smoke checks

```bash
python scripts/run_benchmark.py --config configs/benchmark.yaml --dry-run
python -m compileall -q scripts src
```

## Recreate derived PhysioNetMI development outputs

```bash
python scripts/analyze_robustness.py --results-dir results --prefix PhysionetMI_dev10 --reports-dir reports
python scripts/recommend_interventions.py --results-dir results --reports-dir reports --prefix PhysionetMI_dev10
python scripts/final_statistics.py --results-dir results --prefix PhysionetMI_dev10
```

## Full benchmark runs

```bash
make bnci-full
make physionet-full
```

Full runs download and preprocess EEG data through MOABB/MNE and can take substantial time.
