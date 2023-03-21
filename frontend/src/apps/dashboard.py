import os

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from .utils import millify

# get the absolute path to the directory contain the .csv file
dir_name = os.path.abspath(os.path.dirname(__file__))

csv_file = os.path.join(dir_name, "resource/eda_convenience_store_brands.csv")

df = pd.read_csv(csv_file)
total_revenue = df["Item_Outlet_Sales"].sum()
total_item_sales = df.shape[0]
df_item_sales_by_year = df[["Item_Outlet_Sales", "Outlet_Establishment_Year"]] \
    .groupby("Outlet_Establishment_Year").sum().reset_index().sort_values(by=['Outlet_Establishment_Year'])

df_item_sales_by_item_type = df[["Item_Outlet_Sales", "Item_Type"]] \
    .groupby("Item_Type").sum().reset_index()


def app():
    st.title("Convenience store brand dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Revenue", value=millify(total_revenue))
    with col2:
        st.metric(label="Total Items", value=total_item_sales)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            data_frame=df, y="Item_Outlet_Sales", x="Outlet_Type",
            title="Revenue By Outlet_Type"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig = px.pie(df, values="Item_Outlet_Sales", names="Outlet_Type")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            data_frame=df, y="Item_Outlet_Sales", x="Outlet_Location_Type",
            title="Revenue By Outlet_Location_Type"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig = px.pie(df, values="Item_Outlet_Sales", names="Outlet_Location_Type")
        st.plotly_chart(fig, use_container_width=True)

    fig = plot_revenue_by_item_type()
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        data_frame=df_item_sales_by_year, y="Item_Outlet_Sales", x="Outlet_Establishment_Year",
        title="Revenue By Outlet_Establishment_Year"
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_revenue_by_item_type():
    fig = px.bar(
        data_frame=df_item_sales_by_item_type, y="Item_Outlet_Sales", x="Item_Type",
        title="Revenue By Item_Type"
    )
    return fig
