import streamlit as st
import random
from gtts import gTTS
import uuid
import os
import time

# ================== 1. CẤU HÌNH TRANG (Phải để đầu tiên) ==================
st.set_page_config(
    page_title="Vườn Thỏ Diệu Kỳ",
    page_icon="🐰",
    layout="centered"
)

# ================== 2. TÙY CHỈNH HÌNH ẢNH & ÂM THANH ==================
# Bạn có thể thay đổi link ảnh bên dưới thành tên file ảnh của bạn (ví dụ: "image_ac158d.png")
# nếu file ảnh nằm cùng thư mục với file code này.
LINK_ANH_THO = "https://cdn-icons-png.flaticon.com/512/4086/4086392.png" 
# Hoặc dùng link ảnh hoạt hình động (GIF) nếu muốn
# LINK_ANH_THO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif"

# ================== 3. CSS SIÊU SINH ĐỘNG CHO BÉ ==================
st.markdown(f"""
<style>
    /* Nhúng font chữ tròn trịa dễ thương */
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap');

    /* Nền bầu trời và thảm cỏ */
    .stApp {{
        background: linear-gradient(to bottom, #4FC3F7 0%, #E1F5FE 60%, #76FF03 60%, #64DD17 100%);
        font-family: 'Baloo 2', cursive;
    }}

    /* Ẩn menu mặc định */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* HIỆU ỨNG ĐỘNG: Thỏ nhún nhảy */
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        25% {{ transform: translateY(-15px) rotate(-5deg); }}
        50% {{ transform: translateY(0) rotate(0deg); }}
        75% {{ transform: translateY(-5px) rotate(5deg); }}
    }}

    /* HIỆU ỨNG ĐỘNG: Mây bay */
    @keyframes floatCloud {{
        0% {{ transform: translateX(-10px); }}
        50% {{ transform: translateX(10px); }}
        100% {{ transform: translateX(-10px); }}
    }}

    .rabbit-img {{
        width: 280px;
        animation: bounce 3s infinite ease-in-out; /* Thỏ chuyển động ở đây */
        margin-bottom: -10px;
        filter: drop-shadow(0 15px 15px rgba(0,0,0,0.3));
        transition: transform 0.2s;
        cursor: pointer;
    }}
    
    .rabbit-img:hover {{
        transform: scale(1.1); /* Phóng to khi di chuột vào */
    }}

    /* Bong bóng lời thoại (Speech Bubble) */
    .bubble {{
        position: relative;
        background: #FFFFFF;
        border-radius: 40px;
        padding: 20px 30px;
        text-align: center;
        color: #E65100;
        font-size: 26px;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border: 5px solid #FF9800;
        margin-bottom: 25px;
        animation: floatCloud 4s infinite ease-in-out;
    }}
    
    .bubble:after {{
        content: '';
        position: absolute;
        bottom: -20px;
        left: 50%;
        border: 20px solid transparent;
        border-top-color: #FF9800;
        margin-left: -20px;
    }}

    /* Card hiển thị số/đồ vật */
    .game-card {{
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 30px;
        text-align: center;
        font-size: 55px;
        color: #D50000;
        margin: 10px 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 3px dashed #BDBDBD;
    }}

    /* Nút bấm kẹo ngọt */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(to bottom, #FFEB3B, #FDD835);
        color: #D50000 !important;
        font-family: 'Baloo 2', cursive !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border-radius: 50px !important;
        border: 4px solid #FBC02D !important;
        box-shadow: 0 8px 0 #F57F17 !important;
        transition: all 0.1s;
        text-transform: uppercase;
        margin-top: 15px;
    }}
    
    .stButton>button:hover {{
        background: #FFF176;
        transform: translateY(-2px);
    }}

    .stButton>button:active {{
        transform: translateY(6px);
        box-shadow: 0 2px 0 #F57F17 !important;
    }}
    
    /* Input nhập số */
    .stNumberInput input {{
        font-size: 35px;
        text-align: center;
        color: #E91E63;
        font-weight: bold;
        border-radius: 20px;
        border: 3px solid #E1F5FE;
    }}
</style>
""", unsafe_allow_html=True)

# ================== 4. CÁC HÀM HỖ TRỢ (LOGIC) ==================

def phat_am_thanh(text):
    """Hàm đọc giọng nói chị Google"""
    try:
        filename = f"sound_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang="vi")
        tts.save(filename)
        audio_file = open(filename, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        audio_file.close()
        os.remove(filename)
    except Exception:
        # Nếu lỗi âm thanh thì bỏ qua, không làm crash app của bé
        pass

def hien_thi_nhan_vat(loi_noi, cam_xuc="vui"):
    """Hiển thị Thỏ và lời thoại"""
    # Chia cột để thỏ nằm giữa
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        # 1. Lời thoại
        st.markdown(f'<div class="bubble">{loi_noi}</div>', unsafe_allow_html=True)
        
        # 2. Hình ảnh thỏ (có thể thay đổi link ảnh ở đầu file)
        st.markdown(
            f'<div style="text-align: center;">'
            f'<img src="{LINK_ANH_THO}" class="rabbit-img">'
            f'</div>', 
            unsafe_allow_html=True
        )

# ================== 5. DỮ LIỆU BÀI HỌC ==================
do_vat = {
    "🍎": "quả táo",
    "cat": "con mèo", # Dùng text nếu không hiển thị được emoji mèo
    "🐟": "con cá",
    "🌸": "bông hoa",
    "⭐": "ngôi sao",
    "🍬": "viên kẹo",
    "🎈": "bóng bay"
}
# Map lại emoji mèo vì một số hệ điều hành cũ không hiện emoji mèo đẹp
icon_map = {
    "cat": "🐱", 
    "🍎": "🍎", "🐟": "🐟", "🌸": "🌸", "⭐": "⭐", "🍬": "🍬", "🎈": "🎈"
}

chu_so = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

# ================== 6. QUẢN LÝ TRẠNG THÁI (SESSION STATE) ==================
if "buoc" not in st.session_state:
    st.session_state.buoc = 1     # Bắt đầu ở bước 1
    st.session_state.so = 1       # Mặc định
    st.session_state.key_vat = "🍎"
    st.session_state.ten_vat = "quả táo"
    st.session_state.diem = 0

def tao_cau_hoi_moi():
    st.session_state.so = random.randint(1, 10)
    # Chọn ngẫu nhiên vật
    key, name = random.choice(list(do_vat.items()))
    st.session_state.key_vat = key
    st.session_state.ten_vat = name

# ================== 7. GIAO DIỆN CHÍNH (FLOW) ==================

# -- Khoảng trắng để đẩy nội dung xuống dưới mây --
st.write("") 
st.write("") 

# --- BƯỚC 1: MÀN HÌNH CHÀO ---
if st.session_state.buoc == 1:
    hien_thi_nhan_vat("Chào bé yêu! <br> Tớ là Thỏ Bông.<br> Cùng chơi đếm số nhé! ❤️")
    
    # Phát âm thanh chào (chỉ phát 1 lần)
    if 'da_chao' not in st.session_state:
        phat_am_thanh("Chào bé yêu! Tớ là Thỏ Bông. Cùng chơi đếm số với tớ nhé!")
        st.session_state.da_chao = True

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 VÀO CHƠI THÔI"):
            tao_cau_hoi_moi()
            st.session_state.buoc = 2
            st.rerun()

# --- BƯỚC 2: HỌC ĐẾM (HIỂN THỊ) ---
elif st.session_state.buoc == 2:
    hien_thi_nhan_vat(f"Đố bé biết có bao nhiêu <br> {st.session_state.ten_vat} ở dưới nào?")
    
    # Lấy icon
    icon = icon_map.get(st.session_state.key_vat, st.session_state.key_vat)
    
    # Hiển thị vật thể
    st.markdown(f"""
    <div class="game-card">
        {' '.join([icon] * st.session_state.so)}
    </div>
    """, unsafe_allow_html=True)
    
    phat_am_thanh(f"Đố bé biết có bao nhiêu {st.session_state.ten_vat} nào?")
    
    time.sleep(1.5) # Dừng xíu cho bé đếm
    
    if st.button("👉 XEM ĐÁP ÁN"):
        st.session_state.buoc = 3
        st.rerun()

# --- BƯỚC 3: KẾT QUẢ ĐẾM ---
elif st.session_state.buoc == 3:
    hien_thi_nhan_vat(f"Đúng rồi! Có tất cả <b>{st.session_state.so}</b> {st.session_state.ten_vat}!")
    
    st.markdown(f"""
    <div class="game-card" style="color: #2E7D32; border-color: #2E7D32;">
        {st.session_state.so}<br>
        <span style="font-size: 24px;">({chu_so[st.session_state.so]})</span>
    </div>
    """, unsafe_allow_html=True)
    
    phat_am_thanh(f"Có tất cả {st.session_state.so} {st.session_state.ten_vat}. Số {st.session_state.so}.")

    if st.button("🎮 CHƠI TRÒ CHƠI KIỂM TRA"):
        st.session_state.buoc = 4
        st.rerun()

# --- BƯỚC 4: TRÒ CHƠI NHẬP SỐ ---
elif st.session_state.buoc == 4:
    hien_thi_nhan_vat(f"Bây giờ bé hãy nhập số lượng <br> {st.session_state.ten_vat} vào ô dưới nhé!")
    
    icon = icon_map.get(st.session_state.key_vat, st.session_state.key_vat)
    st.markdown(f"""
    <div class="game-card">
        {' '.join([icon] * st.session_state.so)}
    </div>
    """, unsafe_allow_html=True)

    # Input nhập số
    tra_loi = st.number_input("Bé chọn số ở đây:", 0, 20, 0)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Kiểm tra ✅"):
            if tra_loi == st.session_state.so:
                st.balloons() # Bóng bay
                phat_am_thanh("Hoan hô! Bé đếm đúng rồi! Bé giỏi quá!")
                time.sleep(1)
                st.session_state.buoc = 5
                st.rerun()
            else:
                phat_am_thanh(f"Chưa đúng rồi. Bé thử đếm lại kỹ hơn nhé!")
                st.error("Ôi sai rồi, bé đếm lại nhé!")
    
    with col_b:
        if st.button("Đổi câu khác 🔄"):
            tao_cau_hoi_moi()
            st.session_state.buoc = 2
            st.rerun()

# --- BƯỚC 5: CÂU HỎI NÂNG CAO (SỐ LIỀN SAU) ---
elif st.session_state.buoc == 5:
    dap_an_sau = st.session_state.so + 1
    hien_thi_nhan_vat(f"Câu hỏi khó hơn nè! <br> Số đứng sau số {st.session_state.so} là số mấy?")
    
    st.markdown(f"""
    <div class="game-card">
        {st.session_state.so} ➡️ ❓
    </div>
    """, unsafe_allow_html=True)

    tra_loi_sau = st.number_input("Số tiếp theo là:", 0, 20, 0)

    if st.button("Trả lời 🎁"):
        if tra_loi_sau == dap_an_sau:
            st.snow() # Tuyết rơi chúc mừng
            phat_am_thanh(f"Tuyệt vời! Sau số {st.session_state.so} là số {dap_an_sau}. Bé thông minh quá!")
            st.success(f"Chính xác! {st.session_state.so} rồi đến {dap_an_sau}")
            time.sleep(3)
            
            # Reset game để chơi tiếp
            tao_cau_hoi_moi()
            st.session_state.buoc = 2
            st.rerun()
        else:
            phat_am_thanh("Chưa đúng. Con hãy đếm thêm 1 đơn vị nữa nhé.")
            st.warning(f"Gợi ý: {st.session_state.so} thêm 1 là mấy nhỉ?")

# ================== FOOTER ==================
st.markdown("---")
st.caption("© 2025 - Bé Vui Học Toán cùng AI - Trường Mầm Non Bản Em")
