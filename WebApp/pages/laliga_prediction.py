import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dự đoán La Liga", layout="wide", page_icon="⚽")
st.markdown("""
    <style>
    body, .stApp {
        background-color: #181818;
        color: #f5f6fa;
    }
    .stDataFrame, .stTable {
        background-color: #222 !important;
        color: #f5f6fa !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Bảng dự đoán kết quả La Liga")

pred_path = os.path.join('Datasets', 'Predictions', 'predictions_laliga_spain.csv')
if os.path.exists(pred_path):
    pred_df = pd.read_csv(pred_path)
    if not pred_df.empty:
        pred_df = pred_df.rename(columns={
            "Date": "Ngày",
            "Time": "Giờ",
            "Team A": "Đội A",
            "Team B": "Đội B",
            "Prediction for Team A": "Dự đoán Đội A",
            "Prediction for Team B": "Dự đoán Đội B"
        })
        def highlight_prediction(val):
            if val == "W":
                return "background-color: #00b894; color: white"
            elif val == "L":
                return "background-color: #d63031; color: white"
            elif val == "D":
                return "background-color: #fdcb6e; color: black"
            return ""
        styled_df = pred_df.style.applymap(highlight_prediction, subset=["Dự đoán Đội A", "Dự đoán Đội B"])
        st.dataframe(styled_df, use_container_width=True, hide_index=True, height=600)
    else:
        st.warning("File dự đoán La Liga rỗng!")
else:
    st.warning("Không tìm thấy file dự đoán La Liga!") 