import streamlit as st
from apps import dashboard, stocks
from streamlit_option_menu import option_menu

apps = [
    {
        "func": dashboard.app,
        "title": "Convenience store brand dashboard",
        "icon": "bar-chart-fill",
    },
    {"func": stocks.app, "title": "Stock trading", "icon": "graph-up-arrow"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]
params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="menu-app",
        default_index=default_index,
    )

    st.sidebar.title("About")

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
