# Prompt Log

### 1. Implementation plan for Streamlit MVP
**Prompt:**
Role: You are a senior BI developer and a python data engineer who builds clean, modular, production-style analytical apps with Streamlit, Pandas, Plotly and scikit-learn.
Context: I'm building an end-to-end data analytics and reporting MVP for a health insurance dataset. The audience is business stakeholders (care management and finance) who need to understand what drives medical costs and which members are high risk. I already analyzed this data in a Jupyter notebook (see Input). This project turns that analysis into a modular, interactive Streamlit application.
Environment: Python 3.12 managed with uv. Run all commands with `uv run`. Packages already installed: streamlit, pandas, plotly, scikit-learn.
Input:
1. Reference Notebook: @notebook/HighRiskPrediction_Insurance.ipynb
- source of truth for the data cleaning steps, EDA charts, preprocessing and model setup.
- Ignore the Google Colab and Drive-specific code (drive.mount and the /content/drive path).
2. Dataset: data/insurance.csv
	- age (int), sex (male/female), bmi (float), children (int), smoker (yes/no), region (northeast/northwest/southeast/southwest), charges (float, individual medical costs billed by health insurance)
Task: Propose an implementation plan for converting my notebook analysis into a modular Streamlit application. Do NOT write any code yet. I will review and approve the plan first.
Required output:
Respond with these sections, in this order:
1.	Project Structure: a folder tree showing src/data_loader.py, src/quality.py, src/metrics.py, src/charts.py, src/model.py and app.py
2.	Module Responsibilities: for each module, a table with function name | purpose | inputs | outputs
3.	 High-risk member definition: propose a definition, explain the business reasoning, and show which parameters will be configurable.
4.	Dashboard layout: sidebar filters, the KPI row, and each tab with the charts or tables it contains. Include a Data Quality tab, a High-Risk Members tab with CSV export, and a Cost Estimator tab using the model.
5.	Validation plan: how we will confirm the results match my notebook (row counts, duplicates, R², MAE)
6.	Build order: the step-by-step order to implement and test each module.
7.	Open questions: anything you need me to decide before building.
Constraints:
- Keep business logic in src/ modules; app.py should only handle layout and UI.
- Every module must be runnable on its own with an `if __name__ == "__main__":` test
- Never hardcode results, counts or metrics. Everything must be computed from the data at runtime so it can be validated against the notebook.
- KPIs, charts and tables must respond to the sidebar filters, except:
  the Data Quality tab always describes the full dataset, and the model is always
  trained on the full cleaned dataset
- Use Plotly for all charts so they are interactive
- Follow the prompt-logging rules in CLAUDE.md. Create prompts.md now and log this
  planning prompt as entry #1. This is the only file you should create at this stage.
- Use st.cache_data / st.cache_resource for data loading and model training.
- Keep it an MVP: clear and working over feature-heavy.

**Output summary:**
- Reviewed the notebook and raw CSV directly (confirmed 1338 raw rows, 1 exact duplicate at age=19/male/bmi=30.59/northwest, 0 nulls) to ground the plan in actual data rather than assumptions.
- Proposed a 6-module structure (data_loader, quality, metrics, charts, model + app.py) with a function-level responsibility table for each.
- Proposed a configurable risk-factor-count definition for "High Risk" (smoker, BMI≥30, age≥50, charges≥75th percentile; flagged at ≥2 factors), reasoned from the notebook's own regression weights and EDA.
- Proposed sidebar filters, a 5-metric KPI row, and four tabs (Cost Drivers, Data Quality, High-Risk Members with CSV export, Cost Estimator), a validation plan tied to notebook-reproducible numbers (row counts, dedup, describe() stats, R²≈0.8069, MAE≈$4177.05), a build order, and open questions on risk thresholds, estimator input defaults, and number formatting.

**Files created/changed:**
- prompts.md (created)

**My review:**
_(to be filled in by me)_

### 2. Build the MVP per the approved plan
**Prompt:**
7. Open Questions
Does the risk-factor-count definition (§3) match your intent, or did you have a specific cutoff (e.g. "top 10% of charges") in mind already? Yes, they match the intent.
Are the default thresholds (BMI 30, age 50, 75th percentile, min 2 factors) reasonable starting points, or do you want different defaults? Yes, they are reasonable.
For the Cost Estimator inputs, should sliders/dropdowns default to dataset medians/modes, or start blank? Yes, default it to dataset medians/modes,
Any preference on currency/number formatting (e.g. $13,279 vs 13279.12) across KPIs and tables? $13,279  this format is good.

**Output summary:**
- Built all 5 src/ modules per the approved build order (data_loader, quality, model, metrics, charts) plus app.py, each validated against the notebook's numbers via its own `if __name__ == "__main__":` block: 1338→1337 row dedup, 0 nulls, identical duplicate row, matching describe()/group-by stats, R²=0.8069 and MAE=$4177.05 with matching coefficients.
- Implemented the configurable risk-factor-count high-risk definition (smoker / BMI≥30 / age≥50 / charges≥75th pct, flagged at ≥2 factors) with live sliders in the High-Risk Members tab.
- Built app.py with sidebar filters, a 5-metric KPI row, and all four tabs (Cost Drivers, Data Quality, High-Risk Members with CSV export, Cost Estimator with median/mode-defaulted inputs); Data Quality tab and model training correctly bypass sidebar filters as required.
- Applied the dataviz skill's fixed categorical color mapping (no auto-cycled colors) and diverging color for the correlation heatmap and coefficient chart; verified the full app end-to-end with Streamlit's `AppTest` harness (no exceptions across all 4 tabs) and confirmed live reactivity: sidebar filters reshape KPIs, risk-threshold sliders change the flagged count, and the Cost Estimator's prediction responds correctly to input changes.
- Fixed a `use_container_width` deprecation (installed Streamlit version requires `width="stretch"`) and removed an unused `pandas` import surfaced during verification.

**Files created/changed:**
- app.py (created)
- src/__init__.py (created)
- src/data_loader.py (created)
- src/quality.py (created)
- src/model.py (created)
- src/metrics.py (created)
- src/charts.py (created)

**My review:**
_(to be filled in by me)_
