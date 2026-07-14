#!/usr/bin/env python3
"""Generate restrained methods figures from existing benchmark CSV outputs only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DEFAULT_PREFIX = "BNCI2014-001_BNCI2014_001_all_riemann_lr"
INK = "#222222"
MUTED = "#666666"
BLUE = "#1f5a7a"


def set_style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9,
        "axes.labelsize": 8.5, "axes.edgecolor": INK, "axes.linewidth": 0.8,
        "xtick.color": INK, "ytick.color": INK, "text.color": INK,
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    })


def require_columns(df: pd.DataFrame, cols: set[str], source: Path | str) -> None:
    missing = cols - set(df.columns)
    if missing:
        raise ValueError(f"{source} is missing required columns: {sorted(missing)}")


def load_subject_summary(results_dir: Path, prefix: str) -> pd.DataFrame:
    path = results_dir / f"{prefix}_subject_summary.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    require_columns(df, {"dataset", "subject", "pipeline", "stressor", "dropout_fraction", "roc_auc", "balanced_accuracy"}, path)
    return df


def save(fig: plt.Figure, base: Path) -> dict[str, str]:
    base.parent.mkdir(parents=True, exist_ok=True)
    png, svg = base.with_suffix(".png"), base.with_suffix(".svg")
    fig.savefig(png, dpi=400, bbox_inches="tight", pad_inches=0.04)
    fig.savefig(svg, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return {"png": str(png), "svg": str(svg)}


def metric_label(metric: str) -> str:
    return "ROC AUC" if metric == "roc_auc" else metric.replace("_", " ").title()


def load_intervention_classes(results_dir: Path, prefix: str) -> tuple[pd.DataFrame, Path]:
    for path in [results_dir / f"{prefix}_final_intervention_classes.csv", results_dir / f"{prefix}_subject_risk_cards.csv"]:
        if path.exists():
            df = pd.read_csv(path)
            if "intervention_class" in df.columns:
                return df, path
            if "risk_level" in df.columns:
                out = df.copy(); out["intervention_class"] = out["risk_level"]
                return out, path
    raise FileNotFoundError(f"No intervention class or risk-card CSV found for prefix {prefix}")


def dropout_table(subj: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    keep = subj[subj["stressor"].isin(["clean", "channel_dropout"])].copy()
    keep["dropout_fraction"] = keep["dropout_fraction"].astype(float)
    pivot = keep.pivot_table(index="subject", columns="dropout_fraction", values=metric, aggfunc="mean").sort_index(axis=1)
    if pivot.shape[1] < 2:
        raise ValueError("Need at least two dropout fractions")
    rows = []
    for frac, values in pivot.items():
        x = values.dropna().astype(float).to_numpy()
        mean = float(x.mean())
        if len(x) > 1:
            se = float(x.std(ddof=1) / np.sqrt(len(x)))
            lo, hi = stats.t.interval(0.95, len(x) - 1, loc=mean, scale=se)
        else:
            lo = hi = np.nan
        rows.append({"dropout_fraction": float(frac), "mean": mean, "ci_low": float(lo), "ci_high": float(hi), "n": int(len(x))})
    return pivot, pd.DataFrame(rows)


def pipeline_schematic(subj: pd.DataFrame, prefix: str, reports_dir: Path) -> dict[str, str]:
    set_style()
    dataset = ", ".join(sorted(map(str, subj["dataset"].dropna().unique())))
    pipeline = ", ".join(sorted(map(str, subj["pipeline"].dropna().unique())))
    n_subjects = int(subj["subject"].nunique())
    stressors = ", ".join(sorted(map(str, subj["stressor"].dropna().unique())))
    metrics = ", ".join([m for m in ["roc_auc", "balanced_accuracy", "brier_score", "ece"] if m in subj.columns and not subj[m].isna().all()])
    steps = [("Open EEG", f"{dataset}\nn={n_subjects}"), ("MOABB/MNE", "load metadata"), ("Preprocess", "epochs, channels"), ("Decoder", pipeline), ("Stress tests", stressors), ("Subject table", "fold means"), ("Paired stats", metrics)]
    fig, ax = plt.subplots(figsize=(7.4, 1.9)); ax.axis("off")
    xs = np.linspace(0.05, 0.95, len(steps))
    for i, (x, (title, body)) in enumerate(zip(xs, steps)):
        ax.text(x, 0.62, title, ha="center", va="center", weight="bold", fontsize=7.8)
        ax.text(x, 0.36, body, ha="center", va="center", fontsize=6.4, color=MUTED, wrap=True)
        if i < len(xs) - 1:
            ax.annotate("", xy=(xs[i+1]-0.045, 0.5), xytext=(x+0.045, 0.5), arrowprops={"arrowstyle": "->", "lw": 0.8, "color": MUTED})
    ax.text(0.0, 0.96, "A", transform=ax.transAxes, weight="bold", fontsize=11)
    ax.text(0.5, 0.96, "Analysis workflow", transform=ax.transAxes, ha="center", va="top", fontsize=9.5)
    ax.text(0.5, 0.05, f"Source: {prefix}_subject_summary.csv", transform=ax.transAxes, ha="center", fontsize=6.5, color=MUTED)
    return save(fig, reports_dir / f"{prefix}_methods_pipeline_schematic")


def robustness_degradation_plot(subj: pd.DataFrame, prefix: str, metric: str, reports_dir: Path) -> dict[str, str]:
    set_style(); pivot, summary = dropout_table(subj, metric)
    fig, ax = plt.subplots(figsize=(3.75, 3.05)); x = pivot.columns.to_numpy(float)
    for _, row in pivot.iterrows():
        ax.plot(x, row.to_numpy(float), color="#bdbdbd", lw=0.65, alpha=0.7, zorder=1)
    yerr = np.vstack([summary["mean"] - summary["ci_low"], summary["ci_high"] - summary["mean"]])
    yerr = np.where(np.isfinite(yerr), yerr, 0.0)
    ax.errorbar(summary["dropout_fraction"], summary["mean"], yerr=yerr, color=BLUE, marker="o", ms=3.6, lw=1.45, capsize=2.2, zorder=2)
    ax.set_xlabel("Channel dropout fraction"); ax.set_ylabel(metric_label(metric)); ax.set_title("Channel-dropout degradation")
    ax.set_ylim(0, 1.02); ax.set_xticks(x); ax.grid(axis="y", color="#dddddd", lw=0.45); ax.spines[["top", "right"]].set_visible(False)
    ax.text(0.0, 1.03, "B", transform=ax.transAxes, weight="bold", fontsize=11)
    ax.text(0.0, -0.25, f"Paired subjects, n={pivot.shape[0]}; mean ± 95% CI.", transform=ax.transAxes, fontsize=6.4, color=MUTED)
    return save(fig, reports_dir / f"{prefix}_methods_robustness_degradation_{metric}")


def intervention_class_plot(results_dir: Path, prefix: str, reports_dir: Path) -> dict[str, str]:
    set_style(); classes, source = load_intervention_classes(results_dir, prefix)
    require_columns(classes, {"subject", "intervention_class"}, source)
    counts = classes["intervention_class"].fillna("missing").value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(3.75, 3.05)); y = np.arange(len(counts))
    ax.barh(y, counts.values, height=0.52, color="#555555"); ax.set_yticks(y, labels=counts.index.astype(str)); ax.invert_yaxis()
    ax.set_xlabel("Subjects"); ax.set_title("Deployment-risk classes"); ax.grid(axis="x", color="#dddddd", lw=0.45); ax.set_axisbelow(True); ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, max(counts.values) + 1.2)
    for yi, value in zip(y, counts.values):
        ax.text(value + 0.06, yi, str(int(value)), va="center", ha="left", fontsize=7.5)
    ax.text(0.0, 1.03, "C", transform=ax.transAxes, weight="bold", fontsize=11)
    ax.text(0.0, -0.25, "Descriptive strata; not causal effects.", transform=ax.transAxes, fontsize=6.4, color=MUTED)
    return save(fig, reports_dir / f"{prefix}_methods_intervention_class_counts")


def generate_figures(results_dir: Path, reports_dir: Path, prefix: str, metric: str = "roc_auc") -> dict[str, object]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    subj = load_subject_summary(results_dir, prefix)
    class_source = results_dir / f"{prefix}_final_intervention_classes.csv"
    if not class_source.exists():
        class_source = results_dir / f"{prefix}_subject_risk_cards.csv"
    outputs = {
        "pipeline_schematic": pipeline_schematic(subj, prefix, reports_dir),
        "robustness_degradation": robustness_degradation_plot(subj, prefix, metric, reports_dir),
        "intervention_class_counts": intervention_class_plot(results_dir, prefix, reports_dir),
    }
    manifest = {"prefix": prefix, "metric": metric, "source_files": [str(results_dir / f"{prefix}_subject_summary.csv"), str(class_source)], "outputs": outputs, "style_note": "Restrained journal-style figures: white background, minimal color, direct data panels.", "note": "Figures are generated from existing repository CSV outputs only; no synthetic benchmark observations are used."}
    (reports_dir / f"{prefix}_methods_figures_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", type=Path, default=Path("results")); ap.add_argument("--reports-dir", type=Path, default=Path("reports")); ap.add_argument("--prefix", default=DEFAULT_PREFIX); ap.add_argument("--metric", default="roc_auc", choices=["roc_auc", "balanced_accuracy"])
    args = ap.parse_args(); print(json.dumps(generate_figures(args.results_dir, args.reports_dir, args.prefix, args.metric), indent=2))


if __name__ == "__main__":
    main()
