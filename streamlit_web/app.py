import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Tracking Daily Food",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
    <style>
        .title { text-align: center; font-size: 36px; font-weight: bold; color: #ff6347; }
        .subtitle { text-align: center; font-size: 20px; color: #666; }
        .container { background-color: #f9f9f9; padding: 20px; border-radius: 10px; 
                     box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); margin: auto; }
        .button-container { text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# Chia layout thành 2 cột (4/5 và 1/5)
col_left, col_right = st.columns([4, 1])

# Cột nội dung (4/5)
with col_left:
    st.markdown('<p class="title">🍽️ Theo dõi Thực phẩm Hằng ngày 🍽️</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Quản lý chế độ ăn uống và theo dõi dinh dưỡng dễ dàng!</p>', unsafe_allow_html=True)

    st.markdown("""
    ## 📌 Giới thiệu ứng dụng  
    **Tracking Daily Food** giúp bạn dễ dàng theo dõi chế độ ăn uống và kiểm soát dinh dưỡng hàng ngày:
    - 🥗 **Gợi ý bữa ăn** dựa trên chiều cao, cân nặng, tuổi và giới tính.
    - 🔎 **Tra cứu thực phẩm** để xem giá trị dinh dưỡng chi tiết.
    - 🍻 **Thiết kế bữa ăn** phù hợp với nhu cầu và sở thích cá nhân.

    ### 👩‍💻 Công nghệ áp dụng
    Ứng dụng được xây dựng bằng các công nghệ:
    - 💪 **Scikit-Learn**: Thư viện để phân tích dữ liệu và xây dựng mô hình gợi ý.
    - 🌟 **Streamlit**: Framework để phát triển giao diện tương tác.
    - 📊 **KMeans & Decision Tree**: Mô hình để phân nhóm calo và phân loại bữa ăn.

    ### 🔗 Liên kết
    - Mã nguồn: [GitHub Repository](https://github.com/nglhongphuong/tracking-daily-food-consumption)
    """, unsafe_allow_html=True)

    # Hiển thị thông tin phiên bản
    st.markdown('<p class="version">Phiên bản: 1.0 | Ngày tạo: Tháng 2/2025</p>', unsafe_allow_html=True)

    # Nút điều hướng đến các trang chính
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗉 Gợi ý bữa ăn"):
            st.switch_page("pages/1_Diet_Recommend_Food.py")

    with col2:
        if st.button("📊 Tra cứu thực phẩm"):
            st.switch_page("pages/3_Nutri_Finder.py")

    with col3:
        if st.button("🔍 Thiết kế bữa ăn"):
            st.switch_page("pages/2_Custom_Food.py")

    st.markdown('</div>', unsafe_allow_html=True)

# Cột ảnh (1/5)
with col_right:
    st.image("https://i.pinimg.com/736x/57/0a/44/570a44884ac94b65c42415c7e777117c.jpg", use_container_width=True)
    st.image("https://i.pinimg.com/736x/51/80/91/5180913728f4a702bfc359d0e9adf79f.jpg", use_container_width=True)
