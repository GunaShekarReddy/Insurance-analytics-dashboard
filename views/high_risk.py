"""Who is high risk? Configurable risk flagging with CSV export."""

import streamlit as st

from src.charts import risk_factor_breakdown
from src.insights import high_risk_insight
from src.metrics import (
    DEFAULT_AGE_THRESHOLD,
    DEFAULT_BMI_THRESHOLD,
    DEFAULT_CHARGES_PERCENTILE,
    DEFAULT_MIN_FACTORS,
    flag_high_risk,
    high_risk_summary,
)
from views.components import render_insight, render_kpi_row


def render() -> None:
    filtered_df = st.session_state["filtered_df"]

    st.title("Who is high risk?")
    render_kpi_row(filtered_df)

    st.caption("Tune the high-risk definition below. Table respects sidebar filters.")

    r1, r2, r3, r4 = st.columns(4)
    bmi_threshold = r1.slider(
        "BMI threshold", 15.0, 55.0, float(DEFAULT_BMI_THRESHOLD), key="risk_bmi_threshold"
    )
    age_threshold = r2.slider(
        "Age threshold", 18, 64, DEFAULT_AGE_THRESHOLD, key="risk_age_threshold"
    )
    charges_percentile = r3.slider(
        "Charges percentile", 50, 99, DEFAULT_CHARGES_PERCENTILE, key="risk_charges_percentile"
    )
    min_factors = r4.slider(
        "Min factors required", 1, 4, DEFAULT_MIN_FACTORS, key="risk_min_factors"
    )

    flagged_df = flag_high_risk(
        filtered_df,
        bmi_threshold=bmi_threshold,
        age_threshold=age_threshold,
        charges_percentile=charges_percentile,
        min_factors=min_factors,
    )
    risk_summary = high_risk_summary(flagged_df)

    rc1, rc2 = st.columns(2)
    rc1.metric("High-Risk Members", f"{risk_summary['high_risk_count']:,}")
    rc2.metric("High-Risk %", f"{risk_summary['high_risk_pct']:.1f}%")

    breakdown_col = st.selectbox(
        "Breakdown by", ["region", "smoker", "sex"], key="risk_breakdown_col"
    )
    st.plotly_chart(risk_factor_breakdown(flagged_df, breakdown_col), width="stretch")

    high_risk_only = flagged_df[flagged_df["is_high_risk"]]
    st.subheader(f"High-Risk Member Table ({len(high_risk_only):,})")
    st.dataframe(high_risk_only)

    st.download_button(
        "Download High-Risk Members (CSV)",
        data=high_risk_only.to_csv(index=False).encode("utf-8"),
        file_name="high_risk_members.csv",
        mime="text/csv",
    )

    render_insight(high_risk_insight(flagged_df))
