# Insurance Cost & Risk Analytics Dashboard

An interactive Streamlit dashboard built on a health insurance dataset, turning an
exploratory Jupyter notebook analysis into a modular, multi-page analytics tool for
two business audiences:

- **Care management** — who is likely to be high-cost or high-risk, and why.
- **Finance** — what drives medical costs across the member population.

## Pages

The app is a multi-page storytelling dashboard (`st.navigation` / `st.Page`):

1. **Overview** — purpose, audience, the business questions answered, and how to use the filters.
2. **Data Quality** — "Can we trust this data?" Always describes the full dataset, independent of filters.
3. **Who are our members?** — univariate EDA: histogram + boxplot for a selected numeric column, count plots for sex/smoker/region.
4. **What drives medical costs?** — bivariate cost-driver EDA: distributions, boxplots, scatter plots, correlation heatmap, group statistics.
5. **Who is high risk?** — a configurable, risk-factor-count high-risk definition with a flagged member table and CSV export.
6. **What will a member cost?** — a linear regression cost estimator (model always trained on the full cleaned dataset).

Pages 3–6 share a structure: the business question as the title, a KPI row, charts,
then a short written insight and a "So what" line — all computed from the filtered
data at runtime.

## Project structure

```
app.py                  # Multi-page entrypoint: page config, sidebar filters, st.navigation
app_v1_tabs.py           # Frozen v1 snapshot (single-page tabbed layout) — not maintained
src/
  data_loader.py         # Load + clean the raw CSV
  quality.py              # Null/duplicate/dtype/profile checks for the Data Quality page
  metrics.py              # KPI summary + configurable high-risk flagging
  model.py                 # Feature encoding, LinearRegression training, prediction
  charts.py                # Plotly chart builders
  insights.py               # Runtime-computed insight + "so what" text per page
views/
  components.py            # Shared UI: sidebar filters, KPI row, insight renderer
  overview.py, data_quality.py, members.py,
  cost_drivers.py, high_risk.py, cost_estimator.py   # One module per page
data/insurance.csv        # Source dataset
notebook/HighRiskPrediction_Insurance.ipynb   # Original EDA/model notebook (source of truth)
prompts.md                 # Prompt log for this project
```

Business logic lives entirely in `src/`; `app.py` and `views/` handle layout and UI
only. Every `src/` module is runnable standalone (`if __name__ == "__main__":`) and
prints values that can be checked against the reference notebook.

## Data

`data/insurance.csv` — 1,338 raw rows (1,337 after removing one exact duplicate):

| Column | Type | Description |
|---|---|---|
| age | int | Age of the primary beneficiary |
| sex | male / female | Gender |
| bmi | float | Body mass index |
| children | int | Number of dependents covered |
| smoker | yes / no | Smoking status |
| region | northeast / northwest / southeast / southwest | Residential region |
| charges | float | Individual medical costs billed by health insurance |

## Model

A `LinearRegression` model (scikit-learn) trained on the full cleaned dataset with
an 80/20 train-test split (`random_state=42`), encoding `sex`/`smoker` as 0/1 and
one-hot encoding `region`. Achieves R² ≈ 0.81 and MAE ≈ $4,177 on the held-out test
set, matching the reference notebook.

## Running it

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv run streamlit run app.py
```

To run an individual module's self-test (useful for validating against the notebook):

```bash
uv run python src/model.py
```

## Environment

- Python 3.12, managed with `uv`
- Add packages with `uv add <package>` — never `pip`
- Key dependencies: `streamlit`, `pandas`, `plotly`, `scikit-learn`
