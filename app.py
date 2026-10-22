"""Insurance Cost & Risk Analytics Dashboard entrypoint. Navigation/layout only; logic lives in src/."""

import streamlit as st

from src.data_loader import get_clean_data, load_raw_data
from views import cost_drivers, cost_estimator, data_quality, high_risk, members, overview
from views.components import render_sidebar_filters

st.set_page_config(page_title="Insurance Cost & Risk Analytics", layout="wide")

raw_df = load_raw_data()
clean_df = get_clean_data()

st.sidebar.title("Insurance Cost & Risk Analytics")
filtered_df = render_sidebar_filters(clean_df)

if filtered_df.empty:
    st.warning("No members match the current filters. Adjust the sidebar filters.")
    st.stop()

st.session_state["raw_df"] = raw_df
st.session_state["clean_df"] = clean_df
st.session_state["filtered_df"] = filtered_df

pg = st.navigation(
    [
        st.Page(overview.render, title="Overview", url_path="overview", default=True),
        st.Page(data_quality.render, title="Data Quality", url_path="data-quality"),
        st.Page(members.render, title="Who are our members?", url_path="members"),
        st.Page(
            cost_drivers.render, title="What drives medical costs?", url_path="cost-drivers"
        ),
        st.Page(high_risk.render, title="Who is high risk?", url_path="high-risk"),
        st.Page(
            cost_estimator.render, title="What will a member cost?", url_path="cost-estimator"
        ),
    ]
)
pg.run()
