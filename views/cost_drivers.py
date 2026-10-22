"""What drives medical costs? Cost driver EDA on the filtered population."""

import streamlit as st

from src.charts import boxplot, correlation_heatmap, histogram, scatter_vs_charges
from src.insights import cost_drivers_insight
from src.metrics import group_stats
from src.model import encode_features
from views.components import render_insight, render_kpi_row


def render() -> None:
    filtered_df = st.session_state["filtered_df"]

    st.title("What drives medical costs?")
    render_kpi_row(filtered_df)

    st.plotly_chart(histogram(filtered_df, "charges"), width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(boxplot(filtered_df, "smoker"), width="stretch")
        st.plotly_chart(boxplot(filtered_df, "region"), width="stretch")
    with col2:
        st.plotly_chart(boxplot(filtered_df, "sex"), width="stretch")
        st.plotly_chart(boxplot(filtered_df, "children"), width="stretch")

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(scatter_vs_charges(filtered_df, "age"), width="stretch")
    with col4:
        st.plotly_chart(scatter_vs_charges(filtered_df, "bmi"), width="stretch")

    st.plotly_chart(correlation_heatmap(encode_features(filtered_df)), width="stretch")

    st.subheader("Group Statistics")
    group_col = st.selectbox("Group by", ["sex", "smoker", "region"], key="group_stats_col")
    st.dataframe(group_stats(filtered_df, group_col).style.format("{:,.2f}"))

    render_insight(cost_drivers_insight(filtered_df))
