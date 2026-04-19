import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

def load_data(filepath):
    """Hàm đọc dữ liệu từ file CSV"""
    try:
        df = pd.read_csv(filepath)
        print("✅ Tải dữ liệu thô thành công!")
        return df
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file {filepath}")
        return None

def preprocess_data(df):
    """Hàm biến đổi dữ liệu sang dạng One-Hot Encoding"""
    # 1. Tách chuỗi bằng dấu phẩy và xóa khoảng trắng thừa
    # "Ve may bay, Khach san" -> ['Ve may bay', 'Khach san']
    transactions = df['Items'].apply(lambda x: [item.strip() for item in x.split(',')]).tolist()
    
    # 2. Sử dụng TransactionEncoder để chuyển thành ma trận True/False
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    
    # 3. Gom lại thành DataFrame của Pandas cho đẹp
    encoded_df = pd.DataFrame(te_ary, columns=te.columns_)
    
    print("\n✅ Biến đổi dữ liệu thành công (One-Hot Encoding)!")
    print(f"📊 Có tổng cộng {len(te.columns_)} dịch vụ duy nhất: {te.columns_}")
    print("\n--- Bảng dữ liệu đã sẵn sàng cho Apriori ---")
    print(encoded_df.head())
    
    return encoded_df

if __name__ == "__main__":
    data_path = "data/dummy_data.csv"
    
    # Chạy hàm đọc dữ liệu
    raw_df = load_data(data_path)
    
    # Nếu đọc thành công thì chạy tiếp hàm biến đổi
    if raw_df is not None:
        processed_df = preprocess_data(raw_df)