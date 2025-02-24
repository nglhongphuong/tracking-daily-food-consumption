import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.write("# Chào mừng bạn đến với website theo dõi thực phẩm ăn hằng ngày! 👋")

st.sidebar.success("Trang chủ")

st.markdown(
    """
    Ứng dụng ... bằng Scikit-Learn and Streamlit.
    """
)