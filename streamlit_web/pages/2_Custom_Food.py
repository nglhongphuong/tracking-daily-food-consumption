import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from streamlit_echarts import st_echarts

# Cấu hình trang
st.set_page_config(page_title="Thiết kế Bữa Ăn", layout="wide")
st.markdown("""
    <style>
        .title { text-align: center; font-size: 32px; font-weight: bold; color: #ff6347; }
        .container { background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); }
        .input-field { padding: 5px; border-radius: 5px; border: 1px solid #ccc; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🥗 Thiết kế Bữa Ăn theo Nhu Cầu 🥗</p>', unsafe_allow_html=True)

# Tải dữ liệu thức ăn
sheet_id = "1mjMrweeCQVRrOiqQRkJGe66DWbzTKsJh"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
df = pd.read_csv(csv_url).dropna().reset_index(drop=True)

cols_to_convert = [col for col in df.columns if col not in ["TÊN THỨC ĂN", "Loại", "Hình"]]

df[cols_to_convert] = df[cols_to_convert].replace({',': '', ' ': '', 'NA': None}, regex=True)
df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
df[cols_to_convert] = df[cols_to_convert].fillna(df[cols_to_convert].mean()).astype(int)

# Phân nhóm calo bằng KMeans
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[["Calories (kcal)"]])
kmeans = KMeans(n_clusters=3, random_state=42)
df["Calorie Type"] = kmeans.fit_predict(df_scaled)
df["Calorie Type"] = df["Calorie Type"].map({0: 'Calo thấp', 1: 'Calo trung bình', 2: 'Calo cao'})

# Huấn luyện mô hình Decision Tree
X_train = df[["Calories (kcal)", "Protein (g)", "Fat (g)", "Carbonhydrates (g)"]]
y_train = df["Calorie Type"]
model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

# Khởi tạo danh sách món ăn đã thêm
if "added_meals" not in st.session_state:
    st.session_state.added_meals = []

if len(st.session_state.added_meals) > 0:
    # Hiển thị biểu đồ trước
    st.markdown("## 📊 Tổng Quan Dinh Dưỡng")
    total_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for meal in st.session_state.added_meals:
        total_nutrition["calories"] += meal["calories"]
        total_nutrition["protein"] += meal["protein"]
        total_nutrition["fat"] += meal["fat"]
        total_nutrition["carbs"] += meal["carbs"]

    total_data = [
        {"value": total_nutrition["calories"], "name": "Calories"},
        {"value": total_nutrition["protein"], "name": "Protein"},
        {"value": total_nutrition["fat"], "name": "Fat"},
        {"value": total_nutrition["carbs"], "name": "Carbs"}
    ]
    total_options = {
        "title": {"left": "center", "top": "2%", "textStyle": {"fontSize": 18, "fontWeight": "bold", "color": "#333"}},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
        "legend": {"orient": "horizontal", "bottom": "5%", "textStyle": {"fontSize": 14, "color": "#333"}},
        "series": [{
            "name": "Dinh dưỡng",
            "type": "pie",
            "radius": ["40%", "70%"],
            "center": ["50%", "40%"],
            "data": total_data
        }]
    }
    st_echarts(options=total_options, height="300px")

# Nhập thông tin món ăn từ người dùng
st.sidebar.header("📌 Nhập thông tin món ăn")
ten_mon_an = st.sidebar.text_input("Tên món ăn", "Món ăn của bạn")
calories = st.sidebar.number_input("Calories (kcal)", 0, 1000, 250)
protein = st.sidebar.number_input("Protein (g)", 0, 1000, 10)
fat = st.sidebar.number_input("Fat (g)", 0, 1000, 10)
carbs = st.sidebar.number_input("Carbonhydrates (g)", 0, 1000, 30)

if st.sidebar.button("➕ Thêm thức ăn"):
    new_meal = pd.DataFrame({
        'Calories (kcal)': [calories],
        'Protein (g)': [protein],
        'Fat (g)': [fat],
        'Carbonhydrates (g)': [carbs]
    })
    predicted_calo = model.predict(new_meal)[0]
    st.session_state.added_meals.append({
        "name": ten_mon_an,
        "calories": calories,
        "protein": protein,
        "fat": fat,
        "carbs": carbs,
        "calo_type": predicted_calo
    })
    st.rerun()

# Hiển thị danh sách món ăn dạng lưới
st.markdown("## 📝 Danh sách Bữa Ăn đã Thiết Kế")

if not st.session_state.added_meals:
    st.info("Chưa có thức ăn nào được thêm. Hãy nhập món ăn từ thanh bên trái! 🍽️")
else:
    cols = st.columns(3)
    to_remove = None  # Lưu món ăn cần xóa để tránh lỗi vòng lặp khi xóa trong danh sách

    for i, meal in enumerate(st.session_state.added_meals):
        with cols[i % 3]:
            st.markdown(f"### 🍽️ {meal['name']}")
            st.write(f"🔹 Calories: {meal['calories']} kcal")
            st.write(f"🔹 Protein: {meal['protein']} g")
            st.write(f"🔹 Fat: {meal['fat']} g")
            st.write(f"🔹 Carbs: {meal['carbs']} g")
            st.write(f"🔹 Nhóm dinh dưỡng: {meal['calo_type']}")

            if st.button(f"❌ Xóa {meal['name']}", key=f"delete_{i}"):
                to_remove = i  # Đánh dấu món ăn cần xóa

    # Thực hiện xóa món ăn ngoài vòng lặp để tránh lỗi
    if to_remove is not None:
        st.session_state.added_meals.pop(to_remove)
        st.rerun()

    # Nút xóa tất cả món ăn
    if st.button("🗑️ Xóa tất cả món ăn"):
        st.session_state.added_meals.clear()
        st.rerun()

