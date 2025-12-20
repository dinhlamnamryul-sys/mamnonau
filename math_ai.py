import streamlit as st
import requests
from streamlit_lottie import st_lottie
from gtts import gTTS
import os
import uuid
import time
import random

# ================== 1. CẤU HÌNH TRANG GAME ==================
st.set_page_config(page_title="Khu Rừng Phép Thuật", page_icon="🍄", layout="wide")

# ================== 2. TẢI TÀI NGUYÊN (HOẠT HÌNH & ẢNH) ==================
def load_lottie(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Hoạt hình Lottie (Link ổn định)
anim_welcome = load_lottie("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json") # Cáo vẫy tay
anim_star = load_lottie("https://assets9.lottiefiles.com/packages/lf20_touohxv0.json") # Sao vàng
anim_confetti = load_lottie("https://assets2.lottiefiles.com/packages/lf20_u4y9eppv.json") # Pháo giấy
anim_math = load_lottie("https://assets10.lottiefiles.com/packages/lf20_4kji20Y93r.json") # Số

# ================== 3. CSS "THẦN TIÊN" ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Patrick+Hand&display=swap');
    
    /* 1. Nền Rừng Xanh Phép Thuật */
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/fairy-tale-landscape-with-meadow-tree-clouds_107791-744.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Patrick Hand', cursive;
    }
    
    /* 2. Thanh điểm số (Hũ sao) */
    .score-board {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.9);
        padding: 10px 20px;
        border-radius: 50px;
        border: 4px solid #FFD700;
        font-size: 24px;
        font-weight: bold;
        color: #FF6F00;
        z-index: 999;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    /* 3. Khung nội dung trắng mờ ảo */
    .magic-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 5px solid #81C784;
        text-align: center;
    }

    /* 4. Tiêu đề cute */
    h1 {
        font-family: 'Fredoka One', cursive;
        color: #2E7D32 !important;
        text-shadow: 3px 3px 0px #A5D6A7;
        font-size: 60px !important;
        text-align: center;
    }
    
    h2, h3 {
        font-family: 'Fredoka One', cursive;
        color: #FF7043 !important;
    }

    /* 5. Nút bấm biến hình */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 70px;
        font-size: 28px !important;
        font-family: 'Fredoka One', cursive !important;
        border: none;
        box-shadow: 0 8px 0 rgba(0,0,0,0.2);
        transition: all 0.2s;
        margin-bottom: 10px;
    }
    
    /* Màu nút bấm theo vị trí */
    div[data-testid="column"]:nth-of-type(1) .stButton>button { background: #FFEE58; color: #F57F17; box-shadow: 0 8px 0 #F9A825; }
    div[data-testid="column"]:nth-of-type(2) .stButton>button { background: #42A5F5; color: white; box-shadow: 0 8px 0 #1565C0; }
    div[data-testid="column"]:nth-of-type(3) .stButton>button { background: #EC407A; color: white; box-shadow: 0 8px 0 #AD1457; }

    .stButton>button:active {
        transform: translateY(5px);
        box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important;
    }
    
    /* Ẩn header mặc định */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ================== 4. QUẢN LÝ TRẠNG THÁI (SESSION) ==================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'stars' not in st.session_state: st.session_state.stars = 0 # Điểm số
if 'music' not in st.session_state: st.session_state.music = True

# Hàm điều hướng
def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()

# Hàm phát giọng nói
def speak(text):
    try:
        filename = f"speech_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang='vi')
        tts.save(filename)
        st.audio(open(filename, "rb").read(), format="audio/mp3", autoplay=True)
        os.remove(filename)
    except: pass

# ================== 5. THANH ĐIỂM SỐ (LUÔN HIỆN) ==================
st.markdown(f"""
<div class="score-board">
    ⭐ Hũ Sao: {st.session_state.stars}
</div>
""", unsafe_allow_html=True)

# ================== 6. TRANG CHỦ: BẢN ĐỒ KHO BÁU ==================
if st.session_state.page == 'home':
    # Hiệu ứng tiêu đề
    st.markdown("<h1>🍄 KHU RỪNG PHÉP THUẬT 🍄</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if anim_welcome: st_lottie(anim_welcome, height=200, key="welcome")
        st.markdown("<h3 style='text-align:center;'>Bé muốn đi đâu chơi nào?</h3>", unsafe_allow_html=True)

    # MENU CHÍNH (Dạng lưới đẹp mắt)
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown('<div class="magic-box" style="padding:10px;">', unsafe_allow_html=True)
        if anim_math: st_lottie(anim_math, height=120, key="m1")
        st.markdown("### Nhà Toán Học")
        if st.button("VÀO HỌC 1️⃣2️⃣3️⃣"):
            navigate('math')
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="magic-box" style="padding:10px;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3659/3659784.png", width=120)
        st.markdown("### Rạp Chiếu Phim")
        if st.button("XEM PHIM 🍿"):
            navigate('cinema')
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c:
        st.markdown('<div class="magic-box" style="padding:10px;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3043/3043665.png", width=120)
        st.markdown("### Sàn Nhảy Múa")
        if st.button("NGHE NHẠC 🎵"):
            navigate('music')
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Nút phát tiếng chào
    if st.button("🔊 Nghe Cáo Chào"):
        speak("Chào mừng bé đến với Khu Rừng Phép Thuật! Bé hãy chọn một trò chơi nhé!")

# ================== 7. TRANG TOÁN: GIÚP THỎ TÌM CÀ RỐT ==================
elif st.session_state.page == 'math':
    if st.button("🔙 Về Nhà"): navigate('home')
    
    st.markdown('<div class="magic-box">', unsafe_allow_html=True)
    
    c_img, c_content = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/1998/1998610.png", width=150) # Thỏ
    with c_content:
        st.markdown("## 🐰 Giúp Thỏ tìm Cà rốt!")
        st.markdown("### Thỏ đang đói bụng quá. Bé hãy đếm xem có bao nhiêu củ cà rốt?")
    
    # Logic Game
    if 'math_q' not in st.session_state: st.session_state.math_q = random.randint(1, 5)
    
    # Hiển thị Cà rốt (Hình ảnh to đẹp)
    carrots = "".join(["<img src='https://cdn-icons-png.flaticon.com/512/2909/2909787.png' width='60' style='margin:5px;'>"] * st.session_state.math_q)
    st.markdown(f"<div style='background:#FFF3E0; padding:20px; border-radius:20px;'>{carrots}</div>", unsafe_allow_html=True)
    
    st.write("")
    
    # Đáp án
    cols = st.columns(3)
    ans_list = [st.session_state.math_q, st.session_state.math_q+1, abs(st.session_state.math_q-1)]
    if ans_list[2] == 0: ans_list[2] = 2
    ans_list = list(set(ans_list)) # Lọc trùng
    while len(ans_list) < 3: ans_list.append(random.randint(1,9))
    random.shuffle(ans_list)

    def check_math(val):
        if val == st.session_state.math_q:
            st.session_state.stars += 1 # Cộng điểm
            st.balloons()
            speak("Giỏi quá! Cảm ơn bé đã cho Thỏ ăn!")
            time.sleep(1.5)
            st.session_state.math_q = random.randint(1, 9)
            st.rerun()
        else:
            st.error("Chưa đúng rồi, Thỏ vẫn đói quá!")
            speak("Chưa đúng rồi, bé đếm lại đi!")

    for i, num in enumerate(ans_list):
        with cols[i]:
            if st.button(f"SỐ {num}", key=f"btn_{num}"):
                check_math(num)
                
    st.markdown('</div>', unsafe_allow_html=True)

# ================== 8. TRANG PHIM: CÂU CHUYỆN RỪNG XANH ==================
elif st.session_state.page == 'cinema':
    if st.button("🔙 Về Nhà"): navigate('home')
    
    st.markdown('<div class="magic-box">', unsafe_allow_html=True)
    st.markdown("## 🍿 Rạp Chiếu Phim Cổ Tích")
    
    story_choice = st.selectbox("Bé muốn nghe chuyện gì?", ["Cáo và Cò", "Kiến và Ve Sầu", "Sư Tử và Chuột"])
    
    if story_choice == "Cáo và Cò":
        st.video("https://www.youtube.com/watch?v=k_q9461iCw4") # Link minh họa (thay bằng link đúng nếu có)
        st.info("Bài học: Phải biết tôn trọng bạn bè.")
    elif story_choice == "Kiến và Ve Sầu":
        st.video("https://www.youtube.com/watch?v=2r7J_gC_4t0") # Link minh họa
        st.info("Bài học: Phải chăm chỉ lao động.")
    else:
        st.video("https://www.youtube.com/watch?v=7uJf1X2yX1o") # Link minh họa
        st.info("Bài học: Đừng coi thường người nhỏ bé.")
        
    if st.button("⭐ Xem xong nhận Sao"):
        st.session_state.stars += 1
        st.balloons()
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# ================== 9. TRANG NHẠC: VŨ ĐIỆU SÔI ĐỘNG ==================
elif st.session_state.page == 'music':
    if st.button("🔙 Về Nhà"): navigate('home')
    
    st.markdown('<div class="magic-box">', unsafe_allow_html=True)
    st.markdown("## 🎵 Sàn Nhảy Mùa Hè")
    
    col_anim, col_list = st.columns([1,2])
    
    with col_anim:
        # Nhúng ảnh GIF nhảy múa
        st.markdown('<img src="https://media.giphy.com/media/hWY5z84uXF3wjpxG5X/giphy.gif" width="100%">', unsafe_allow_html=True)
    
    with col_list:
        st.markdown("### Bé chọn bài hát nhé:")
        song = st.radio("", ["Baby Shark 🦈", "Một Con Vịt 🦆", "Cả Nhà Thương Nhau 👨‍👩‍👧"])
        
        if song == "Baby Shark 🦈":
            st.video("https://www.youtube.com/watch?v=XqZsoesa55w")
        elif song == "Một Con Vịt 🦆":
            st.video("https://www.youtube.com/watch?v=3182wcMhXuk")
        else:
            st.video("https://www.youtube.com/watch?v=sJ16X-Rz8vU")

    st.markdown('</div>', unsafe_allow_html=True)
