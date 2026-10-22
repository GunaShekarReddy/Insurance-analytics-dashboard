"""Who are our members? Univariate EDA on the filtered population."""

import streamlit as st

from src.charts import count_plot, distribution_boxplot, histogram
from src.insights import members_insight
from views.components import render_insight, render_kpi_row

NUMERIC_COLUMNS = ["age", "bmi", "children", "charges"]


def render() -> None:
    filtered_df = st.session_state["filtered_df"]

    st.title("Who are our members?")
    render_kpi_row(filtered_df)

    st.subheader("Numeric Distributions")
    numeric_col = st.selectbox("Numeric column", NUMERIC_COLUMNS, key="members_numeric_col")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(histogram(filtered_df, numeric_col), width="stretch")
    with col2:
        st.plotly_chart(distribution_boxplot(filtered_df, numeric_col), width="stretch")

    st.subheader("Categorical Counts")
    cat1, cat2, cat3 = st.columns(3)
    with cat1:
        st.plotly_chart(count_plot(filtered_df, "sex"), width="stretch")
    with cat2:
        st.plotly_chart(count_plot(filtered_df, "smoker"), width="stretch")
    with cat3:
        st.plotly_chart(count_plot(filtered_df, "region"), width="stretch")

    render_insight(members_insight(filtered_df, numeric_col))
