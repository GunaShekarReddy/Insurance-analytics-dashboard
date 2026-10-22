"""What will a member cost? Model is always trained on the full cleaned dataset."""

import streamlit as st

from src.charts import actual_vs_predicted, coefficient_chart
from src.insights import cost_estimator_insight
from src.model import predict_charges, train_model
from views.components import render_insight, render_kpi_row


def render() -> None:
    filtered_df = st.session_state["filtered_df"]
    clean_df = st.session_state["clean_df"]

    st.title("What will a member cost?")
    render_kpi_row(filtered_df)

    st.caption("Model is trained on the full cleaned dataset, independent of sidebar filters.")

    model_result = train_model(clean_df)

    mc1, mc2 = st.columns(2)
    mc1.metric("Model R-squared", f"{model_result['r2']:.3f}")
    mc2.metric("Model MAE", f"${model_result['mae']:,.0f}")

    st.subheader("Estimate Charges for a Member")

    age_min, age_max = int(clean_df["age"].min()), int(clean_df["age"].max())
    bmi_min, bmi_max = float(clean_df["bmi"].min()), float(clean_df["bmi"].max())
    sex_options = sorted(clean_df["sex"].unique())
    children_options = sorted(clean_df["children"].unique())
    smoker_options = sorted(clean_df["smoker"].unique())
    region_options = sorted(clean_df["region"].unique())

    e1, e2, e3 = st.columns(3)
    with e1:
        est_age = st.slider(
            "Age", age_min, age_max, int(clean_df["age"].median()), key="estimator_age"
        )
        est_sex = st.selectbox(
            "Sex",
            sex_options,
            index=sex_options.index(clean_df["sex"].mode()[0]),
            key="estimator_sex",
        )
    with e2:
        est_bmi = st.slider(
            "BMI", bmi_min, bmi_max, float(clean_df["bmi"].median()), key="estimator_bmi"
        )
        est_children = st.selectbox(
            "Children",
            children_options,
            index=children_options.index(int(clean_df["children"].mode()[0])),
            key="estimator_children",
        )
    with e3:
        est_smoker = st.selectbox(
            "Smoker",
            smoker_options,
            index=smoker_options.index(clean_df["smoker"].mode()[0]),
            key="estimator_smoker",
        )
        est_region = st.selectbox(
            "Region",
            region_options,
            index=region_options.index(clean_df["region"].mode()[0]),
            key="estimator_region",
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
    st.metric("Estimated Charges", f"${predicted:,.0f}")

    st.plotly_chart(coefficient_chart(model_result["coefficients"]), width="stretch")
    st.plotly_chart(
        actual_vs_predicted(model_result["y_test"], model_result["predictions"]),
        width="stretch",
    )

    render_insight(cost_estimator_insight(filtered_df, predicted))
