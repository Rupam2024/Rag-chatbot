import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from database.sqlite_db import db

# Load Dataset

def load_data(csv_path):

    try:

        df = pd.read_csv(csv_path)

        df = df.fillna("Not Available")

        return df

    except Exception as e:

        st.error(
            f"Error loading dataset: {e}"
        )

        return pd.DataFrame()

# KPI Metrics

def show_kpis(df):

    total_products = len(df)

    total_companies = (
        df["COMPANY"]
        .nunique()
        if "COMPANY" in df.columns
        else 0
    )

    avg_mrp = (
        pd.to_numeric(
            df["MRP"],
            errors="coerce"
        ).mean()
        if "MRP" in df.columns
        else 0
    )

    total_categories = (
        df["SUB GROUP"]
        .nunique()
        if "SUB GROUP" in df.columns
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Products",
        total_products
    )

    col2.metric(
        "Companies",
        total_companies
    )

    col3.metric(
        "Avg MRP",
        f"₹{avg_mrp:.2f}"
    )

    col4.metric(
        "Categories",
        total_categories
    )


# Top Companies


def top_companies_chart(
    df,
    top_n=10
):

    if "COMPANY" not in df.columns:
        return

    company_counts = (
        df["COMPANY"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    company_counts.columns = [
        "Company",
        "Count"
    ]

    fig = px.bar(
        company_counts,
        x="Company",
        y="Count",
        title="Top Companies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Top Drug Categories
def top_categories_chart(
    df,
    top_n=10
):

    if "SUB GROUP" not in df.columns:
        return

    category_counts = (
        df["SUB GROUP"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    category_counts.columns = [
        "Category",
        "Count"
    ]

    fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        title="Top Drug Categories"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# MRP Distribution

def mrp_distribution_chart(df):

    if "MRP" not in df.columns:
        return

    mrp = pd.to_numeric(
        df["MRP"],
        errors="coerce"
    )

    fig = px.histogram(
        mrp,
        nbins=20,
        title="MRP Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# NLEM Status

def nlem_chart(df):

    possible_cols = [
        "NLEM",
        "NLEM STATUS"
    ]

    column = None

    for col in possible_cols:

        if col in df.columns:
            column = col
            break

    if not column:
        return

    counts = (
        df[column]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        counts,
        names="Status",
        values="Count",
        title="NLEM Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Query Analytics

def query_analytics():

    metrics = db.dashboard_metrics()

    st.subheader(
        "Query Analytics"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Queries",
        metrics["total_queries"]
    )

    col2.metric(
        "Avg Response Time",
        f"{metrics['avg_response_time']} sec"
    )

    col3.metric(
        "Avg Rating",
        metrics["avg_rating"]
    )

# Top Searches

def top_searches_chart():

    searches = db.get_top_searches(
        limit=10
    )

    if not searches:
        return

    df = pd.DataFrame(
        searches,
        columns=[
            "Drug",
            "Search Count"
        ]
    )

    fig = px.bar(
        df,
        x="Drug",
        y="Search Count",
        title="Most Searched Drugs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Recent Queries

def recent_queries_table():

    data = db.get_recent_queries(
        limit=10
    )

    if not data:
        return

    df = pd.DataFrame(
        data,
        columns=[
            "Question",
            "Route",
            "Response Time",
            "Timestamp"
        ]
    )

    st.subheader(
        "Recent Queries"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# Dashboard Page


def render_dashboard(
    csv_path
):

    st.title(
        "Drug Analytics Dashboard"
    )

    df = load_data(
        csv_path
    )

    if df.empty:

        st.warning(
            "Dataset not found."
        )

        return

    show_kpis(df)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        top_companies_chart(df)

    with col2:

        top_categories_chart(df)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        mrp_distribution_chart(df)

    with col4:

        nlem_chart(df)

    st.divider()

    query_analytics()

    st.divider()

    top_searches_chart()

    st.divider()

    recent_queries_table()

# Standalone Test

if __name__ == "__main__":

    print(
        "Use inside Streamlit app."
    )
