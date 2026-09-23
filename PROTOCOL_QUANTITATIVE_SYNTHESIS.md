# Secondary quantitative analysis

This document describes the selected contrasts and estimators used for the supplementary quantitative analysis. The selection is an illustrative secondary analysis, separate from the 23-report focal synthesis. The 20 architecture contrasts, five delayed contrasts and eight descriptive pairs do not constitute a census of all eligible estimates in the source dataset.

## Source records and inputs

The external data snapshot and its identifiers are recorded in `ATLAS_SOURCE.md`. The analysis CSVs identify selected source records by estimate ID; `data/atlas_selected_estimates.json` preserves their unrounded values. Standardised effects and standard errors in the analysis CSVs are rounded to three decimal places.

## Architecture contrasts

`data/architecture_effects.csv` contains ten open or unguided and ten structured or scaffolded first independent/AI-off contrasts. Estimate separate models for these two selected sets. Some multi-arm studies share controls across sets, so the two estimates are descriptive summaries rather than an independent-groups test of architecture. Architecture labels are not randomised moderators.

## Delayed independent performance

`data/delayed_retention_effects.csv` contains five selected delayed contrasts: Contractor and Reyes (2026), Barcaui (2025), Kazemitabaar et al. (2023), Kalam et al. (2025), and Kreijkes et al. (2026). Report the full set, plus separate sensitivity analyses excluding Kreijkes (active note-taking comparator) and Barcaui (standard error reconstructed from a confidence interval). `data/delayed_leave_one_out.csv` reports all single-study omissions. These exploratory checks do not replace the full-set summary.

## Estimator

Estimate between-study variance by restricted maximum likelihood (REML), including the intercept-estimation term in its score equation. Use modified Hartung–Knapp variance bounded below by the conventional random-effects variance and a t distribution with k − 1 degrees of freedom for 95% confidence intervals. Approximate 95% prediction intervals use the same critical value and the square root of τ² plus the estimated variance of the mean; intervals with few studies are especially uncertain. Compute Cochran Q using fixed inverse-variance weights and I² = max(0, (Q − k + 1)/Q).

## Descriptive assistance pairs

`data/paired_ai_on_off.csv` contains eight same-arm descriptive AI-on/AI-off pairs. The outcomes may differ in timing and scale; do not interpret their differences as pooled treatment effects, within-person causal decrements, or correlations. No significance test is specified for these pairs.

## Reproduction

From the repository root:

```bash
python analysis/meta_analysis.py
python analysis/tests/test_reml.py
```

Dependencies: Python 3, numpy, pandas, scipy. The script uses local inputs and does not require network access.
