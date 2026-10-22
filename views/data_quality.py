"""Data Quality page: can we trust this data? Always describes the full dataset."""

import streamlit as st

from src.quality import (
    categorical_profile,
    duplicate_summary,
    dtype_summary,
    null_summary,
    numeric_profile,
)


def render() -> None:
    raw_df = st.session_state["raw_df"]
    clean_df = st.session_state["clean_df"]

    st.title("Can we trust this data?")
    st.caption("This page always describes the full dataset, independent of sidebar filters.")

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
