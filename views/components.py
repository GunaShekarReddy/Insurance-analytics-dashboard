"""Shared UI building blocks used across the storytelling pages. UI only; no business logic."""

import pandas as pd
import streamlit as st

from src.metrics import flag_high_risk, high_risk_summary, kpi_summary


def render_sidebar_filters(clean_df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")

    age_min, age_max = int(clean_df["age"].min()), int(clean_df["age"].max())
    age_range = st.sidebar.slider(
        "Age range", age_min, age_max, (age_min, age_max), key="filter_age_range"
    )

    bmi_min, bmi_max = float(clean_df["bmi"].min()), float(clean_df["bmi"].max())
    bmi_range = st.sidebar.slider(
        "BMI range", bmi_min, bmi_max, (bmi_min, bmi_max), key="filter_bmi_range"
    )

    sex_options = sorted(clean_df["sex"].unique())
    selected_sex = st.sidebar.multiselect(
        "Sex", sex_options, default=sex_options, key="filter_sex"
    )

    region_options = sorted(clean_df["region"].unique())
    selected_region = st.sidebar.multiselect(
        "Region", region_options, default=region_options, key="filter_region"
    )

    smoker_options = sorted(clean_df["smoker"].unique())
    selected_smoker = st.sidebar.multiselect(
        "Smoker", smoker_options, default=smoker_options, key="filter_smoker"
    )

    children_options = sorted(clean_df["children"].unique())
    selected_children = st.sidebar.multiselect(
        "Children", children_options, default=children_options, key="filter_children"
    )

    return clean_df[
        clean_df["age"].between(*age_range)
        & clean_df["bmi"].between(*bmi_range)
        & clean_df["sex"].isin(selected_sex)
        & clean_df["region"].isin(selected_region)
        & clean_df["smoker"].isin(selected_smoker)
        & clean_df["children"].isin(selected_children)
    ]


def render_kpi_row(filtered_df: pd.DataFrame) -> None:
    kpis = kpi_summary(filtered_df)
    risk_preview = high_risk_summary(flag_high_risk(filtered_df))

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Members", f"{kpis['member_count']:,}")
    k2.metric("Average Charges", f"${kpis['avg_charges']:,.0f}")
    k3.metric("Average BMI", f"{kpis['avg_bmi']:.1f}")
    k4.metric("Smoker %", f"{kpis['smoker_pct']:.1f}%")
    k5.metric("High-Risk %", f"{risk_preview['high_risk_pct']:.1f}%")


def render_insight(insight: dict) -> None:
    st.markdown(f"**Insight:** {insight['insight']}")
    st.markdown(f"**So what:** {insight['so_what']}")
