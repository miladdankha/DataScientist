import streamlit as st

st.set_page_config(page_title="Bike sharing · Paris", layout="wide")

st.title("Weekend rentals have doubled since 2022")
st.caption("Vélib' stations · all rentals, January 2022 to June 2024 · source: open data")

with st.sidebar:
    st.subheader("About")
    st.write("Interactive version of the bike sharing brief.")