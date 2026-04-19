import streamlit as st
import pandas as pd

# Import các hàm bạn đã viết ở thư mục src
from src.data_processing import load_data, preprocess_data
from src.apriori_engine import get_association_rules

# 1. Cấu hình giao diện trang Web
st.set_page_config(page_title="Gợi ý Du Lịch", page_icon="✈️", layout="wide")
st.title("✈️ Hệ Thống Phân Tích & Gợi Ý Combo Du Lịch")
st.markdown("---")

# 2. Tải và xử lý dữ liệu ngầm bên dưới
data_path = "data/dummy_data.csv"
raw_df = load_data(data_path)

if raw_df is not None:
    processed_df = preprocess_data(raw_df)
    
    # 3. Tạo thanh công cụ bên trái (Sidebar)
    st.sidebar.header("⚙️ Bảng Điều Khiển Thuật Toán")
    min_supp = st.sidebar.slider("Độ hỗ trợ (Min Support)", 0.01, 0.5, 0.2, 0.01)
    min_conf = st.sidebar.slider("Độ tin cậy (Min Confidence)", 0.1, 1.0, 0.5, 0.05)
    
    # 4. Chạy thuật toán dựa trên thanh trượt
    rules = get_association_rules(processed_df, min_supp, min_conf)
    
    # 5. Hiển thị lên Web
    col1, col2 = st.columns([2, 1]) # Chia tỷ lệ màn hình 2:1
    
    with col1:
        st.subheader("📊 Danh sách Luật kết hợp tìm được")
        if rules is not None and not rules.empty:
            # Hiển thị bảng dữ liệu đẹp mắt
            st.dataframe(rules, use_container_width=True)
        else:
            st.warning("Không tìm thấy luật nào! Hãy thử kéo thanh trượt giảm Support/Confidence xuống.")
            
    with col2:
        st.subheader("💡 Chuyên viên tư vấn ảo")
        st.info("Tính năng mô phỏng Cross-selling cho nhân viên bán hàng.")
        
        if rules is not None and not rules.empty:
            # Lấy danh sách tất cả các dịch vụ
            all_services = processed_df.columns.tolist()
            selected_item = st.selectbox("Khách hàng đang hỏi dịch vụ nào?", ["-- Chọn dịch vụ --"] + all_services)
            
            if selected_item != "-- Chọn dịch vụ --":
                # Lọc ra các luật có chứa dịch vụ khách đang chọn ở vế trái (antecedents)
                suggestions = rules[rules['antecedents'].str.contains(selected_item)]
                
                if not suggestions.empty:
                    st.success(f"Khách mua **{selected_item}** thường mua thêm:")
                    # Chỉ hiện những cột cần thiết cho nhân viên xem
                    st.table(suggestions[['consequents', 'confidence']].head(3))
                else:
                    st.write("Chưa có gợi ý đi kèm cho dịch vụ này.")
else:
    st.error("Không tìm thấy file dữ liệu. Vui lòng kiểm tra lại đường dẫn!")