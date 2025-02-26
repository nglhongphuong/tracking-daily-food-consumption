import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Gợi Ý Món Ăn", layout="wide")

# Hàm tính BMI
def compute_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

# Hàm phân loại BMI
def bmi_category(bmi):
    if bmi < 18.5:
        return "Gầy", "Bạn nên tăng cường dinh dưỡng và tập luyện để đạt cân nặng hợp lý. Hãy bổ sung thực phẩm giàu protein, chất béo lành mạnh và tập thể dục đều đặn."
    elif 18.5 <= bmi < 24.9:
        return "Bình thường", "Chúc mừng! Bạn có chỉ số BMI lý tưởng. Hãy duy trì chế độ ăn uống cân bằng và tập thể dục để giữ gìn sức khỏe."
    elif 25 <= bmi < 29.9:
        return "Thừa cân", "Bạn cần kiểm soát lượng calo nạp vào và tăng cường vận động. Hãy ưu tiên thực phẩm giàu chất xơ, ít đường và thường xuyên tập luyện."
    else:
        return "Béo phì", "Cảnh báo! Bạn có nguy cơ mắc các bệnh liên quan đến béo phì. Hãy xây dựng chế độ ăn uống lành mạnh, giảm tinh bột, đường và tăng cường hoạt động thể chất."




# Hàm tính BMR
def compute_bmr_asian(gender, weight, height, age):
    if gender == 'Nam':
        return round(66 + (13.7 * weight) + (5 * height) - (6.8 * age), 2)
    else:
        return round(655 + (9.6 * weight) + (1.8 * height) - (4.7 * age), 2)

# Hàm tính tổng calo cần thiết
def calculate_daily_calories(bmr, activity_level):
    activity_multipliers = {
        'Ít vận động': 1.2,
        'Vận động nhẹ': 1.375,
        'Vận động vừa': 1.55,
        'Vận động mạnh': 1.725,
        'Vận động rất mạnh': 1.9
    }
    return round(bmr * activity_multipliers.get(activity_level, 1.2), 2)


def suggest_meals(filtered_df,calories):
    return filtered_df[filtered_df["Calories (kcal)"] <= calories].sample(n=min(5, len(filtered_df)))


# Hàm tính tổng dinh dưỡng từ các món đã chọn
def get_nutrition_total():
    selected_meals = [
        st.session_state.breakfast_options[st.session_state.breakfast_options["TÊN THỨC ĂN"] == st.session_state["selected_breakfast"]],
        st.session_state.lunch_options[st.session_state.lunch_options["TÊN THỨC ĂN"] == st.session_state["selected_lunch"]],
        st.session_state.dinner_options[st.session_state.dinner_options["TÊN THỨC ĂN"] == st.session_state["selected_dinner"]]
    ]

    total_nutrition = {
        "Calories (kcal)": 0,
        "Protein (g)": 0,
        "Fat (g)": 0,
        "Carbonhydrates (g)": 0,
        "Chất xơ (g)": 0,
        "Cholesterol (mg)": 0,
        "Canxi (mg)": 0,
        "Photpho (mg)": 0,
        "Sắt (mg)": 0,
        "Natri (mg)": 0,
        "Kali (mg)": 0,
        "Beta Caroten (mcg)": 0,
        "Vitamin A (mcg)": 0,
        "Vitamin B1 (mg)": 0,
        "Vitamin C (mg)": 0
    }

    for meal in selected_meals:
        if not meal.empty:
            for key in total_nutrition.keys():
                try:
                    total_nutrition[key] += float(meal[key].values[0])
                except ValueError:
                    print(f"Warning: Could not convert value {meal[key].values[0]} for key {key}")

    return total_nutrition


st.title("🍽️ Gợi Ý Bữa Ăn Cá Nhân Hóa Cho Bạn")

# Thiết kế form nhập thông tin
with st.form(key="personal_info_form"):
    st.markdown("### 🔍 Thông tin cơ bản")

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Giới tính", ['Nam', 'Nữ'])
        weight = st.number_input("Cân nặng (kg)", min_value=1, value=60)
        age = st.number_input("Tuổi", min_value=1, value=25)

    with col2:
        height = st.number_input("Chiều cao (cm)", min_value=1, value=160)
        activity_level = st.selectbox("Mức độ vận động",
                                      ['Ít vận động', 'Vận động nhẹ', 'Vận động vừa', 'Vận động mạnh',
                                       'Vận động rất mạnh'])
        goal = st.selectbox("Mục tiêu", ['Tăng cân', 'Giảm cân', 'Duy trì'])

    submit_button = st.form_submit_button("📊 Tính toán & Xem gợi ý")

# Lưu trạng thái tính toán
if "bmi" not in st.session_state:
    st.session_state.bmi = None
if "bmr" not in st.session_state:
    st.session_state.bmr = None
if "daily_calories" not in st.session_state:
    st.session_state.daily_calories = None
if "breakfast_options" not in st.session_state:
    st.session_state.breakfast_options = None
if "lunch_options" not in st.session_state:
    st.session_state.lunch_options = None
if "dinner_options" not in st.session_state:
    st.session_state.dinner_options = None

if submit_button:
    st.success("✅ Thông tin đã được cập nhật! Đang tính toán...")
    # Tải dữ liệu thức ăn
    sheet_id = "1mjMrweeCQVRrOiqQRkJGe66DWbzTKsJh"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    df = pd.read_csv(csv_url).dropna().reset_index(drop=True)
    df["Calories (kcal)"] = pd.to_numeric(df["Calories (kcal)"], errors='coerce')

    # Phân nhóm calo bằng KMeans
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[["Calories (kcal)"]])
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Calorie Type"] = kmeans.fit_predict(df_scaled)
    df["Calorie Type"] = df["Calorie Type"].map({0: 'Calo thấp', 1: 'Calo trung bình', 2: 'Calo cao'})

    # Lọc thức ăn phù hợp
    if goal == 'Tăng cân':
        filtered_df = df[df["Calorie Type"].isin(['Calo trung bình', 'Calo cao'])]
    elif goal == 'Giảm cân':
        filtered_df = df[df["Calorie Type"] == 'Calo thấp']
    else:
        filtered_df = df
    st.session_state.bmi = compute_bmi(weight, height)
    st.session_state.bmr = compute_bmr_asian(gender, weight, height, age)
    st.session_state.daily_calories = calculate_daily_calories(st.session_state.bmr, activity_level)
    st.session_state.breakfast_options = suggest_meals(filtered_df,round(st.session_state.daily_calories * 0.3, 2))
    st.session_state.lunch_options = suggest_meals(filtered_df,round(st.session_state.daily_calories * 0.4, 2))
    st.session_state.dinner_options = suggest_meals(filtered_df,round(st.session_state.daily_calories * 0.3, 2))

# Hiển thị kết quả BMI và calo nếu đã tính
if st.session_state.bmi is not None:
    bmi_status,advice = bmi_category(st.session_state.bmi)

    st.subheader("📌 Tình trạng cơ thể")
    st.markdown(f"""
        **📝 Chỉ số BMI:** `{st.session_state.bmi}` ({bmi_status})  
        🔥 **BMR:** `{st.session_state.bmr} kcal/ngày`  
        ⚡ **Nhu cầu calo/ngày:** `{st.session_state.daily_calories} kcal`  
        💡 **Lời khuyên:** *{advice}*  
        """, unsafe_allow_html=True)


    st.subheader("🍛 Gợi Ý Món Ăn")

    col1, col2, col3 = st.columns(3)

    def select_meal(meal_name, meal_options):
        key = f"selected_{meal_name}"
        st.write(meal_options[["TÊN THỨC ĂN","Calories (kcal)","Protein (g)","Fat (g)","Carbonhydrates (g)","Chất xơ (g)","Cholesterol (mg)","Canxi (mg)","Photpho (mg)","Sắt (mg)","Natri (mg)","Kali (mg)","Beta Caroten (mcg)","Vitamin A (mcg)","Vitamin B1 (mg)","Vitamin C (mg)","Loại"]])
        if key not in st.session_state:
            st.session_state[key] = meal_options["TÊN THỨC ĂN"].tolist()[0] if not meal_options.empty else "Không có gợi ý"

        selected_meal = st.selectbox(f"Chọn món ({meal_name})",
                                     meal_options["TÊN THỨC ĂN"].tolist() if not meal_options.empty else ["Không có gợi ý"],
                                     key=key)
        st.write(f"**Món đã chọn:** {st.session_state[key]}")
        # Lấy dòng thức ăn được chọn
        selected_info = meal_options[meal_options["TÊN THỨC ĂN"] == st.session_state[key]]
        if not selected_info.empty:
            # Hiển thị hình ảnh nếu có
            image_url = selected_info["Hình"].values[0]  # Lấy đường dẫn ảnh từ DataFrame
            if image_url and isinstance(image_url, str):
                # Dùng markdown với CSS để đặt kích thước ảnh cố định
                st.markdown(
                    f"""
                                <div style="display: flex; justify-content: center;">
                                    <img src="{image_url}" style="width: 300px; height: 250px; object-fit: cover; border-radius: 10px;padding:5px;">
                                </div>
                                """,
                    unsafe_allow_html=True
                )


    with col1:
        st.markdown(f"### 🍳 Buổi sáng ({round(st.session_state.daily_calories * 0.3, 2)} kcal)")
        select_meal("breakfast", st.session_state.breakfast_options)

    with col2:
        st.markdown(f"### 🍛 Buổi trưa ({round(st.session_state.daily_calories * 0.4, 2)} kcal)")
        select_meal("lunch", st.session_state.lunch_options)

    with col3:
        st.markdown(f"### 🌙 Buổi tối ({round(st.session_state.daily_calories * 0.3, 2)} kcal)")
        select_meal("dinner", st.session_state.dinner_options)

    # Lấy tổng dữ liệu dinh dưỡng
    nutrition_total = get_nutrition_total()

    import streamlit as st
    from streamlit_echarts import st_echarts

    # Chuẩn bị dữ liệu cho biểu đồ tròn
    data = [
        {"value": nutrition_total["Calories (kcal)"], "name": "Calories (kcal)"},
        {"value": nutrition_total["Protein (g)"], "name": "Protein (g)"},
        {"value": nutrition_total["Fat (g)"], "name": "Fat (g)"},
        {"value": nutrition_total["Carbonhydrates (g)"], "name": "Carbs (g)"},
        {"value": nutrition_total["Chất xơ (g)"], "name": "Chất xơ (g)"},
        {"value": nutrition_total["Cholesterol (mg)"], "name": "Cholesterol (g)"},
        {"value": nutrition_total["Canxi (mg)"], "name": "Canxi (mg)"},
        {"value": nutrition_total["Photpho (mg)"], "name": "Photpho (mg)"},
        {"value": nutrition_total["Sắt (mg)"], "name": "Sắt (mg)"},
        {"value": nutrition_total["Natri (mg)"], "name": "Natri (mg)"},
        {"value": nutrition_total["Kali (mg)"], "name": "Kali (mg)"},
        {"value": nutrition_total["Beta Caroten (mcg)"], "name": "Beta Caroten (mcg)"},
        {"value": nutrition_total["Vitamin A (mcg)"], "name": "Vitamin A (mcg)"},
        {"value": nutrition_total["Vitamin B1 (mg)"], "name": "Vitamin B1 (mg)"},
        {"value": nutrition_total["Vitamin C (mg)"], "name": "Vitamin C (mg)"}
    ]
    st.markdown("## 📊 Tổng Quan Dinh Dưỡng")

    # Cấu hình biểu đồ
    option = {
        "title": {
            "left": "center",
            "top": "2%",
            "textStyle": {"fontSize": 18, "fontWeight": "bold", "color": "#333"},
        },
        "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
        "legend": {
            "orient": "horizontal",
            "bottom": "5%",  # Đưa chú thích lên cao hơn
            "textStyle": {"fontSize": 14, "color": "#333"},
        },
        "series": [
            {
                "name": "Dinh dưỡng",
                "type": "pie",
                "radius": ["40%", "70%"],  # Donut Chart
                "center": ["50%", "40%"],  # Di chuyển biểu đồ lên trên
                "avoidLabelOverlap": True,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 3,
                },
                "label": {
                    "show": False,
                    "position": "outside",
                    "formatter": "{b}: {c}",
                    "fontSize": 12,
                    "color": "#333",
                },
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": 16,
                        "fontWeight": "bold",
                        "color": "#E91E63",
                    }
                },
                "labelLine": {"show": True, "smooth": 0.2},
                "data": [
                    {
                        **item,
                        "itemStyle": {
                            "color": f"rgba({i * 40 % 255},{(i * 70) % 255},{(i * 100) % 255}, 0.8)"
                        },
                    }
                    for i, item in enumerate(data)
                ],
            }
        ],
    }

    # Hiển thị biểu đồ
    st_echarts(options=option, height="400px")  # Tăng chiều cao để tránh bị che
