"""Overview page: what this dashboard is for, who it's for, and how to use it."""

import streamlit as st


def render() -> None:
    clean_df = st.session_state["clean_df"]

    st.title("Insurance Cost & Risk Analytics Dashboard")

    st.markdown(
        f"""
This dashboard analyzes **{len(clean_df):,} health insurance members** to help two
audiences do their jobs:

- **Care management** — who is likely to be high-cost or high-risk, and why.
- **Finance** — what drives medical costs across the member population.

### Business questions this dashboard answers
- **Data Quality** — Can we trust this data?
- **Who are our members?** — What does the member population look like?
- **What drives medical costs?** — Which factors move charges the most?
- **Who is high risk?** — Which members should care management prioritize?
- **What will a member cost?** — What should we expect a given member to cost?

### How to use the filters
Use the sidebar on the left to narrow the population by age, BMI, sex, region,
smoker status, and number of children. The KPI row, charts, and tables on
**Who are our members?**, **What drives medical costs?**, **Who is high risk?**,
and **What will a member cost?** all respond live to these filters.

**Data Quality** always describes the full dataset, and the cost model behind
**What will a member cost?** is always trained on the full cleaned dataset — both
stay stable reference points no matter how you filter.
"""
    )
