import streamlit as st

st.set_page_config(page_title="Hệ thống Gợi ý Du lịch", page_icon="🌍", layout="wide")

st.title("🌍 Hệ thống Khai thác Dữ liệu Hành vi Du lịch")
st.markdown("---")

st.markdown("""
### 👋 Chào mừng thầy cô và các bạn đến với đồ án của nhóm!

Hệ thống này được thiết kế để giải quyết bài toán bán chéo (Cross-selling) cho các đại lý du lịch, giúp tăng doanh thu bằng cách phân tích lịch sử giao dịch và đưa ra các Combo phù hợp.

**Hệ thống bao gồm 2 phân hệ chính:**
1. 📊 **Dashboard Quản lý:** Dành cho Giám đốc xem báo cáo tổng quan, tình hình tiêu thụ các dịch vụ.
2. 💡 **Hệ thống Gợi ý (Apriori Engine):** Dành cho Nhân viên Sale / Khách hàng để tự động đề xuất dịch vụ đi kèm.

👈 **Vui lòng chọn các chức năng ở thanh Menu bên trái để bắt đầu trải nghiệm.**
""")