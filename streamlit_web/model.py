import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier

# Hàm tính BMR
def compute_bmr_asian(gender, body_weight, body_height, age):
    if gender == 'male':
        return 66 + (13.7 * body_weight) + (5 * body_height) - (6.8 * age)
    elif gender == 'female':
        return 655 + (9.6 * body_weight) + (1.8 * body_height) - (4.7 * age)

# Hàm tính nhu cầu calo hàng ngày
def calculate_daily_calorie_needs(bmr, activity_level):
    activity_multipliers = {
        'ít vận động': 1.2,
        'vận động nhẹ': 1.375,
        'vận động vừa': 1.55,
        'vận động mạnh': 1.725,
        'vận động cực kỳ mạnh': 1.9
    }
    return bmr * activity_multipliers[activity_level]

# Hàm lọc món ăn theo mục tiêu
def filter_meals_by_goal(df, goal):
    if goal == 'Tăng cân':
        return df[df['Calorie Type'].isin(['Calo cao', 'Calo trung bình'])]
    elif goal == 'Giảm cân':
        return df[df['Calorie Type'].isin(['Calo thấp'])]
    elif goal == 'Duy trì':
        return df[df['Calorie Type'].isin(['Calo cao', 'Calo trung bình', 'Calo thấp'])]
    return df

# Hàm lọc món ăn theo bữa và lượng calo
def filter_meals_by_time(df, calorie_limit):
    return df[df['Calories (kcal)'] <= calorie_limit]

# Hàm chọn ngẫu nhiên món ăn
def suggest_random_meal(df, calorie_limit, n=5):
    filtered = filter_meals_by_time(df, calorie_limit)
    return filtered.sample(n=min(n, len(filtered)))

# Hàm huấn luyện mô hình KMeans
def train_kmeans(df, cols_to_convert, n_clusters=3):
    X = df[cols_to_convert]
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    return kmeans, X_scaled

# Hàm huấn luyện mô hình Decision Tree
def train_decision_tree(X_train, y_train, max_depth=2):
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model
