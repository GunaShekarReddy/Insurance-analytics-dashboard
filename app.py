"""Insurance Cost & Risk Analytics Dashboard. Layout and UI only; logic lives in src/."""

import streamlit as st

from src.charts import (
    actual_vs_predicted,
    boxplot,
    coefficient_chart,
    correlation_heatmap,
    histogram,
    risk_factor_breakdown,
    scatter_vs_charges,
)
from src.data_loader import get_clean_data, load_raw_data
from src.metrics import (
    DEFAULT_AGE_THRESHOLD,
    DEFAULT_BMI_THRESHOLD,
    DEFAULT_CHARGES_PERCENTILE,
    DEFAULT_MIN_FACTORS,
    flag_high_risk,
    group_stats,
    high_risk_summary,
    kpi_summary,
)
from src.model import encode_features, predict_charges, train_model
from src.quality import (
    categorical_profile,
    duplicate_summary,
    dtype_summary,
    null_summary,
    numeric_profile,
)

st.set_page_config(page_title="Insurance Cost & Risk Analytics", layout="wide")

raw_df = load_raw_data()
clean_df = get_clean_data()

st.title("Insurance Cost & Risk Analytics Dashboard")

# --- Sidebar filters ---
st.sidebar.header("Filters")

age_min, age_max = int(clean_df["age"].min()), int(clean_df["age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

bmi_min, bmi_max = float(clean_df["bmi"].min()), float(clean_df["bmi"].max())
bmi_range = st.sidebar.slider("BMI range", bmi_min, bmi_max, (bmi_min, bmi_max))

sex_options = sorted(clean_df["sex"].unique())
selected_sex = st.sidebar.multiselect("Sex", sex_options, default=sex_options)

region_options = sorted(clean_df["region"].unique())
selected_region = st.sidebar.multiselect("Region", region_options, default=region_options)

smoker_options = sorted(clean_df["smoker"].unique())
selected_smoker = st.sidebar.multiselect("Smoker", smoker_options, default=smoker_options)

children_options = sorted(clean_df["children"].unique())
selected_children = st.sidebar.multiselect(
    "Children", children_options, default=children_options
)

filtered_df = clean_df[
    clean_df["age"].between(*age_range)
    & clean_df["bmi"].between(*bmi_range)
    & clean_df["sex"].isin(selected_sex)
    & clean_df["region"].isin(selected_region)
    & clean_df["smoker"].isin(selected_smoker)
    & clean_df["children"].isin(selected_children)
]

if filtered_df.empty:
    st.warning("No members match the current filters. Adjust the sidebar filters.")
    st.stop()

# --- KPI row ---
kpis = kpi_summary(filtered_df)
risk_preview = high_risk_summary(flag_high_risk(filtered_df))

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Members", f"{kpis['member_count']:,}")
k2.metric("Average Charges", f"${kpis['avg_charges']:,.0f}")
k3.metric("Average BMI", f"{kpis['avg_bmi']:.1f}")
k4.metric("Smoker %", f"{kpis['smoker_pct']:.1f}%")
k5.metric("High-Risk %", f"{risk_preview['high_risk_pct']:.1f}%")

tab_overview, tab_quality, tab_risk, tab_estimator = st.tabs(
    ["Cost Drivers", "Data Quality", "High-Risk Members", "Cost Estimator"]
)

# --- Tab 1: Cost Drivers ---
with tab_overview:
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

    st.plotly_chart(
        correlation_heatmap(encode_features(filtered_df)), width="stretch"
    )

    st.subheader("Group Statistics")
    group_col = st.selectbox("Group by", ["sex", "smoker", "region"], key="group_stats_col")
    st.dataframe(group_stats(filtered_df, group_col).style.format("{:,.2f}"))

# --- Tab 2: Data Quality (always full raw dataset, ignores filters) ---
with tab_quality:
    st.caption("This tab always describes the full dataset, independent of sidebar filters.")

    dup_count, dup_rows = duplicate_summary(raw_df)
    c1, c2 = st.columns(2)
    c1.metric("Raw Rows", f"{len(raw_df):,}")
    c2.metric("Rows After Dedup", f"{len(clean_df):,}", delta=f"-{dup_count}")

    st.subheader("Null Values")
    st.dataframe(null_summary(raw_df).rename("null_count"))

    st.subheader(f"Duplicate Rows ({dup_count})")
    st.dataframe(dup_rows)

    st.subheader("Column Types")
    st.dataframe(dtype_summary(raw_df))

    st.subheader("Numeric Profile")
    st.dataframe(numeric_profile(clean_df).style.format("{:,.2f}"))

    st.subheader("Categorical Profile")
    for col, counts in categorical_profile(raw_df).items():
        st.write(f"**{col}**")
        st.dataframe(counts)

# --- Tab 3: High-Risk Members ---
with tab_risk:
    st.caption("Tune the high-risk definition below. Table respects sidebar filters.")

    r1, r2, r3, r4 = st.columns(4)
    bmi_threshold = r1.slider("BMI threshold", 15.0, 55.0, float(DEFAULT_BMI_THRESHOLD))
    age_threshold = r2.slider("Age threshold", 18, 64, DEFAULT_AGE_THRESHOLD)
    charges_percentile = r3.slider(
        "Charges percentile", 50, 99, DEFAULT_CHARGES_PERCENTILE
    )
    min_factors = r4.slider("Min factors required", 1, 4, DEFAULT_MIN_FACTORS)

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

    breakdown_col = st.selectbox("Breakdown by", ["region", "smoker", "sex"], key="risk_breakdown_col")
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

# --- Tab 4: Cost Estimator (model always trained on full cleaned dataset) ---
with tab_estimator:
    st.caption("Model is trained on the full cleaned dataset, independent of sidebar filters.")

    model_result = train_model(clean_df)

    mc1, mc2 = st.columns(2)
    mc1.metric("Model R-squared", f"{model_result['r2']:.3f}")
    mc2.metric("Model MAE", f"${model_result['mae']:,.0f}")

    st.subheader("Estimate Charges for a Member")
    e1, e2, e3 = st.columns(3)
    with e1:
        est_age = st.slider("Age", age_min, age_max, int(clean_df["age"].median()))
        est_sex = st.selectbox("Sex", sex_options, index=sex_options.index(clean_df["sex"].mode()[0]))
    with e2:
        est_bmi = st.slider("BMI", bmi_min, bmi_max, float(clean_df["bmi"].median()))
        est_children = st.selectbox(
            "Children",
            children_options,
            index=children_options.index(int(clean_df["children"].mode()[0])),
        )
    with e3:
        est_smoker = st.selectbox(
            "Smoker", smoker_options, index=smoker_options.index(clean_df["smoker"].mode()[0])
        )
        est_region = st.selectbox(
            "Region", region_options, index=region_options.index(clean_df["region"].mode()[0])
        )

    predicted = predict_charges(
        model_result["model"],
        model_result["feature_columns"],
        age=est_age,
        sex=est_sex,
        bmi=est_bmi,
        children=est_children,
        smoker=est_smoker,
        region=est_region,
    )
    st.metric("Estimated Annual Charges", f"${predicted:,.0f}")

    st.plotly_chart(coefficient_chart(model_result["coefficients"]), width="stretch")
    st.plotly_chart(
        actual_vs_predicted(model_result["y_test"], model_result["predictions"]),
        width="stretch",
    )
