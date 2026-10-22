"""KPIs and high-risk member flagging logic. Operates on an already-filtered DataFrame."""

import pandas as pd

DEFAULT_BMI_THRESHOLD = 30
DEFAULT_AGE_THRESHOLD = 50
DEFAULT_CHARGES_PERCENTILE = 75
DEFAULT_MIN_FACTORS = 2


def kpi_summary(df: pd.DataFrame) -> dict:
    return {
        "member_count": len(df),
        "avg_charges": df["charges"].mean(),
        "avg_bmi": df["bmi"].mean(),
        "avg_age": df["age"].mean(),
        "smoker_pct": (df["smoker"] == "yes").mean() * 100,
    }


def flag_high_risk(
    df: pd.DataFrame,
    bmi_threshold: float = DEFAULT_BMI_THRESHOLD,
    age_threshold: int = DEFAULT_AGE_THRESHOLD,
    charges_percentile: float = DEFAULT_CHARGES_PERCENTILE,
    min_factors: int = DEFAULT_MIN_FACTORS,
) -> pd.DataFrame:
    flagged = df.copy()
    charges_cutoff = df["charges"].quantile(charges_percentile / 100)

    flagged["factor_smoker"] = flagged["smoker"] == "yes"
    flagged["factor_bmi"] = flagged["bmi"] >= bmi_threshold
    flagged["factor_age"] = flagged["age"] >= age_threshold
    flagged["factor_charges"] = flagged["charges"] >= charges_cutoff

    factor_cols = ["factor_smoker", "factor_bmi", "factor_age", "factor_charges"]
    flagged["risk_factor_count"] = flagged[factor_cols].sum(axis=1)
    flagged["is_high_risk"] = flagged["risk_factor_count"] >= min_factors

    return flagged


def high_risk_summary(df_flagged: pd.DataFrame) -> dict:
    total = len(df_flagged)
    high_risk_count = int(df_flagged["is_high_risk"].sum())
    return {
        "high_risk_count": high_risk_count,
        "high_risk_pct": (high_risk_count / total * 100) if total else 0.0,
    }


def group_stats(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    return df.groupby(group_col)["charges"].agg(["mean", "median", "count"])


if __name__ == "__main__":
    from data_loader import get_clean_data

    clean = get_clean_data()

    print("--- KPI summary ---")
    print(kpi_summary(clean))

    flagged = flag_high_risk(clean)
    print("\n--- High-risk summary (default thresholds) ---")
    print(high_risk_summary(flagged))

    print("\n--- Group stats by sex ---")
    print(group_stats(clean, "sex"))

    print("\n--- Group stats by smoker ---")
    print(group_stats(clean, "smoker"))
