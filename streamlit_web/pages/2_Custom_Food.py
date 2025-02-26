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

cols_to_convert = [col for col in df.columns if col not in ["TÊN THỨC ĂN", "Loại","Hình"]]
df[cols_to_convert] = df[cols_to_convert].replace({',': '', ' ': '', 'NA': None}, regex=True)
df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
df[cols_to_convert] = df[cols_to_convert].fillna(df[cols_to_convert].mean()).astype(int)

# Phân nhóm calo bằng KMeans
# Chọn các cột số học từ DataFrame
X = df[cols_to_convert]
cols = X.columns

# Chuẩn hóa dữ liệu số
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(X)
df_scaled = pd.DataFrame(df_scaled, columns=[cols])


kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 42)
df["Calorie Type"] = kmeans.fit_predict(df_scaled)
df["Calorie Type"] = df["Calorie Type"].map({0: 'Calo thấp', 1: 'Calo trung bình', 2: 'Calo cao'})

# Huấn luyện mô hình Decision Tree
X_train = df[cols_to_convert]
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
calories = st.sidebar.number_input("Calories (kcal)", 0, 1000, 5)
protein = st.sidebar.number_input("Protein (g)", 0, 1000, 100)
fat = st.sidebar.number_input("Fat (g)", 0, 1000, 10)
carbs = st.sidebar.number_input("Carbonhydrates (g)", 0, 1000, 30)
fiber = st.sidebar.number_input("Chất xơ (g)", 0, 100, 5)
cholesterol = st.sidebar.number_input("Cholesterol (mg)", 0, 5000, 3000)
canxi = st.sidebar.number_input("Canxi (mg)", 0, 1000, 100)
photpho = st.sidebar.number_input("Photpho (mg)", 0, 1000, 100)
sat = st.sidebar.number_input("Sắt (mg)", 0, 100, 10)
natri = st.sidebar.number_input("Natri (mg)", 0, 5000, 500)
kali = st.sidebar.number_input("Kali (mg)", 0, 5000, 1000)
beta_caroten = st.sidebar.number_input("Beta Caroten (mcg)", 0, 5000, 500)
vitamin_a = st.sidebar.number_input("Vitamin A (mcg)", 0, 5000, 500)
vitamin_b1 = st.sidebar.number_input("Vitamin B1 (mg)", 0, 100, 2)
vitamin_c = st.sidebar.number_input("Vitamin C (mg)", 0, 500, 50)



if st.sidebar.button("➕ Thêm thức ăn"):
    new_meal = pd.DataFrame({
        'Calories (kcal)': [calories],
        'Protein (g)': [protein],
        'Fat (g)': [fat],
        'Carbonhydrates (g)': [carbs],
        'Chất xơ (g)': [fiber],
        'Cholesterol (mg)': [cholesterol],
        'Canxi (mg)': [canxi],
        'Photpho (mg)': [photpho],
        'Sắt (mg)': [sat],
        'Natri (mg)': [natri],
        'Kali (mg)': [kali],
        'Beta Caroten (mcg)': [beta_caroten],
        'Vitamin A (mcg)': [vitamin_a],
        'Vitamin B1 (mg)': [vitamin_b1],
        'Vitamin C (mg)': [vitamin_c]
    })
    predicted_calo = model.predict(new_meal)[0]
    st.session_state.added_meals.append({
        "name": ten_mon_an,
        "calories": calories,
        "protein": protein,
        "fat": fat,
        "carbs": carbs,
           "fiber": fiber,
        "cholesterol": cholesterol,
        "canxi": canxi,
        "photpho": photpho,
        "sat": sat,
        "natri": natri,
        "kali": kali,
        "beta_caroten": beta_caroten,
        "vitamin_a": vitamin_a,
        "vitamin_b1": vitamin_b1,
        "vitamin_c": vitamin_c,
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
            with st.expander("Xem chi tiết dinh dưỡng"):
                st.write(f"🔹 Chất xơ: {meal['fiber']} g ")
                st.write(f"🔹 Cholesterol: {meal['cholesterol']} mg ")
                st.write(f"🔹 Canxi: {meal['canxi']} mg")
                st.write(f"🔹 Sắt: {meal['sat']} mg ")
                st.write(f"🔹 Natri: {meal['natri']} mg ")
                st.write(f"🔹 Kali: {meal['kali']} mg ")
                st.write(f"🔹 Beta Caroten: {meal['beta_caroten']} mcg")
                st.write(f"🔹 Vitamin A: {meal['vitamin_a']} mcg")
                st.write(f"🔹 Vitamin B1: {meal['vitamin_b1']} mg")
                st.write(f"🔹 Vitamin C: {meal['vitamin_c']} mg")
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

