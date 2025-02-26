import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Đọc dữ liệu từ Google Sheets
sheet_id = "1mjMrweeCQVRrOiqQRkJGe66DWbzTKsJh"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
df = pd.read_csv(csv_url).dropna().reset_index(drop=True)

# Giao diện Streamlit
st.set_page_config(page_title="Tra cứu Thực phẩm", layout="wide")
st.markdown("""
    <style>
        .title { text-align: center; font-size: 32px; font-weight: bold; color: #ff6347; }
        .food-card { background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); }
        .food-image { border-radius: 10px; width: 200px; height: 200px; object-fit: cover; }
        .nutrition-info { display: flex; flex-wrap: wrap; gap: 10px; }
        .nutrient { width: 48%; padding: 5px; background: #f1f1f1; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🍏 Tra cứu Thực phẩm (100g mỗi loại) 🍏</p>', unsafe_allow_html=True)
st.subheader("Tìm kiếm và xem thông tin dinh dưỡng của thực phẩm")

# Thanh tìm kiếm
tim_kiem = st.text_input("🔍 Nhập tên thực phẩm:", placeholder="Nhập tên món ăn...")

# Bộ lọc loại thực phẩm
loai_thuc_pham = df["Loại"].unique().tolist()
loai_chon = st.multiselect("📌 Chọn loại thực phẩm:", loai_thuc_pham, default=[])

df_filtered = pd.DataFrame(columns=df.columns)

if loai_chon or tim_kiem:
    # Lọc dữ liệu
    df_filtered = df.copy()
    if loai_chon:
        df_filtered = df_filtered[df_filtered["Loại"].isin(loai_chon)]
    if tim_kiem:
        df_filtered = df_filtered[df_filtered["TÊN THỨC ĂN"].str.contains(tim_kiem, case=False, na=False)]

# Hiển thị dữ liệu
if not df_filtered.empty:
    for _, row in df_filtered.iterrows():
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(row["Hình"], width=200)
            st.markdown(f"""
                **{row["TÊN THỨC ĂN"]}**
            """)

        with col2:
            st.markdown(f"""
                🔥 **Calories:** {row['Calories (kcal)']} kcal  
                💪 **Protein:** {row['Protein (g)']} g  
                🛢️ **Fat:** {row['Fat (g)']} g  
                🍞 **Carbs:** {row['Carbonhydrates (g)']} g  
            """)

            with st.expander("📋 Thông tin chi tiết"):
                col_left, col_right = st.columns(2)
                nutrients = [
                    "Calories (kcal)", "Protein (g)", "Fat (g)", "Carbonhydrates (g)", "Chất xơ (g)",
                    "Cholesterol (mg)",
                    "Canxi (mg)", "Photpho (mg)", "Sắt (mg)", "Natri (mg)", "Kali (mg)", "Beta Caroten (mcg)",
                    "Vitamin A (mcg)", "Vitamin B1 (mg)", "Vitamin C (mg)"
                ]

                for i, nutrient in enumerate(nutrients):
                    if i % 2 == 0:
                        col_left.write(f"**{nutrient}:** {row[nutrient]}")
                    else:
                        col_right.write(f"**{nutrient}:** {row[nutrient]}")

                st.write(f"**Loại thực phẩm:** {row['Loại']}")

        st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")
else:
    st.warning("⚠️ Không tìm thấy thực phẩm phù hợp.")