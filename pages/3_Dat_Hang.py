import streamlit as st
import pandas as pd
from src.data_processing import load_data, preprocess_data
from src.apriori_engine import get_association_rules

st.set_page_config(page_title="Đặt Hàng", page_icon="🛒", layout="wide")
st.title("🛒 Trải nghiệm Đặt Hàng & Gợi ý Thông minh")
st.markdown("---")

# BẢNG GIÁ GIẢ LẬP (MOCK DATA) - Giúp demo sinh động hơn
PRICE_LIST = {
    'Ve may bay': 1500000,
    'Khach san': 800000,
    'Thue xe may': 150000,
    'Tour 4 dao': 500000,
    'Bao hiem': 100000
}

def format_currency(amount):
    """Hàm định dạng tiền tệ VNĐ"""
    return f"{amount:,.0f} VNĐ".replace(',', '.')

# Khởi tạo Giỏ hàng
if 'cart' not in st.session_state:
    st.session_state.cart = []

data_path = "data/dummy_data.csv"
raw_df = load_data(data_path)

if raw_df is not None:
    processed_df = preprocess_data(raw_df)
    rules = get_association_rules(processed_df, min_support=0.1, min_confidence=0.5)
    all_services = processed_df.columns.tolist()

    col1, col2 = st.columns([2, 1])

    # CỘT TRÁI: MENU DỊCH VỤ
    with col1:
        st.subheader("🛍️ Danh mục Dịch vụ Du lịch")
        cols = st.columns(3)
        for i, service in enumerate(all_services):
            with cols[i % 3]:
                # Hiển thị nút bấm kèm giá tiền
                price_str = format_currency(PRICE_LIST.get(service, 0))
                if st.button(f"➕ Thêm {service}\n({price_str})", use_container_width=True, key=f"btn_{service}"):
                    if service not in st.session_state.cart:
                        st.session_state.cart.append(service)
                        st.rerun() # Tải lại trang ngay lập tức

    # CỘT PHẢI: GIỎ HÀNG VÀ GỢI Ý
    with col2:
        st.subheader("🛒 Giỏ hàng của bạn")
        
        total_price = 0
        if not st.session_state.cart:
            st.info("Giỏ hàng đang trống.")
        else:
            for item in st.session_state.cart:
                item_price = PRICE_LIST.get(item, 0)
                total_price += item_price
                st.success(f"✅ {item} - {format_currency(item_price)}")
            
            # Hiển thị Tổng Bill thật nổi bật
            st.metric(label="💰 Tổng thanh toán", value=format_currency(total_price))
            
            if st.button("🗑️ Xóa tất cả", type="secondary"):
                st.session_state.cart = []
                st.rerun()

        st.markdown("---")
        
        # HỆ THỐNG GỢI Ý THÔNG MINH
        st.subheader("💡 Gợi ý cho bạn")
        
        if not st.session_state.cart:
            # Xử lý Cold Start: Nếu giỏ trống, gợi ý Top 2 món phổ biến nhất
            st.caption("🔥 Top dịch vụ bán chạy nhất tháng:")
            top_services = processed_df.sum().sort_values(ascending=False).head(2).index.tolist()
            for item in top_services:
                if st.button(f"🚀 Thêm {item} vào giỏ", key=f"top_{item}"):
                    st.session_state.cart.append(item)
                    st.rerun()
                    
        elif rules is not None and not rules.empty:
            cart_set = set(st.session_state.cart)
            valid_suggestions = []
            
            for index, row in rules.iterrows():
                antecedents_set = set([item.strip() for item in row['antecedents'].split(',')])
                consequents_set = set([item.strip() for item in row['consequents'].split(',')])
                
                if antecedents_set.issubset(cart_set) and not consequents_set.intersection(cart_set):
                    valid_suggestions.append({
                        'dieu_kien': row['antecedents'],
                        'goi_y': row['consequents'],
                        'ti_le': row['confidence'],
                        'do_dai_dieu_kien': len(antecedents_set)
                    })
            
            if valid_suggestions:
                valid_suggestions = sorted(valid_suggestions, key=lambda x: (x['do_dai_dieu_kien'], x['ti_le']), reverse=True)
                
                seen = set()
                count = 0
                st.write("Vì bạn đã chọn Combo này, mua thêm món sau sẽ rất hợp lý:")
                
                for item in valid_suggestions:
                    suggested_item = item['goi_y']
                    if suggested_item not in seen and count < 2: # Chỉ hiện tối đa 2 gợi ý tốt nhất
                        # BIẾN GỢI Ý THÀNH NÚT BẤM (Mua ngay)
                        price_goi_y = PRICE_LIST.get(suggested_item, 0)
                        button_label = f"✨ Mua thêm {suggested_item}\n(Khớp {item['ti_le']*100:.0f}% - Giá: {format_currency(price_goi_y)})"
                        
                        if st.button(button_label, type="primary", key=f"suggest_{suggested_item}"):
                            st.session_state.cart.append(suggested_item)
                            st.rerun()
                            
                        seen.add(suggested_item)
                        count += 1
            else:
                st.info("🎉 Bạn đã chọn một Combo quá hoàn hảo!")
else:
    st.error("Lỗi tải dữ liệu hệ thống.")