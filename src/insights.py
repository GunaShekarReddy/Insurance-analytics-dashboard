"""Runtime-computed insight text for the storytelling pages. No hardcoded numbers."""

import pandas as pd


def members_insight(df: pd.DataFrame, numeric_col: str) -> dict:
    mean = df[numeric_col].mean()
    median = df[numeric_col].median()
    if median and mean > median * 1.05:
        skew_word = "right-skewed (a few high values pull the average up)"
    elif median and mean < median * 0.95:
        skew_word = "left-skewed"
    else:
        skew_word = "roughly symmetric"

    smoker_pct = (df["smoker"] == "yes").mean() * 100
    region_counts = df["region"].value_counts(normalize=True)
    dominant_region = region_counts.idxmax()
    dominant_region_pct = region_counts.max() * 100

    insight = (
        f"For the filtered population, {numeric_col} has a mean of {mean:,.1f} versus a "
        f"median of {median:,.1f} ({skew_word}). {smoker_pct:.1f}% are smokers, and the "
        f"largest region segment is {dominant_region} ({dominant_region_pct:.1f}% of members)."
    )
    if "symmetric" in skew_word:
        so_what = (
            "A balanced distribution means the average is a reasonable summary here — "
            "use it as a stable baseline when comparing against the High-Risk Members page."
        )
    else:
        so_what = (
            "A skewed distribution means the average alone can mislead planning — pair this "
            "view with the High-Risk Members page rather than relying on the mean in isolation."
        )
    return {"insight": insight, "so_what": so_what}


def cost_drivers_insight(df: pd.DataFrame) -> dict:
    by_smoker = df.groupby("smoker")["charges"].mean()

    if {"yes", "no"}.issubset(by_smoker.index) and by_smoker["no"] > 0:
        ratio = by_smoker["yes"] / by_smoker["no"]
        insight = (
            f"Smokers in the filtered population average ${by_smoker['yes']:,.0f} in charges "
            f"versus ${by_smoker['no']:,.0f} for non-smokers — about {ratio:.1f}x higher."
        )
        so_what = (
            "Smoking status is the single largest lever on cost here; cessation outreach has "
            "the clearest payoff for finance and care management alike."
        )
    else:
        only_group = by_smoker.index[0]
        label = "smokers" if only_group == "yes" else "non-smokers"
        insight = (
            f"Every member in the current filter is a {label.rstrip('s')}, averaging "
            f"${by_smoker.iloc[0]:,.0f} in charges."
        )
        so_what = "Widen the Smoker filter in the sidebar to compare cost drivers across both groups."

    return {"insight": insight, "so_what": so_what}


def high_risk_insight(df_flagged: pd.DataFrame) -> dict:
    total = len(df_flagged)
    high_risk = df_flagged[df_flagged["is_high_risk"]]
    count = len(high_risk)
    pct = (count / total * 100) if total else 0.0

    if count:
        factor_cols = ["factor_smoker", "factor_bmi", "factor_age", "factor_charges"]
        factor_rates = high_risk[factor_cols].mean().sort_values(ascending=False)
        top_factor = factor_rates.index[0].replace("factor_", "")
        top_factor_pct = factor_rates.iloc[0] * 100
        insight = (
            f"{count:,} of {total:,} filtered members ({pct:.1f}%) are flagged high-risk. "
            f"Among them, {top_factor_pct:.0f}% are flagged for {top_factor}, the most common driver."
        )
        so_what = f"Care management outreach targeting {top_factor} would reach the largest share of this group."
    else:
        insight = f"None of the {total:,} filtered members meet the current high-risk thresholds."
        so_what = "Loosen the thresholds above, or widen the sidebar filters, to surface a risk cohort."

    return {"insight": insight, "so_what": so_what}


def cost_estimator_insight(filtered_df: pd.DataFrame, predicted: float) -> dict:
    avg_charges = filtered_df["charges"].mean()
    diff = predicted - avg_charges
    pct = (diff / avg_charges * 100) if avg_charges else 0.0
    direction = "above" if diff >= 0 else "below"

    insight = (
        f"This estimate of ${predicted:,.0f} is ${abs(diff):,.0f} ({abs(pct):.0f}%) {direction} "
        f"the ${avg_charges:,.0f} average charges of the currently filtered population."
    )
    so_what = (
        "Use this gap to flag members whose expected cost sits well above their peer group "
        "for proactive case management."
    )
    return {"insight": insight, "so_what": so_what}


if __name__ == "__main__":
    from data_loader import get_clean_data
    from metrics import flag_high_risk
    from model import predict_charges, train_model

    clean = get_clean_data()

    print("--- members_insight ---")
    print(members_insight(clean, "bmi"))

    print("\n--- cost_drivers_insight ---")
    print(cost_drivers_insight(clean))

    print("\n--- high_risk_insight ---")
    print(high_risk_insight(flag_high_risk(clean)))

    result = train_model(clean)
    predicted = predict_charges(
        result["model"],
        result["feature_columns"],
        age=19,
        sex="female",
        bmi=27.9,
        children=0,
        smoker="yes",
        region="southwest",
    )
    print("\n--- cost_estimator_insight ---")
    print(cost_estimator_insight(clean, predicted))
