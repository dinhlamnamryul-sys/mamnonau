import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import speech_recognition as sr  # <--- [MỚI] Thêm thư viện nhận diện giọng nói

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Vui Học Toán 3D - AI",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. CSS & ANIMATION ==================
st.markdown("""
<style>
    /* Nền cầu vồng */
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
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
        min-height: 350px;
    }
    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    /* Số khổng lồ */
    .super-number {
        font-size: 140px; line-height: 1.1; font-weight: 900;
        color: #ff6b6b; text-shadow: 4px 4px 0px #fff; margin: 0;
    }
    /* BUTTON STYLE */
    div.stButton > button {
        width: 100%; height: 65px; font-size: 18px !important;
        font-weight: 800 !important; color: white !important;
        border: 3px solid white !important; border-radius: 30px !important;
        cursor: pointer; margin-bottom: 12px;
        box-shadow: 0 5px 0 rgba(0,0,0,0.15); position: relative;
    }
    div.stButton > button:active { top: 4px; box-shadow: 0 0 0 rgba(0,0,0,0.15); }
    
    .char-item { font-size: 80px; display: inline-block; margin: 5px; }
    .instruction { font-size: 22px; color: #57606f; font-weight: bold; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM XỬ LÝ LOGIC & AI ==================

# [MỚI] TỪ ĐIỂN HIỂU GIỌNG NÓI
TEXT_TO_NUM = {
    "một": 1, "mốt": 1, "1": 1,
    "hai": 2, "hài": 2, "2": 2,
    "ba": 3, "bà": 3, "3": 3,
    "bốn": 4, "tư": 4, "4": 4,
    "năm": 5, "lăm": 5, "5": 5,
    "sáu": 6, "6": 6,
    "bảy": 7, "bẩy": 7, "7": 7,
    "tám": 8, "8": 8,
    "chín": 9, "chính": 9, "9": 9,
    "mười": 10, "chục": 10, "10": 10
}

def play_sound_and_wait(text, wait_seconds):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        with st.spinner(f"🔊 Cô đang nói: {text}"):
            time.sleep(wait_seconds)
    except Exception:
        time.sleep(wait_seconds)

# [MỚI] HÀM NGHE GIỌNG NÓI
def listen_for_answer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("👂 Đang lắng nghe... Bé hãy nói to lên nhé!")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=3)
            st.success("🤖 Đang suy nghĩ...")
            text = r.recognize_google(audio, language="vi-VN")
            return text.lower()
        except:
            return None

def generate_data():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Thỏ"), ("🍎", "Táo"), ("⭐", "Sao"), 
        ("🎈", "Bóng"), ("🍄", "Nấm"), ("🐠", "Cá")
    ])
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

if st.session_state.num == 0:
    generate_data()

# ================== 4. GIAO DIỆN CHÍNH ==================

# --- BƯỚC 1: TRANG CHỦ ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card" style="padding: 50px;">
        <div style="font-size:100px; margin-bottom:10px;">🎡</div>
        <h1 style="color:#ff4757; font-size:50px;">BÉ VUI HỌC TOÁN</h1>
        <p class="instruction">AI: Giọng nói & Nghe hiểu</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("""<style>div.stButton > button {background: linear-gradient(to bottom, #ff6b6b, #ee5253); height: 80px; font-size: 24px !important;}</style>""", unsafe_allow_html=True)
        if st.button("🚀 BẮT ĐẦU NGAY"):
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!", 3)
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: HỌC SỐ ---
elif st.session_state.step == 2:
    c1, c2 = st.columns([3, 7])
    with c1:
        st.markdown("### 🎮 Điều khiển")
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait("Bé hãy nhìn xem, đây là số mấy?", 3)
        if st.button("🗣️ Đây là số...?"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)
        if st.button("🔄 Đổi số khác"):
            generate_data()
            st.rerun()
        st.markdown(f"""<style>div.stButton:nth-of-type(4) > button {{background: linear-gradient(to bottom, #fd79a8, #e84393);}}</style>""", unsafe_allow_html=True)
        if st.button("➡️ Xem hình ảnh"):
            play_sound_and_wait(f"Đúng rồi! Số {st.session_state.num}. Cùng xem hình nhé!", 3)
            st.session_state.step = 3
            st.rerun()
    with c2:
        st.markdown(f"""<div class="game-card"><p class="instruction">Số này là số mấy?</p><div class="super-number">{st.session_state.num}</div></div>""", unsafe_allow_html=True)

# --- BƯỚC 3: HỌC ĐẾM ---
elif st.session_state.step == 3:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    c1, c2 = st.columns([3, 7])
    with c1:
        st.markdown("### 🎮 Điều khiển")
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait(f"Đố bé biết có bao nhiêu bạn {st.session_state.name} ở đây?", 4)
        if st.button("🔢 Đếm cùng cô"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}", 3)
        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #fab1a0, #e17055);}}</style>""", unsafe_allow_html=True)
        if st.button("🎮 Chơi trò chơi"):
            play_sound_and_wait("Bây giờ bé hãy tự mình chọn, hoặc nói đáp án nhé!", 3)
            st.session_state.step = 4
            st.rerun()
    with c2:
        st.markdown(f"""<div class="game-card"><p class="instruction">Có bao nhiêu <b>{st.session_state.name}</b>?</p><div>{html_icons}</div><h1 style="font-size: 80px; color:#ff6b81; margin:0;">{st.session_state.num}</h1></div>""", unsafe_allow_html=True)

# --- BƯỚC 4: BÀI TẬP (CÓ AI NGHE GIỌNG) ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    c1, c2 = st.columns([3, 7])
    
    with c1:
        st.markdown("### 🎮 Điều khiển AI")
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait("Bé hãy đếm và chọn số đúng, hoặc bấm nút micro để nói nhé!", 5)
        
        # [MỚI] NÚT BẤM ĐỂ NÓI
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #00b894, #00cec9);}}</style>""", unsafe_allow_html=True)
        if st.button("🎙️ NÓI ĐÁP ÁN"):
            play_sound_and_wait("Bé nói đi, cô đang nghe nè!", 1)
            user_text = listen_for_answer()
            if user_text:
                st.info(f"Bé đã nói: '{user_text}'")
                found_num = None
                # Kiểm tra xem trong câu nói có số đúng không
                for word, val in TEXT_TO_NUM.items():
                    if word in user_text:
                        found_num = val
                        break
                
                if found_num == st.session_state.num:
                    st.balloons()
                    play_sound_and_wait(f"Giỏi quá! Bé nói đúng rồi, là số {found_num}!", 4)
                    generate_data()
                    st.session_state.step = 2
                    st.rerun()
                else:
                    play_sound_and_wait("Cô nghe chưa rõ hoặc chưa đúng, bé nói lại nhé!", 3)
            else:
                st.warning("Cô chưa nghe thấy gì cả!")

        if st.button("⬅️ Quay lại"):
            st.session_state.step = 2
            st.rerun()

    with c2:
        st.markdown(f"""<div class="game-card"><p class="instruction">Hình này ứng với số mấy?</p><div style="margin-bottom: 20px;">{html_icons}</div></div>""", unsafe_allow_html=True)
        st.write("") 
        
        # CÁC NÚT BẤM SỐ (DỰ PHÒNG)
        cols = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with cols[idx]:
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound_and_wait("Chính xác! Hoan hô bé!", 3)
                        generate_data()
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Sai rồi!")
                        play_sound_and_wait("Chưa đúng rồi!", 2)
