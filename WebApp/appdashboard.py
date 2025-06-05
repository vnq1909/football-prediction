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
st.subheader("Chào mừng bạn đến với Football Dashboard!")

st.markdown("""
trang này giúp bạn theo dõi, phân tích và trực quan hóa dữ liệu các giải bóng đá hàng đầu như La Liga và Serie A.

- Xem thống kê, bảng xếp hạng, kết quả và nhiều thông tin hấp dẫn khác.
- Sử dụng menu bên trái để chọn dashboard của từng giải đấu.
""") 