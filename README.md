# Assistance resilience review — data and analysis

This repository accompanies **Beyond AI-Assisted Performance: Assistance Resilience and Retained Human Capability in AI-Supported Education**. It contains the machine-readable review audit and the quantitative inputs/results used in the manuscript.

## Files
- `data/focal_screening.csv` — all 42 focal screening decisions.
- `data/focal_study_characteristics.csv` — extraction table for the 23 included reports.
- `data/focal_excluded_reports.csv` — exclusion audit for 19 reports.
- `data/design_feature_counts.csv` — descriptive design-feature coverage counts.
- `data/architecture_effects.csv` — 20 first independent/AI-off standardized contrasts.
- `data/delayed_retention_effects.csv` — five delayed independent retention contrasts.
- `data/paired_ai_on_off.csv` — eight descriptive AI-on / AI-off arm-level pairs.
- `data/meta_results.csv` — REML random-effects results with modified Hartung-Knapp confidence intervals and prediction intervals.
- `data/delayed_leave_one_out.csv` — delayed-retention leave-one-out diagnostics.
- `analysis/meta_analysis.py` — script implementing the quantitative synthesis.
- `PROTOCOL_FOCAL_CORE.md` and `PROTOCOL_QUANTITATIVE_SYNTHESIS.md` — operational eligibility and analysis rules.
- `ATLAS_SOURCE.md` — immutable upstream source identifiers for the external standardized-effect resource.

The manuscript treats the architecture models as external quantitative triangulations rather than a formal open-versus-structured subgroup test because some multi-arm trials share controls across architecture categories.
