# Insurance Cost & Risk Analytics Dashboard

## Project overview
End-to-end data analytics and reporting MVP built in Streamlit for a health insurance
dataset. Audience: business stakeholders (care management and finance) who need to
understand what drives medical costs and which members are high risk.
This project converts an existing Jupyter notebook analysis into a modular,
interactive Streamlit application.

## Environment
- Python 3.12, managed with uv
- Run every command with `uv run` (e.g. `uv run python src/quality.py`,
  `uv run streamlit run app.py`)
- Add packages with `uv add <package>`, never pip
- Installed: streamlit, pandas, plotly, scikit-learn

## Data
- Dataset: data/insurance.csv
- Columns: age (int), sex (male/female), bmi (float), children (int), smoker (yes/no),
  region (northeast/northwest/southeast/southwest),
  charges (float, individual medical costs billed by health insurance)
- Reference notebook: notebook/HighRiskPrediction_Insurance.ipynb
  (source of truth for cleaning, EDA, preprocessing and model setup;
  ignore its Google Colab/Drive code)

## Project structure
To be added once the implementation plan is approved.

## Coding standards
- Business logic lives in src/ modules; app.py handles layout and UI only
- Every module is runnable on its own with an `if __name__ == "__main__":` test
- Never hardcode results, counts or metrics; compute everything from the data at runtime
- Use Plotly for all charts
- Use st.cache_data / st.cache_resource for data loading and model training
- MVP mindset: clear and working over feature-heavy

## Prompt log
Maintain prompts.md in the project root throughout this project.
After completing each task prompt I give you, append an entry in this format:

### <number>. <short title>
**Prompt:**
<my prompt, copied verbatim>

**Output summary:**
<2–4 bullets: what you produced or decided>

**Files created/changed:**
<list of files, or "none">

**My review:**
_(to be filled in by me)_

Rules:
- Never fill in or edit the "My review" lines. Those are mine.
- Never rewrite or delete earlier entries; only append.
- Do not log purely conversational questions, only task prompts.
- Updating prompts.md is always allowed, even when a task says not to change other files.