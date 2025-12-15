import streamlit as st
import random

# ------------------ CẤU HÌNH TRANG ------------------
st.set_page_config(
    page_title="Bé đếm cùng Thỏ Con",
    page_icon="🐰",
    layout="centered"
)

# ------------------ CSS THÂN THIỆN MẦM NON ------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #fffde7, #e1f5fe);
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    font-size: 26px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.stButton>button {
    font-size: 22px;
    border-radius: 20px;
    padding: 10px 25px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<div class="card">
    <h1>🐰 AI “BÉ ĐẾM CÙNG THỎ CON”</h1>
    <p>Học đếm số từ 1 đến 10</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------ DỮ LIỆU ------------------
do_vat = {
    "🍎": "quả táo",
    "🐟": "con cá",
    "🌸": "bông hoa",
    "🐰": "con thỏ",
    "🍌": "quả chuối"
}

chu_so = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

# ------------------ SESSION STATE ------------------
if "so" not in st.session_state:
    st.session_state.so = 0
    st.session_state.hinh = ""
    st.session_state.ten = ""

# ------------------ BƯỚC 1: KHỞI ĐỘNG ------------------
st.subheader("👋 Thỏ Con chào bé!")
st.info("🐰 Xin chào các bạn nhỏ! Hôm nay chúng mình cùng đếm số nhé!")

# ------------------ BƯỚC 2: HỌC ĐẾM ------------------
if st.button("🎲 BẮT ĐẦU HỌC ĐẾM"):
    st.session_state.so = random.randint(1, 10)
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))

# ------------------ HIỂN THỊ ------------------
if st.session_state.so > 0:
    st.markdown(f"""
    <div class="card">
        <p>🐰 Bé hãy đếm xem có bao nhiêu {st.session_state.ten} nhé!</p>
        <p style="font-size:45px;">
        {st.session_state.hinh * st.session_state.so}
        </p>
        <p>👉 AI đọc: <b>{chu_so[st.session_state.so]}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ BƯỚC 3: TƯƠNG TÁC ------------------
    tra_loi = st.number_input(
        "🖐️ Bé chọn số đúng:",
        min_value=1,
        max_value=10,
        step=1
    )

    if st.button("✅ KIỂM TRA"):
        if tra_loi == st.session_state.so:
            st.balloons()
            st.success("🎉 GIỎI QUÁ! BÉ TRẢ LỜI ĐÚNG RỒI!")
        else:
            st.warning("😊 CHƯA ĐÚNG, BÉ ĐẾM LẠI NHÉ!")

# ------------------ BƯỚC 5: KẾT THÚC ------------------
st.markdown("---")
st.caption("🐰 Hôm nay con học rất giỏi, hẹn gặp lại nhé!")

