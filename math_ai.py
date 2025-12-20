import streamlit as st
import random
from gtts import gTTS
import uuid
import os
import time

# ================== CẤU HÌNH TRANG (Phải để đầu tiên) ==================
st.set_page_config(
    page_title="Vườn Thỏ Diệu Kỳ",
    page_icon="🐰",
    layout="centered"
)

# ================== HÀM PHÁT ÂM THANH (Cải tiến) ==================
def phat_am_thanh(text):
    try:
        filename = f"sound_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang="vi")
        tts.save(filename)
        # Đọc file audio
        audio_file = open(filename, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        audio_file.close()
        # Xóa file sau khi đọc xong
        os.remove(filename)
    except Exception as e:
        # Nếu lỗi âm thanh thì bỏ qua, không làm crash app
        pass

# ================== LOGIC GAME ==================
# Dữ liệu
do_vat = {
    "🍎": "quả táo",
    "🐟": "chú cá",
    "🌸": "bông hoa",
    "🐰": "bạn thỏ",
    "🍌": "quả chuối",
    "⭐": "ngôi sao",
    "🎈": "bóng bay"
}

chu_so = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

# Khởi tạo Session
if "buoc" not in st.session_state:
    st.session_state.buoc = 1
    st.session_state.so = 1
    st.session_state.hinh = "🍎"
    st.session_state.ten = "quả táo"
    # Logic tạo câu hỏi đầu tiên
    st.session_state.so = random.randint(1, 5) # Mới đầu học số nhỏ thôi
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))

def tao_cau_hoi_moi():
    st.session_state.so = random.randint(1, 10)
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))

# ================== CSS "LONG LANH" (Trang trí) ==================
st.markdown("""
<style>
    /* Nhúng font chữ dễ thương từ Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;800&display=swap');

    /* 1. Nền trang web: Gradient màu kẹo ngọt */
    .stApp {
        background: linear-gradient(to bottom, #FFDEE9 0%, #B5FFFC 100%);
        font-family: 'Baloo 2', cursive;
    }

    /* 2. Thẻ bài học (Card): Bo tròn, đổ bóng nổi */
    .game-card {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 30px;
        border-radius: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 4px solid #fff;
    }

    /* 3. Tiêu đề to, rõ ràng */
    h1 {
        color: #FF6F61;
        text-shadow: 2px 2px 0px #fff;
        font-weight: 800;
        text-align: center;
    }

    /* 4. Số và Emoji to đùng cho bé dễ nhìn */
    .big-icon { font-size: 60px; line-height: 1.2; animation: bounce 2s infinite; }
    .big-text { font-size: 30px; color: #00838F; font-weight: bold; }
    
    /* 5. Nút bấm (Button): Tròn, màu sắc sặc sỡ */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        font-size: 22px;
        font-weight: bold;
        padding: 10px 0;
        background-color: #FF9A8B;
        background-image: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
        color: white;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 106, 136, 0.4);
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        color: #fff;
    }

    /* 6. Ô nhập số: Căn giữa, chữ to */
    .stNumberInput input {
        text-align: center;
        font-size: 30px;
        color: #FF6F61;
        font-weight: bold;
        border-radius: 15px;
    }

    /* Hiệu ứng nhún nhảy nhẹ */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Ẩn menu mặc định của Streamlit cho gọn */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== GIAO DIỆN CHÍNH ==================

# 1. Tiêu đề chung
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Bạn có thể thay bằng st.image("image_ac158d.png") nếu file ảnh nằm cùng thư mục
    st.markdown("<div style='font-size:60px; text-align:center;'>🐰</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1>VƯỜN THỎ DIỆU KỲ</h1>", unsafe_allow_html=True)

# 2. Nội dung thay đổi theo từng bước
placeholder = st.empty()

# --- BƯỚC 1: MÀN HÌNH CHÀO ---
if st.session_state.buoc == 1:
    with placeholder.container():
        st.markdown("""
        <div class="game-card">
            <p class="big-text">Xin chào bé yêu! 👋</p>
            <p>Hôm nay Thỏ Con sẽ cùng bé tập đếm nhé!</p>
            <div style="font-size: 80px;">🏰 🌈 🍄</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chỉ phát âm thanh 1 lần khi load trang
        if 'da_chao' not in st.session_state:
            phat_am_thanh("Xin chào bé yêu! Hôm nay Thỏ Con sẽ cùng bé tập đếm nhé!")
            st.session_state.da_chao = True
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🚀 BẮT ĐẦU NÀO"):
                st.session_state.buoc = 2
                st.rerun()

# --- BƯỚC 2: HỌC ĐẾM (HIỂN THỊ) ---
elif st.session_state.buoc == 2:
    with placeholder.container():
        st.markdown(f"""
        <div class="game-card">
            <p class="big-text">Bé đếm cùng Thỏ nhé!</p>
            <div class="big-icon">
                {' '.join([st.session_state.hinh] * st.session_state.so)}
            </div>
            <hr>
            <p style="font-size: 24px; color: #555;">Đây là số:</p>
            <h1 style="color: #FF4081; font-size: 50px;">{st.session_state.so} - {chu_so[st.session_state.so]}</h1>
        </div>
        """, unsafe_allow_html=True)

        phat_am_thanh(f"Có {st.session_state.so} {st.session_state.ten}. Số {chu_so[st.session_state.so]}")
        time.sleep(1) # Đợi xíu cho bé nghe

        if st.button("👉 SANG BÀI TẬP"):
            st.session_state.buoc = 3
            st.rerun()

# --- BƯỚC 3: BÀI TẬP ĐẾM ---
elif st.session_state.buoc == 3:
    with placeholder.container():
        st.markdown(f"""
        <div class="game-card">
            <p class="big-text">Đố bé biết có bao nhiêu {st.session_state.ten}?</p>
            <div class="big-icon">
                {' '.join([st.session_state.hinh] * st.session_state.so)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Input nhập số được làm đẹp bằng CSS ở trên
        tra_loi = st.number_input("Bé chọn số ở đây nhé:", 1, 20, 1)

        col_check, col_next = st.columns(2)
        with col_check:
            if st.button("Kiểm tra ✅"):
                if tra_loi == st.session_state.so:
                    st.balloons() # Hiệu ứng bóng bay
                    phat_am_thanh("Hoan hô! Bé giỏi quá! Đúng rồi!")
                    time.sleep(1)
                    st.session_state.buoc = 4
                    st.rerun()
                else:
                    st.error("Chưa đúng rồi, bé đếm lại kỹ hơn nhé!")
                    phat_am_thanh("Tiếc quá, chưa đúng rồi. Bé thử lại nhé!")
        
        with col_next:
            if st.button("Đổi câu khác 🔄"):
                tao_cau_hoi_moi()
                st.session_state.buoc = 2
                st.rerun()

# --- BƯỚC 4: BÀI TẬP TƯ DUY (+1) ---
elif st.session_state.buoc == 4:
    dap_an = st.session_state.so + 1
    with placeholder.container():
        st.markdown(f"""
        <div class="game-card">
            <p class="big-text">Câu hỏi khó hơn nè! 🧠</p>
            <p>Số nào đứng sau số <b>{st.session_state.so}</b>?</p>
            <div style="font-size: 40px; margin: 20px;">
                {st.session_state.so} ➡️ ❓
            </div>
        </div>
        """, unsafe_allow_html=True)

        tra_loi = st.number_input("Số tiếp theo là:", 1, 20, 1)

        if st.button("Trả lời 🎁"):
            if tra_loi == dap_an:
                st.snow() # Hiệu ứng tuyết rơi/phao giấy
                phat_am_thanh("Xuất sắc! Bé rất thông minh!")
                st.success(f"Chính xác! Sau số {st.session_state.so} là số {dap_an}")
                time.sleep(2)
                st.session_state.buoc = 5
                st.rerun()
            else:
                phat_am_thanh("Sai rồi. Bé nhớ lại dãy số nhé!")
                st.warning("Gợi ý: Bé cộng thêm 1 vào nhé!")

# --- BƯỚC 5: KẾT THÚC & CHƠI LẠI ---
elif st.session_state.buoc == 5:
    with placeholder.container():
        st.markdown("""
        <div class="game-card">
            <div style="font-size: 80px;">🏆 🥇 🌟</div>
            <h1 style="color: #4CAF50;">BÉ GIỎI QUÁ!</h1>
            <p class="big-text">Bé đã hoàn thành bài học hôm nay.</p>
        </div>
        """, unsafe_allow_html=True)
        
        phat_am_thanh("Chúc mừng bé! Hẹn gặp lại bé lần sau nhé!")

        if st.button("Làm lại câu mới 🔁"):
            tao_cau_hoi_moi()
            st.session_state.buoc = 2
            st.rerun()

# ================== FOOTER ==================
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>© 2025 – Sản phẩm giáo dục mầm non từ trái tim ❤️</div>", unsafe_allow_html=True)
