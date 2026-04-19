import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Import hàm đọc và xử lý dữ liệu từ file bạn vừa làm xong
from src.data_processing import load_data, preprocess_data

def get_association_rules(df, min_support=0.1, min_confidence=0.5):
    """
    Hàm chạy thuật toán Apriori và xuất ra các luật kết hợp.
    """
    print(f"\n🔍 Đang chạy Apriori với min_support={min_support}, min_confidence={min_confidence}...")
    
    # 1. Tìm các tập dịch vụ thường xuyên xuất hiện cùng nhau
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    
    if frequent_itemsets.empty:
        print(" Không tìm thấy tập mục thường xuyên nào với support này. Hãy giảm min_support xuống!")
        return None
        
    # 2. Sinh ra các luật kết hợp (Association Rules)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    
    if rules.empty:
        print(" Không tìm thấy luật kết hợp nào. Hãy giảm min_confidence xuống!")
        return None
        
    # 3. Làm gọn lại kết quả để dễ đọc
    # Chỉ lấy các cột quan trọng và sắp xếp theo độ Nâng (Lift) giảm dần
    rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    rules = rules.sort_values(by='lift', ascending=False)
    
    # Ép kiểu dữ liệu để in ra nhìn đẹp hơn (bỏ chữ frozenset)
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    
    print(f" Đã tìm thấy {len(rules)} luật kết hợp!")
    return rules

if __name__ == "__main__":
    # 1. Lấy dữ liệu
    data_path = "data/dummy_data.csv" # Lưu ý dấu ../ vì ta đang đứng trong thư mục src
    raw_df = load_data(data_path)
    
    if raw_df is not None:
        # 2. Xử lý dữ liệu
        processed_df = preprocess_data(raw_df)
        
        # 3. Chạy thuật toán
        # Do dữ liệu giả (dummy) của ta có 5 dòng, ta set support = 0.2 (tức là xuất hiện ít nhất 1 lần)
        rules_df = get_association_rules(processed_df, min_support=0.2, min_confidence=0.5)
        
        # 4. In kết quả ra màn hình
        if rules_df is not None:
            print("\n BẢNG XẾP HẠNG CÁC LUẬT KẾT HỢP (TOP 5):")
            print(rules_df.head(5).to_string(index=False))