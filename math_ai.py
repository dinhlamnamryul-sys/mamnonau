import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé đếm cùng Thỏ Con",
    page_icon="🐰",
    layout="centered"
)

# ================== CSS GIAO DIỆN ĐẸP ==================
st.markdown("""
<style>
/* Nền ứng dụng */
.stApp { 
    background: linear-gradient(to bottom, #fffde7, #b3e5fc); 
}

/* Thẻ card trắng */
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border: 2px solid #fff;
}

/* Chữ to cho bé dễ đọc */
h1 { color: #d35400; font-family: 'Comic Sans MS', cursive; }
.big-text { font-size: 24px; color: #2c3e50; }
.emoji-display { font-size: 60px; line-height: 1.2; letter-spacing: 10px; }
.number-big { font-size: 50px; color: #e74c3c; font-weight: bold; }

/* Nút bấm câu trả lời */
div.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 24px;
    font-weight: bold;
    border-radius: 15px;
    background-color: #ffffff;
    border: 2px solid #4CAF50;
    color: #4CAF50;
    transition: all 0.3s;
}
div.stButton > button:hover {
    background-color: #4CAF50;
    color: white;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ================== DỮ LIỆU ==================
do_vat = {
    "🍎": "quả táo",
    "🐟": "con cá",
    "🌸": "bông hoa",
    "🐰": "con thỏ",
    "🍌": "quả chuối",
    "⭐": "ngôi sao",
    "🎈": "bóng bay"
}

chu_so = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

# ================== HÀM HỖ TRỢ ==================
def phat_am_thanh(text):
    """Phát âm thanh không cần lưu file (tránh lỗi file locked)"""
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang="vi")
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format="audio/mp3", autoplay=True)
    except Exception as e:
        st.warning(f"Lỗi âm thanh: {e}")

def tao_cau_hoi_moi():
    st.session_state.so = random.randint(1, 10)
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))
    # Tạo danh sách đáp án ngẫu nhiên cho trắc nghiệm
    dap_an_dung = st.session_state.so
    lua_chon = [dap_an_dung]
    while len(lua_chon) < 3:
        r = random.randint(1, 10)
        if r not in lua_chon:
            lua_chon.append(r)
    random.shuffle(lua_chon)
    st.session_state.lua_chon_buoc3 = lua_chon

def tao_cau_hoi_buoc4():
    # Tạo đáp án cho bước tìm số liền sau
    dap_an_dung = st.session_state.so + 1
    lua_chon = [dap_an_dung]
    while len(lua_chon) < 3:
        r = random.randint(1, 11) # Có thể lên tới 11
        if r not in lua_chon:
            lua_chon.append(r)
    random.shuffle(lua_chon)
    st.session_state.lua_chon_buoc4 = lua_chon

# ================== KHỞI TẠO STATE ==================
if "buoc" not in st.session_state:
    st.session_state.buoc = 1
    tao_cau_hoi_moi()

# ================== HEADER ==================
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80)
with col_h2:
    st.markdown("<h1>BÉ VUI HỌC TOÁN</h1>", unsafe_allow_html=True)

# Thanh tiến trình
progress = (st.session_state.buoc - 1) / 4
st.progress(progress)

# ================== ĐIỀU HƯỚNG ==================
if st.session_state.buoc > 1 and st.session_state.buoc < 5:
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("⬅️", help="Quay lại"):
            st.session_state.buoc -= 1
            st.rerun()

# ================== NỘI DUNG CHÍNH ==================

# --- BƯỚC 1: CHÀO HỎI ---
if st.session_state.buoc == 1:
    st.markdown("""
    <div class="card">
        <h2 style='color:#e67e22'>🐰 Xin chào bé yêu!</h2>
        <p class="big-text">Hôm nay Thỏ Con sẽ cùng bé học đếm nhé!</p>
        <p>Bé đã sẵn sàng chưa nào?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chỉ phát âm thanh 1 lần khi load trang
    if "welcomed" not in st.session_state:
        phat_am_thanh("Xin chào các bạn nhỏ! Hôm nay chúng mình cùng đếm số nhé!")
        st.session_state.welcomed = True

    if st.button("🚀 BẮT ĐẦU THÔI!", type="primary"):
        st.session_state.buoc = 2
        st.rerun()

# --- BƯỚC 2: HỌC ĐẾM ---
elif st.session_state.buoc == 2:
    st.markdown(f"""
    <div class="card">
        <p class="big-text">Bé hãy đếm xem có bao nhiêu <b>{st.session_state.ten}</b>?</p>
        <div class="emoji-display">{st.session_state.hinh * st.session_state.so}</div>
        <p class="big-text">Đáp án là số:</p>
        <p class="number-big">{st.session_state.so}</p>
        <p style="color:gray">({chu_so[st.session_state.so]})</p>
    </div>
    """, unsafe_allow_html=True)

    # Nút nghe lại
    if st.button("🔊 Nghe Thỏ đọc"):
        phat_am_thanh(f"Có {chu_so[st.session_state.so]} {st.session_state.ten}")

    st.write("")
    if st.button("➡️ Sang bài tập tiếp theo", type="primary"):
        st.session_state.buoc = 3
        st.rerun()

# --- BƯỚC 3: KIỂM TRA ĐẾM (TRẮC NGHIỆM) ---
elif st.session_state.buoc == 3:
    st.markdown(f"""
    <div class="card">
        <p class="big-text">Đố bé biết có bao nhiêu <b>{st.session_state.ten}</b>?</p>
        <div class="emoji-display">{st.session_state.hinh * st.session_state.so}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center'>Bé hãy chọn một số nhé:</h3>", unsafe_allow_html=True)
    
    # Hiển thị 3 nút bấm to
    cols = st.columns(3)
    for i, so in enumerate(st.session_state.lua_chon_buoc3):
        with cols[i]:
            if st.button(f"{so}", key=f"btn_b3_{i}"):
                if so == st.session_state.so:
                    st.success("Tuyệt vời! Bé chọn đúng rồi!")
                    phat_am_thanh("Hoan hô! Bé làm đúng rồi!")
                    time.sleep(1) # Đợi 1 chút cho bé nghe
                    tao_cau_hoi_buoc4() # Chuẩn bị cho bước 4
                    st.session_state.buoc = 4
                    st.rerun()
                else:
                    st.error("Chưa đúng, bé đếm lại nhé!")
                    phat_am_thanh("Sai rồi, con thử lại nhé!")

# --- BƯỚC 4: TÌM SỐ LIỀN SAU ---
elif st.session_state.buoc == 4:
    st.markdown(f"""
    <div class="card">
        <p class="big-text">Câu hỏi khó hơn nè!</p>
        <p class="big-text">Số nào đứng ngay sau số <b style='color:red; font-size:40px'>{st.session_state.so}</b>?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center'>Chọn đáp án đúng:</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    dap_an = st.session_state.so + 1
    
    for i, so in enumerate(st.session_state.lua_chon_buoc4):
        with cols[i]:
            if st.button(f"{so}", key=f"btn_b4_{i}"):
                if so == dap_an:
                    st.balloons()
                    phat_am_thanh("Xuất sắc! Con thông minh quá!")
                    time.sleep(1.5)
                    st.session_state.buoc = 5
                    st.rerun()
                else:
                    st.error(f"Sau số {st.session_state.so} không phải là {so} đâu.")
                    phat_am_thanh("Chưa đúng rồi, con suy nghĩ thêm nhé!")

# --- BƯỚC 5: KẾT THÚC ---
elif st.session_state.buoc == 5:
    st.markdown("""
    <div class="card" style="background-color: #e8f5e9;">
        <h1 style="color:green">🏆 CHÚC MỪNG BÉ!</h1>
        <p class="big-text">Con đã hoàn thành bài học rất xuất sắc.</p>
        <img src="https://media.giphy.com/media/u2pmTWUi0GjTO/giphy.gif" width="200">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 HỌC TIẾP CÂU KHÁC", type="primary"):
        tao_cau_hoi_moi()
        st.session_state.buoc = 2
        st.rerun()

# ================== FOOTER ==================
st.markdown("---")
st.caption("© 2025 – Sản phẩm AI Mầm Non - Nhóm tác giả: Lò Thị Hạnh - Quàng Thị Phương - Trần Thị Nguyệt Nga")
