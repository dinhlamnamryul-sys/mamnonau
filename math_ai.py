import streamlit as st
import random
from gtts import gTTS
import uuid, os

# ================== HÀM AI ĐỌC ==================
def ai_noi(text):
    filename = f"voice_{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang="vi")
    tts.save(filename)
    audio = open(filename, "rb").read()
    st.audio(audio, format="audio/mp3", autoplay=True)
    os.remove(filename)

# ================== ÂM THANH HOAN HÔ / ĐỘNG VIÊN ==================
def phat_am_thanh(mp3_text):
    filename = f"sound_{uuid.uuid4()}.mp3"
    tts = gTTS(text=mp3_text, lang="vi")
    tts.save(filename)
    audio = open(filename, "rb").read()
    st.audio(audio, format="audio/mp3", autoplay=True)
    os.remove(filename)

# ================== CẤU HÌNH ==================
st.set_page_config(
    page_title="Bé đếm cùng Thỏ Con",
    page_icon="🐰",
    layout="centered"
)

# ================== CSS ==================
st.markdown("""
<style>
.stApp { background: linear-gradient(to bottom, #fffde7, #e1f5fe); }
.card {
    background: white;
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    font-size: 26px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.big { font-size: 48px; }
.stButton>button {
    font-size: 22px;
    border-radius: 20px;
    padding: 10px 25px;
}
</style>
""", unsafe_allow_html=True)

# ================== DỮ LIỆU ==================
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

# ================== SESSION ==================
if "buoc" not in st.session_state:
    st.session_state.buoc = 1
    st.session_state.so = random.randint(1, 10)
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))

# ================== HEADER ==================
st.markdown("""
<div class="card">
<h1>🐰 AI “BÉ ĐẾM CÙNG THỎ CON”</h1>
<p>Học đếm số từ 1 đến 10</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================== BƯỚC 1 ==================
if st.session_state.buoc == 1:
    st.markdown("""
    <div class="card">
    🐰 Xin chào các bạn nhỏ!<br>
    Hôm nay chúng mình cùng đếm số nhé!
    </div>
    """, unsafe_allow_html=True)
    ai_noi("Xin chào các bạn nhỏ! Hôm nay chúng mình cùng đếm số nhé!")

    if st.button("👉 BẮT ĐẦU"):
        st.session_state.buoc = 2

# ================== BƯỚC 2 ==================
elif st.session_state.buoc == 2:
    st.markdown(f"""
    <div class="card">
    🐰 Bé hãy đếm cùng Thỏ Con nhé!
    <p class="big">{st.session_state.hinh * st.session_state.so}</p>
    👉 AI đọc: <b>{chu_so[st.session_state.so]}</b>
    </div>
    """, unsafe_allow_html=True)

    ai_noi(chu_so[st.session_state.so])

    if st.button("➡️ LUYỆN TẬP"):
        st.session_state.buoc = 3

# ================== BƯỚC 3: KIỂM TRA (TỰ PHÁT ÂM THANH) ==================
elif st.session_state.buoc == 3:
    st.markdown(f"""
    <div class="card">
    🐰 Có bao nhiêu {st.session_state.ten}?
    <p class="big">{st.session_state.hinh * st.session_state.so}</p>
    </div>
    """, unsafe_allow_html=True)

    tra_loi = st.number_input("👉 Bé chọn số:", 1, 10, 1)

    if st.button("✅ KIỂM TRA"):
        if tra_loi == st.session_state.so:
            st.balloons()
            phat_am_thanh("Hoan hô! Bé làm đúng rồi!")
            st.success("🎉 Giỏi quá!")
            st.session_state.buoc = 4
        else:
            phat_am_thanh("Chưa đúng rồi! Con thử lại nhé!")
            st.warning("😊 Chưa đúng rồi!")

# ================== BƯỚC 4 ==================
elif st.session_state.buoc == 4:
    dap_an = st.session_state.so + 1
    st.markdown("""
    <div class="card">
    🐰 Số nào đứng sau số này?
    </div>
    """, unsafe_allow_html=True)
    st.write(f"Số: **{st.session_state.so}**")

    tra_loi = st.number_input("👉 Bé trả lời:", 1, 10, 1)

    if st.button("✅ KIỂM TRA"):
        if tra_loi == dap_an:
            st.balloons()
            phat_am_thanh("Rất giỏi! Con trả lời đúng!")
            st.session_state.buoc = 5
        else:
            phat_am_thanh("Con suy nghĩ lại nhé!")
            st.warning("😊 Chưa đúng!")

# ================== BƯỚC 5 ==================
elif st.session_state.buoc == 5:
    st.balloons()
    st.markdown("""
    <div class="card">
    🐰 Hôm nay con học rất giỏi!<br>
    Hẹn gặp lại lần sau nhé!
    </div>
    """, unsafe_allow_html=True)
    ai_noi("Hôm nay con học rất giỏi! Hẹn gặp lại lần sau!")

    if st.button("🔄 HỌC LẠI"):
        st.session_state.buoc = 1

st.markdown("---")
st.caption("© 2025 – AI mầm non | Phục vụ giáo dục & chuyển đổi số")
