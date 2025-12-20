import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import os
import shutil 

# ================== 1. CẤU HÌNH & KHỞI TẠO ==================
st.set_page_config(
    page_title="Hệ Thống Giáo Dục Mầm Non AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo thư mục an toàn
UPLOAD_FOLDER = "thu_vien_so"
def init_upload_folder():
    try:
        if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
            os.remove(UPLOAD_FOLDER)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
    except Exception as e:
        st.error(f"Lỗi khởi tạo: {e}")

init_upload_folder()

if "step" not in st.session_state: st.session_state.step = 1

# ================== 2. CSS GIAO DIỆN ==================
st.markdown("""
<style>
    /* Nền gradient */
    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #E0F7FA 100%);
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* Card nội dung */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 3px solid #fff;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Chữ tiêu đề */
    h1 { color: #FF69B4; text-shadow: 2px 2px 0 #fff; margin: 0; font-size: 2.5em;}
    .big-text { font-size: 24px; color: #555; margin-bottom: 20px;}

    /* ICON NHÂN VẬT */
    .char-icon {
        font-size: 100px; 
        margin: 5px;
        display: inline-block;
        filter: drop-shadow(0 4px 4px rgba(0,0,0,0.1));
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .char-icon:hover { transform: scale(1.1); }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* NÚT BẤM */
    div.stButton > button {
        width: 100%;
        height: 65px;
        border-radius: 20px;
        font-size: 22px;
        font-weight: bold;
        border: none;
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
        color: #444;
        background: linear-gradient(45deg, #FF9A9E, #FECFEF);
    }
    div.stButton > button:hover { transform: translateY(-3px); }
    
    /* Link Button style */
    .link-btn {
        text-decoration: none;
        color: #007bff;
        font-weight: bold;
        padding: 10px;
        border: 2px dashed #007bff;
        border-radius: 10px;
        display: block;
        text-align: center;
        margin-top: 10px;
    }
    .link-btn:hover { background-color: #e7f1ff; }
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM HỖ TRỢ ==================
def play_sound(text, delay=0):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        if delay > 0:
            with st.spinner("Cô đang nói..."):
                time.sleep(delay)
    except:
        pass

def generate_math_question():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Con Thỏ"), ("🍎", "Quả Táo"), ("⭐", "Ngôi Sao"), 
        ("🎈", "Bóng Bay"), ("🍄", "Cây Nấm"), ("🐠", "Con Cá"),
        ("🐣", "Gà Con"), ("🦋", "Bươm Bướm")
    ])
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

def get_file_type(filename):
    ext = filename.split('.')[-1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif']: return 'image'
    if ext in ['mp4', 'mov', 'avi']: return 'video'
    if ext in ['mp3', 'wav']: return 'audio'
    return 'unknown'

if "num" not in st.session_state: generate_math_question()

# ================== 4. GIAO DIỆN SIDEBAR ==================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3468/3468306.png", width=100)
    st.markdown("## 🌈 MENU CHỨC NĂNG")
    
    menu = st.radio("", ["🐰 Bé Học Toán", "📂 Kho Học Liệu"], index=0)
    
    st.markdown("---")
    st.info("💡 Mẹo: Bấm 'Đổi câu' để tạo bài tập mới.")
    
    # --- PHẦN LIÊN KẾT BẠN YÊU CẦU ---
    st.markdown("---")
    st.markdown("### 🔗 Liên kết tham khảo")
    # Tạo một nút link đẹp
    st.markdown("""
        <a href="https://gemini.google.com/share/90bf889af5f6" target="_blank" class="link-btn">
            🤖 Xem Chat Gemini Gốc
        </a>
    """, unsafe_allow_html=True)

# ================== 5. CHỨC NĂNG 1: BÉ HỌC TOÁN ==================
if menu == "🐰 Bé Học Toán":
    
    if st.session_state.step == 1:
        st.markdown("""
        <div class="main-card">
            <div style="font-size:100px; animation: bounce 2s infinite;">👋</div>
            <h1>BÉ VUI HỌC TOÁN</h1>
            <p class="big-text">Chào mừng bé đến với lớp học AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("🚀 BẮT ĐẦU NGAY", type="primary"):
                play_sound("Chào mừng bé! Chúng mình cùng học đếm nhé!", delay=3)
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        img_html = "".join([f'<span class="char-icon">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        
        st.markdown(f"""
        <div class="main-card">
            <p class="big-text">Bé hãy đếm xem có bao nhiêu <b>{st.session_state.name}</b>?</p>
            <div style="margin: 20px 0;">{img_html}</div>
            <h1 style="font-size:80px; color:#ff4757;">{st.session_state.num}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔊 Đọc"): 
                play_sound(f"Có {st.session_state.num} {st.session_state.name}")
        with col2:
            if st.button("🔄 Đổi Câu"):
                generate_math_question()
                st.rerun()
        with col3:
            if st.button("➡️ Bài Tập"):
                play_sound("Bé hãy chọn đáp án đúng nhé", delay=2)
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        img_html = "".join([f'<span class="char-icon">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        
        st.markdown(f"""
        <div class="main-card">
            <p class="big-text">Đố bé có bao nhiêu {st.session_state.name}?</p>
            <div style="margin: 20px 0;">{img_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with cols[idx]:
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound("Hoan hô! Bé giỏi quá", delay=2)
                        generate_math_question()
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Sai rồi")
                        play_sound("Chưa đúng đâu")
        
        st.write("")
        if st.button("⬅️ Quay lại đếm"):
            st.session_state.step = 2
            st.rerun()

# ================== 6. CHỨC NĂNG 2: KHO HỌC LIỆU ==================
elif menu == "📂 Kho Học Liệu":
    st.markdown('<div class="main-card"><h1>📂 KHO HỌC LIỆU SỐ</h1></div>', unsafe_allow_html=True)

    with st.expander("⬆️ Tải tài liệu mới", expanded=True):
        uploaded_files = st.file_uploader("Chọn file (Ảnh, Video, Nhạc)", accept_multiple_files=True)
        if uploaded_files:
            init_upload_folder()
            for uploaded_file in uploaded_files:
                path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success("Đã lưu thành công!")
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    
    try:
        files = os.listdir(UPLOAD_FOLDER)
    except:
        init_upload_folder()
        files = []
        
    if not files:
        st.info("Chưa có file nào.")
    else:
        cols = st.columns(2)
        for i, filename in enumerate(files):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file_type = get_file_type(filename)
            with cols[i % 2]:
                with st.container():
                    st.markdown(f'<div style="background:white; padding:10px; border-radius:15px; margin-bottom:10px; border:1px solid #ddd"><b>{filename}</b></div>', unsafe_allow_html=True)
                    if file_type == 'image': st.image(file_path, use_container_width=True)
                    elif file_type == 'video': st.video(file_path)
                    elif file_type == 'audio': st.audio(file_path)
                    
                    if st.button("🗑️ Xóa", key=f"del_{filename}"):
                        try:
                            os.remove(file_path)
                            st.rerun()
                        except:
                            st.error("Không xóa được file")
