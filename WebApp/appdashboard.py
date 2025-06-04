import streamlit as st

st.set_page_config(page_title="Football Dashboard", layout="centered", page_icon="⚽")
st.markdown("""
    <style>
    body, .stApp {
        background-color: #181818;
        color: #f5f6fa;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Football Dashboard")
st.subheader("Chọn giải đấu để xem dashboard")

option = st.selectbox("Chọn giải đấu", ("La Liga", "Serie A"))

if st.button("Xem dashboard"):
    try:
        # Streamlit 1.25+ (nếu có)
        from streamlit_extras.switch_page_button import switch_page
        if option == "La Liga":
            switch_page("laliga_dashboard")
        else:
            switch_page("seriea_dashboard")
    except Exception:
        # Nếu không có switch_page, hướng dẫn user bấm link
        if option == "La Liga":
            st.markdown('[Nhấn vào đây để mở La Liga Dashboard](laliga_dashboard.py)', unsafe_allow_html=True)
        else:
            st.markdown('[Nhấn vào đây để mở Serie A Dashboard](seriea_dashboard.py)', unsafe_allow_html=True) 