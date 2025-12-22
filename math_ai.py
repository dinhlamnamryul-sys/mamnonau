import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import base64
import os

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Đếm Cùng Thỏ Con",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# --- HÀM HỖ TRỢ ĐỌC ẢNH ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# ================== 2. CSS & ANIMATION TOÀN MÀN HÌNH ==================
st.markdown("""
<style>
    /* Nền cầu vồng */
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
    }

    /* ẨN THANH PHÁT ÂM THANH */
    [data-testid="stAudio"] {
        display: none !important;
    }
    
    /* === QUAN TRỌNG: CHỐNG LÀM MỜ KHI APP ĐANG CHẠY (KHI NÓI) === */
    .element-container, .stMarkdown, .stBlock, div[data-testid="stVerticalBlock"] {
        opacity: 1 !important;
        filter: none !important;
    }
    
    /* Card hiển thị */
    .game-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 40px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        text-align: center;
        border: 6px solid #fff;
        animation: floatCard 5s ease-in-out infinite;
        position: relative;
        z-index: 100;
        min-height: 350px;
        margin-top: 40px;
        
        opacity: 1 !important;
        filter: none !important;
        transform-style: preserve-3d;
    }

    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* ANIMATION CHUNG CHO THỎ */
    @keyframes rabbitJump {
        0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
        25% { transform: translateY(-15px) rotate(-5deg) scale(1.05); }
        50% { transform: translateY(0px) rotate(0deg) scale(1); }
        75% { transform: translateY(-5px) rotate(5deg) scale(1.02); }
    }

    .rabbit-hero {
        max-width: 120px;
        height: auto;
        margin-bottom: 20px;
        filter: drop-shadow(0 8px 6px rgba(0,0,0,0.2)) !important;
        animation: rabbitJump 3s infinite ease-in-out;
        opacity: 1 !important;
    }

    .rabbit-peek {
        position: absolute;
        top: -90px;
        left: -30px;
        width: 130px;
        height: auto;
        z-index: 200;
        filter: drop-shadow(2px 5px 5px rgba(0,0,0,0.3)) !important;
        animation: rabbitJump 3s infinite ease-in-out;
        opacity: 1 !important;
    }
    
    .grass-decoration {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: auto;
        max-height: 150px;
        z-index: 40;
        pointer-events: none;
        object-fit: cover;
        opacity: 1 !important;
    }

    /* SỐ KHỔNG LỒ (Dùng cho bước 2) */
    .super-number {
        font-size: 140px;
        line-height: 1.1;
        font-weight: 900;
        color: #ff6b6b;
        text-shadow: 
            3px 3px 0 #fff,
            -1px -1px 0 #fff,  
            1px -1px 0 #fff,
            -1px 1px 0 #fff,
            1px 1px 0 #fff;
        margin: 0;
        margin-top: 20px;
        opacity: 1 !important;
        filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.1)) !important;
        transform: translateZ(0); 
        -webkit-font-smoothing: antialiased;
    }

    /* BUTTON STYLE */
    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 18px !important;
        font-weight: 900 !important;
        color: white !important;
        border: 3px solid white !important;
        border-radius: 30px !important;
        cursor: pointer;
        margin-bottom: 12px;
        box-shadow: 0 5px 0 rgba(0,0,0,0.15);
        transition: all 0.1s;
        position: relative;
        z-index: 101; 
        opacity: 1 !important; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    div.stButton > button:active, div.stButton > button:focus, div.stButton > button:hover {
        top: 4px;
        box-shadow: 0 0 0 rgba(0,0,0,0.15);
        color: white !important;
        background-color: inherit !important;
        opacity: 1 !important; 
        filter: none !important;
        text-decoration: none !important;
        outline: none !important;
        border-color: white !important;
    }

    .char-item {
        font-size: 80px;
        display: inline-block;
        margin: 5px;
        filter: drop-shadow(0 5px 2px rgba(0,0,0,0.1)); 
        opacity: 1 !important;
    }
    
    .instruction { font-size: 22px; color: #57606f; font-weight: bold; opacity: 1 !important; }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
        position: relative;
        z-index: 50;
    }

    /* Animation background */
    .full-screen-anim {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none; 
        z-index: 1;
        overflow: hidden;
    }
    .duck-anim { position: absolute; bottom: 20px; font-size: 80px; animation: swim-screen 25s linear infinite; }
    .bee-anim { position: absolute; font-size: 50px; animation: fly-screen 20s linear infinite; }
    .bubble { position: absolute; background: rgba(255,255,255,0.6); border-radius: 50%; }
    
    @keyframes swim-screen {
        0% { left: -150px; transform: scaleX(1); }
        45% { left: 100vw; transform: scaleX(1); }
        50% { left: 100vw; transform: scaleX(-1); }
        95% { left: -150px; transform: scaleX(-1); }
        100% { left: -150px; transform: scaleX(1); }
    }
    @keyframes fly-screen {
        0% { top: 10vh; left: -10vw; }
        25% { top: 20vh; left: 30vw; transform: rotate(10deg); }
        50% { top: 5vh; left: 60vw; transform: rotate(-10deg); }
        75% { top: 30vh; left: 80vw; transform: rotate(10deg); }
        100% { top: 15vh; left: 110vw; }
    }
    @keyframes rise-screen {
        0% { bottom: -50px; opacity: 0; transform: scale(0.5); }
        50% { opacity: 0.6; }
        100% { bottom: 100vh; opacity: 0; transform: scale(1.5); }
    }

</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM XỬ LÝ LOGIC ==================
def play_sound_and_wait(text, manual_wait=0):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        
        # Phát âm thanh (đã ẩn giao diện bằng CSS)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        
        calculated_wait = (len(text.split()) * 0.45) + 2.0
        final_wait = max(calculated_wait, manual_wait)

        with st.spinner(f"🔊 Cô đang nói..."):
            time.sleep(final_wait)
            
    except Exception:
        time.sleep(manual_wait)

def generate_data():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Thỏ"), ("🍎", "Táo"), ("⭐", "Sao"), 
        ("🎈", "Bóng"), ("🍄", "Nấm"), ("🐠", "Cá"),
        ("🚗", "Xe"), ("🦋", "Bướm")
    ])
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

if st.session_state.num == 0:
    generate_data()

# --- HÀM HTML TRANG TRÍ ---
def get_decoration_html():
    grass_html = ""
    img_b64 = get_base64_image("hoaco.png")
    if img_b64:
        grass_html = f'<img src="data:image/png;base64,{img_b64}" class="grass-decoration">'

    return f"""<div class="full-screen-anim"><div class="duck-anim">🦆</div><div class="bee-anim">🐝</div><div class="bee-anim" style="animation-delay: 10s; top: 40vh; font-size: 35px;">🐝</div><div style="position: absolute; bottom: 10px; left: 5vw; font-size: 50px;">🌷</div><div style="position: absolute; bottom: 15px; left: 12vw; font-size: 40px;">🌻</div><div style="position: absolute; bottom: 10px; right: 5vw; font-size: 50px;">🍄</div><div class="bubble" style="left: 10vw; width: 30px; height: 30px; animation: rise-screen 10s infinite;"></div><div class="bubble" style="left: 30vw; width: 50px; height: 50px; animation: rise-screen 15s infinite 2s;"></div><div class="bubble" style="left: 70vw; width: 20px; height: 20px; animation: rise-screen 12s infinite 5s;"></div><div class="bubble" style="left: 90vw; width: 40px; height: 40px; animation: rise-screen 18s infinite 1s;"></div>{grass_html}</div>"""

# ================== 4. GIAO DIỆN CHÍNH ==================

st.markdown(get_decoration_html(), unsafe_allow_html=True)

# --- BƯỚC 1: TRANG CHỦ ---
if st.session_state.step == 1:
    img_html = ""
    img_b64 = get_base64_image("thocon.png")
    if img_b64:
        img_html = f'<img src="data:image/png;base64,{img_b64}" class="rabbit-hero">'
    else:
        img_html = '<div style="font-size:100px; margin-bottom:10px;">🐰</div>'

    st.markdown(f"""
    <div class="game-card" style="padding: 50px;">
        {img_html}
        <h1 style="color:#ff4757; font-size:50px;">Bé Đếm Cùng Thỏ Con</h1>
        <p class="instruction">Học mà chơi - Chơi mà học</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("""<style>div.stButton > button {background: linear-gradient(to bottom, #ff6b6b, #ee5253); height: 80px; font-size: 24px !important;}</style>""", unsafe_allow_html=True)
        if st.button("🚀 BẮT ĐẦU NGAY"):
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!")
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: HỌC SỐ (Vẫn hiện số để bé học) ---
elif st.session_state.step == 2:
    col_controls, col_display = st.columns([3, 7], gap="large")

    with col_controls:
        st.markdown("### 🎮 Điều khiển")
        
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait("Bé hãy nhìn xem, đây là số mấy?")

        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #74b9ff, #0984e3);}}</style>""", unsafe_allow_html=True)
        if st.button("🗣️ Đây là số...?"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}")

        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #ffeaa7, #fdcb6e); color: #d35400 !important;}}</style>""", unsafe_allow_html=True)
        if st.button("🔄 Đổi số khác"):
            generate_data()
            st.rerun()

        st.markdown(f"""<style>div.stButton:nth-of-type(4) > button {{background: linear-gradient(to bottom, #fd79a8, #e84393);}}</style>""", unsafe_allow_html=True)
        if st.button("➡️ Xem hình ảnh"):
            play_sound_and_wait(f"Đúng rồi! Số {st.session_state.num}. Cùng xem hình nhé!")
            st.session_state.step = 3
            st.rerun()
    
    with col_display:
        rabbit_html = ""
        img_b64 = get_base64_image("thocon.png")
        if img_b64:
            rabbit_html = f'<img src="data:image/png;base64,{img_b64}" class="rabbit-peek">'
        
        st.markdown(f"""
        <div class="game-card">
            {rabbit_html} <p class="instruction">Số này là số mấy?</p>
            <div class="super-number">{st.session_state.num}</div>
        </div>
        """, unsafe_allow_html=True)

# --- BƯỚC 3: XEM HÌNH & HỌC ĐẾM (Đã xóa số hiển thị) ---
elif st.session_state.step == 3:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    col_controls, col_display = st.columns([3, 7], gap="large")

    with col_controls:
        st.markdown("### 🎮 Điều khiển")
        
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait(f"Đố bé biết có bao nhiêu bạn {st.session_state.name} ở đây?")
        
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #55efc4, #00b894);}}</style>""", unsafe_allow_html=True)
        if st.button("🔢 Đếm cùng cô"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}")

        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #fab1a0, #e17055);}}</style>""", unsafe_allow_html=True)
        if st.button("🎮 Chơi trò chơi"):
            play_sound_and_wait("Bây giờ bé hãy tự mình chọn đáp án đúng nhé!")
            st.session_state.step = 4
            st.rerun()

    with col_display:
        st.markdown(f"""
        <div class="game-card">
            <p class="instruction">Có bao nhiêu <b>{st.session_state.name}</b>?</p>
            <div style="margin: 10px 0;">{html_icons}</div>
            </div>
        """, unsafe_allow_html=True)

# --- BƯỚC 4: BÀI TẬP ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    col_controls, col_display = st.columns([3, 7], gap="large")
    
    with col_controls:
        st.markdown("### 🎮 Điều khiển")
        
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait("Bé hãy đếm kỹ và chọn số đúng ở bên cạnh nhé!")
            
        st.markdown(f"""<style>div.stButton:last-of-type > button {{background: linear-gradient(to bottom, #dfe6e9, #b2bec3); color: #636e72 !important; margin-top: 20px;}}</style>""", unsafe_allow_html=True)
        if st.button("⬅️ Quay lại"):
            st.session_state.step = 2
            st.rerun()

    with col_display:
        st.markdown(f"""
        <div class="game-card">
            <p class="instruction">Hình này ứng với số mấy?</p>
            <div style="margin-bottom: 20px;">{html_icons}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") 
        c1, c2, c3 = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with [c1, c2, c3][idx]:
                colors = [("#81ecec", "#00cec9"), ("#74b9ff", "#0984e3"), ("#a29bfe", "#6c5ce7")]
                cl, cd = colors[idx]
                st.markdown(f"""<style>div.stButton:nth-of-type({idx + 2}) > button {{background: linear-gradient(to bottom, {cl}, {cd}); font-size: 30px !important; height: 70px;}}</style>""", unsafe_allow_html=True)
                
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound_and_wait("Chính xác! Hoan hô bé!")
                        generate_data()
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Sai rồi!")
                        play_sound_and_wait("Chưa đúng rồi, bé thử lại nhé!")
