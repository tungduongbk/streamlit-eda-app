import math

import httpx
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

__all__ = ("app",)

from .utils import millify


def app():
    if "ticker_favorites" not in st.session_state:
        st.session_state.ticker_favorites = set()
    st.title("Stock chart")
    text_input = st.text_input(label="Search")
    col1, col2, col3 = st.columns([3, 1, 1])

    with col2:
        clicked = st.button(label="Add Favorite", on_click=on_add_favorite)
        if clicked:
            st.write("Added success")

    with col3:
        cleared = st.button(label="Clear All", on_click=on_clear_favorites)
        if cleared:
            st.write("Cleared")

    if len(st.session_state.ticker_favorites) > 0:
        with col1:
            st.multiselect(
                "Select your favorite tickers", st.session_state.ticker_favorites, key="selected_tickers"
            )

    periods = ["1mo", "3mo", "6mo"]
    columns_chart, column_period = st.columns([10, 1.8])
    with column_period:
        period = st.selectbox(
            label="Period", options=periods,
            index=0, label_visibility="collapsed"
        )
    with columns_chart:
        fig = go.Figure()
        search_ticker = None
        if (text_input is not None) and (text_input != ""):
            fig, search_ticker = plot_search_text(text_input, fig, period)
        if "selected_tickers" in st.session_state:
            selected_tickers = st.session_state.selected_tickers
            if len(selected_tickers) > 0:
                fig = plot_tickers_selection(search_ticker, selected_tickers, fig, period)
        st.plotly_chart(fig)


def on_add_favorite():
    current_ticker = st.session_state.current_ticker
    if current_ticker is not None:
        st.session_state.ticker_favorites.add(current_ticker)


def on_clear_favorites():
    st.session_state.ticker_favorites.clear()


@st.cache_data
def call_ticker_history(text_input: str, period) -> httpx.Response:
    # TODO: Implement query multiple tickers at once - for round trip purpose
    url = "http://localhost:8083/stocks/search"
    params = {"query": text_input}
    if period is not None:
        params["period"] = period

    res = httpx.get(url=url, params=params)
    return res


def plot_tickers_selection(search_ticker, selected: list, fig, period):
    for ticker in selected:
        if ticker == search_ticker:
            continue
        response = call_ticker_history(ticker, period)
        data = response.json()
        if response.status_code == 200:
            df = pd.DataFrame(data["history"])
            fig = fig.add_trace(go.Scatter(x=df["timestamp"], y=df["value"], name=ticker, mode="lines"))
    return fig


def plot_search_text(search_text, fig, period):
    result = call_ticker_history(search_text, period)
    data = result.json()
    if result.status_code == 200:
        st.metric(data["symbol"].upper(),
                  value=millify(data["history"][-1]["value"]),
                  delta=millify(data["delta"]))
        fig = plot_stocks([data], fig)
        st.session_state.current_ticker = data["symbol"]
    else:
        st.header(data["message"])
    return fig, data.get("symbol")


def plot_stocks(histories: list[dict], fig):
    for his in histories:
        ticker = his["symbol"]
        df = pd.DataFrame(his["history"])
        fig = fig.add_trace(go.Scatter(x=df["timestamp"], y=df["value"], name=ticker, mode="lines"))
    return fig
