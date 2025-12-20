import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG CHUYÊN NGHIỆP ==================
st.set_page_config(
    page_title="Math Kids Pro",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Khởi tạo biến Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. CSS ĐẲNG CẤP (HIGH CONTRAST & 3D) ==================
st.markdown("""
<style>
    /* 1. NỀN CHUYỂN ĐỘNG MƯỢT MÀ */
    .stApp {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        font-family: 'Segoe UI', 'Roboto', Helvetica, Arial, sans-serif;
    }

    /* 2. KHUNG GAME (CARD) - TRẮNG SÁNG, BÓNG ĐỔ SÂU */
    .pro-card {
        background-color: #ffffff;
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15); /* Bóng đổ mềm chuyên nghiệp */
        text-align: center;
        border: 8px solid #fff;
        margin-top: 20px;
        position: relative;
    }

    /* 3. TYPOGRAPHY (CHỮ) */
    h1 {
        color: #2c3e50;
        font-weight: 900;
        font-size: 3.5rem !important;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    .instruction {
        font-size: 1.5rem;
        color: #7f8c8d;
        font-weight: 600;
        margin-bottom: 30px;
    }

    /* 4. SỐ HỌC SIÊU TO */
    .super-number {
        font-size: 180px;
        line-height: 1;
        font-weight: 900;
        background: -webkit-linear-gradient(#ff9966, #ff5e62);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(4px 4px 0px rgba(0,0,0,0.1));
        animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    /* 5. NÚT BẤM 3D (ĐIỂM NHẤN QUAN TRỌNG) */
    div.stButton > button {
        width: 100%;
        height: 75px;
        font-size: 24px;
        font-weight: 800;
        text-transform: uppercase;
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        position: relative;
        transition: all 0.1s;
        
        /* Hiệu ứng 3D cứng cáp */
        box-shadow: 0 8px 0 rgba(0,0,0,0.2); 
        margin-bottom: 15px;
        transform: translateY(0);
    }

    /* Hiệu ứng khi bấm xuống */
    div.stButton > button:active {
        transform: translateY(6px); /* Nút lún xuống */
        box-shadow: 0 2px 0 rgba(0,0,0,0.2); /* Bóng giảm đi */
    }

    /* MÀU SẮC RIÊNG CHO TỪNG LOẠI NÚT (Dựa trên thứ tự) */
    /* Nút 1: Xanh lá (Nghe/Bắt đầu) */
    div.stButton > button:first-child { 
        background: linear-gradient(to bottom, #2ecc71, #27ae60);
    }
    /* Nút 2: Vàng Cam (Đổi câu) */
    div.stButton > button:nth-child(1) { 
        background: linear-gradient(to bottom, #f1c40f, #f39c12);
    }
    /* Nút 3: Xanh Dương (Tiếp theo) */
    div.stButton > button:last-child { 
        background: linear-gradient(to bottom, #3498db, #2980b9);
    }

    /* 6. ICON HOẠT HÌNH */
    .char-item {
        font-size: 85px;
        display: inline-block;
        margin: 5px;
        filter: drop-shadow(0 5px 5px rgba(0,0,0,0.1));
        animation: float 3s ease-in-out infinite;
    }

    @keyframes popIn { 0% { transform: scale(0); } 100% { transform: scale(1); } }
    @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }

    /* Ẩn các thành phần thừa */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== 3. LOGIC XỬ LÝ ÂM THANH (CHẶT CHẼ) ==================
def play_sound_and_wait(text, wait_seconds):
    """
    Phát âm thanh và BẮT BUỘC CHỜ (Block) cho đến khi nói xong.
    Điều này ngăn việc người dùng bấm loạn xạ hoặc âm thanh bị ngắt.
    """
    try:
        # 1. Phát âm thanh
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        
        # 2. Hiện thông báo chờ (Spinner)
        with st.spinner(f"🔊 Cô đang đọc: '{text}'..."):
            time.sleep(wait_seconds) # Code sẽ dừng ở đây đúng số giây quy định
            
    except Exception as e:
        st.error(f"Lỗi âm thanh: {e}")

def generate_data():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Thỏ"), ("🍎", "Táo"), ("⭐", "Sao"), 
        ("🎈", "Bóng"), ("🍄", "Nấm"), ("🐠", "Cá"),
        ("🚗", "Xe"), ("🦋", "Bướm")
    ])
    # Tạo đáp án
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

if st.session_state.num == 0:
    generate_data()

# ================== 4. GIAO DIỆN CHÍNH ==================

# --- BƯỚC 1: MÀN HÌNH CHỜ (INTRO) ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="pro-card">
        <div style="font-size:100px; margin-bottom:20px;">🎒</div>
        <h1>BÉ VUI HỌC TOÁN</h1>
        <p class="instruction">Chương trình giáo dục sớm cho trẻ mầm non</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("BẮT ĐẦU NGAY"):
            # Chờ 3 giây để đọc xong câu chào mới chuyển trang
            play_sound_and_wait("Chào mừng bé! Hôm nay lớp mình học số đếm nhé!", 3.5)
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: NHẬN BIẾT MẶT SỐ (SỐ TO) ---
elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="pro-card">
        <p class="instruction">Bé hãy nhìn xem đây là số mấy?</p>
        <div class="super-number">{st.session_state.num}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔊 NGHE TÊN"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)
    with c2:
        if st.button("🔄 ĐỔI SỐ"):
            generate_data()
            st.rerun()
    with c3:
        if st.button("➡️ XEM HÌNH"):
            play_sound_and_wait(f"Đúng rồi! Số {st.session_state.num}. Cùng xem hình nhé!", 3)
            st.session_state.step = 3
            st.rerun()

# --- BƯỚC 3: HỌC ĐẾM (SỐ + HÌNH ẢNH) ---
elif st.session_state.step == 3:
    # Render hình ảnh
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="pro-card">
        <p class="instruction">Có bao nhiêu <b>{st.session_state.name}</b> ở đây nhỉ?</p>
        <div style="min-height: 120px; margin: 20px 0;">{html_icons}</div>
        <hr style="border-top: 2px dashed #ddd; margin: 20px 0;">
        <h1 style="color:#e74c3c; font-size: 80px !important;">{st.session_state.num}</h1>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 ĐẾM CÙNG CÔ"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}", 3)
    with c2:
        if st.button("➡️ LÀM BÀI TẬP"):
            play_sound_and_wait("Bây giờ bé hãy tự mình chọn đáp án đúng nhé!", 3)
            st.session_state.step = 4
            st.rerun()

# --- BƯỚC 4: KIỂM TRA (CHỈ CÓ HÌNH) ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="pro-card">
        <p class="instruction">Bé hãy chọn số đúng cho hình này:</p>
        <div style="min-height: 120px; margin-bottom: 30px;">{html_icons}</div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Nút đáp án to
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            # Logic xử lý đáp án
            if st.button(f"{choice}", key=f"quiz_{idx}"):
                if choice == st.session_state.num:
                    st.balloons()
                    # Chờ đọc xong lời khen mới chuyển bài
                    play_sound_and_wait("Chính xác! Bé thông minh quá! Hoan hô!", 3)
                    generate_data() # Tạo bài mới
                    st.session_state.step = 2 # Quay về học số mới
                    st.rerun()
                else:
                    st.error("Chưa đúng!")
                    play_sound_and_wait(f"Số {choice} chưa đúng. Bé nhìn kỹ và đếm lại nhé!", 3)

    st.write("")
    if st.button("⬅️ QUAY LẠI HỌC SỐ"):
        st.session_state.step = 2
        st.rerun()

# Footer
st.markdown("<div style='text-align:center; color:#fff; margin-top:30px; font-weight:bold'>Professional Kids Education AI © 2025</div>", unsafe_allow_html=True)
