import streamlit as st
import pandas as pd

# Import hàm xử lý dữ liệu
from src.data_processing import load_data, preprocess_data

st.set_page_config(page_title="Dashboard Quản lý", page_icon="📊", layout="wide")
st.title("📊 Báo Cáo Tổng Quan Các Dịch Vụ")
st.markdown("---")

# Tải dữ liệu
data_path = "data/dummy_data.csv"
raw_df = load_data(data_path)

if raw_df is not None:
    processed_df = preprocess_data(raw_df)
    
    # Chia đôi màn hình
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tần suất khách mua dịch vụ")
        st.info("Biểu đồ cho thấy dịch vụ nào đang mang lại lượng khách đông nhất.")
        # Tính tổng số lần xuất hiện của mỗi dịch vụ
        service_counts = processed_df.sum().sort_values(ascending=False)
        # Vẽ biểu đồ cột tích hợp sẵn của Streamlit
        st.bar_chart(service_counts, color="#1f77b4")
        
    with col2:
        st.subheader("🗂️ Dữ liệu Giao dịch Gốc (Raw Data)")
        st.info(f"Tổng số giao dịch đang phân tích: {len(raw_df)} đơn hàng.")
        st.dataframe(raw_df, use_container_width=True)

else:
    st.error("Không tải được dữ liệu.")