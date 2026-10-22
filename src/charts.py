"""Plotly chart builders. Every function returns a go.Figure; no business logic."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fixed categorical colors (never auto-cycled), drawn from the validated palette.
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
RED = "#e34948"
MUTED = "#898781"

SMOKER_COLORS = {"no": BLUE, "yes": ORANGE}
SEX_COLORS = {"female": BLUE, "male": ORANGE}
REGION_ORDER = ["northeast", "northwest", "southeast", "southwest"]
REGION_COLORS = dict(zip(REGION_ORDER, [BLUE, ORANGE, AQUA, YELLOW]))

GROUP_COLOR_MAPS = {"smoker": SMOKER_COLORS, "sex": SEX_COLORS, "region": REGION_COLORS}


def histogram(df: pd.DataFrame, col: str, title: str | None = None) -> go.Figure:
    fig = px.histogram(df, x=col, nbins=40, color_discrete_sequence=[BLUE])
    fig.update_layout(title=title or f"Distribution of {col}", bargap=0.05)
    return fig


def boxplot(df: pd.DataFrame, group_col: str, value_col: str = "charges") -> go.Figure:
    category_orders = {group_col: REGION_ORDER} if group_col == "region" else None
    fig = px.box(
        df,
        x=group_col,
        y=value_col,
        category_orders=category_orders,
        color_discrete_sequence=[BLUE],
    )
    fig.update_layout(title=f"{value_col.title()} by {group_col}")
    return fig


def scatter_vs_charges(
    df: pd.DataFrame, x_col: str, color_col: str = "smoker"
) -> go.Figure:
    color_map = GROUP_COLOR_MAPS.get(color_col)
    fig = px.scatter(
        df,
        x=x_col,
        y="charges",
        color=color_col,
        color_discrete_map=color_map,
        opacity=0.6,
    )
    fig.update_traces(marker=dict(size=7))
    fig.update_layout(title=f"{x_col.title()} vs Charges (by {color_col})")
    return fig


def correlation_heatmap(df_encoded: pd.DataFrame) -> go.Figure:
    corr = df_encoded.corr(numeric_only=True)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale=[RED, "#f0efec", BLUE],
        zmin=-1,
        zmax=1,
        aspect="auto",
    )
    fig.update_layout(title="Correlation Matrix")
    return fig


def risk_factor_breakdown(df_flagged: pd.DataFrame, group_col: str) -> go.Figure:
    summary = (
        df_flagged.groupby(group_col)["is_high_risk"]
        .mean()
        .mul(100)
        .reset_index(name="high_risk_pct")
    )
    category_orders = {group_col: REGION_ORDER} if group_col == "region" else None
    fig = px.bar(
        summary,
        x=group_col,
        y="high_risk_pct",
        category_orders=category_orders,
        color_discrete_sequence=[BLUE],
        text_auto=".1f",
    )
    fig.update_layout(title=f"High-Risk % by {group_col}", yaxis_title="High-Risk %")
    return fig


def actual_vs_predicted(y_test: pd.Series, predictions) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=y_test,
            y=predictions,
            mode="markers",
            marker=dict(color=BLUE, size=7, opacity=0.6),
            name="Members",
        )
    )
    lo, hi = float(y_test.min()), float(y_test.max())
    fig.add_trace(
        go.Scatter(
            x=[lo, hi],
            y=[lo, hi],
            mode="lines",
            line=dict(color=MUTED, dash="dash", width=2),
            name="Perfect prediction",
        )
    )
    fig.update_layout(
        title="Actual vs Predicted Charges (Test Set)",
        xaxis_title="Actual Charges",
        yaxis_title="Predicted Charges",
    )
    return fig


def coefficient_chart(coef_df: pd.DataFrame) -> go.Figure:
    sorted_df = coef_df.sort_values("weight")
    colors = [RED if w < 0 else BLUE for w in sorted_df["weight"]]
    fig = go.Figure(
        go.Bar(
            x=sorted_df["weight"],
            y=sorted_df["feature"],
            orientation="h",
            marker_color=colors,
        )
    )
    fig.update_layout(title="Model Feature Weights", xaxis_title="Weight ($ per unit)")
    return fig


if __name__ == "__main__":
    from data_loader import get_clean_data
    from metrics import flag_high_risk
    from model import encode_features, train_model

    clean = get_clean_data()

    figs = {
        "histogram": histogram(clean, "charges"),
        "boxplot_smoker": boxplot(clean, "smoker"),
        "scatter_age": scatter_vs_charges(clean, "age"),
        "correlation_heatmap": correlation_heatmap(encode_features(clean)),
        "risk_breakdown": risk_factor_breakdown(flag_high_risk(clean), "region"),
    }

    result = train_model(clean)
    figs["actual_vs_predicted"] = actual_vs_predicted(result["y_test"], result["predictions"])
    figs["coefficients"] = coefficient_chart(result["coefficients"])

    for name, fig in figs.items():
        assert fig.data, f"{name} produced an empty figure"
        print(f"{name}: OK ({len(fig.data)} trace(s))")
