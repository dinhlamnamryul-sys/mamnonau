import streamlit as st
import random
from gtts import gTTS
import uuid, os
import time

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Vườn Thỏ Diệu Kỳ",
    page_icon="🐰",
    layout="centered"
)

# ================== CSS CHUYÊN BIỆT CHO TRẺ EM ==================
st.markdown("""
<style>
    /* Nhúng font chữ trẻ em dễ thương */
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap');

    /* 1. Nền bầu trời và thảm cỏ */
    .stApp {
        background: linear-gradient(to bottom, #87CEEB 0%, #B3E5FC 70%, #76FF03 70%, #64DD17 100%);
        font-family: 'Baloo 2', cursive;
    }

    /* 2. Ẩn menu mặc định của Streamlit cho gọn */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. Hiệu ứng đám mây bay */
    @keyframes float {
        0% { transform: translateX(0px); }
        50% { transform: translateX(20px); }
        100% { transform: translateX(0px); }
    }
    
    /* 4. Hiệu ứng Thỏ nhún nhảy */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .rabbit-img {
        width: 250px;
        animation: bounce 2s infinite;
        margin-bottom: -20px;
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.2));
    }

    /* 5. Bong bóng lời thoại */
    .bubble {
        position: relative;
        background: #fff;
        border-radius: 30px;
        padding: 20px;
        text-align: center;
        color: #000;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 4px solid #FF9800;
        margin-bottom: 20px;
        animation: float 3s infinite ease-in-out;
    }
    .bubble:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 0;
        border: 20px solid transparent;
        border-top-color: #FF9800;
        border-bottom: 0;
        margin-left: -20px;
        margin-bottom: -20px;
    }

    /* 6. Thẻ hiển thị số to */
    .number-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        font-size: 50px;
        color: #D50000;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* 7. Nút bấm đẹp như kẹo */
    .stButton>button {
        width: 100%;
        background-color: #FFEB3B !important;
        color: #D50000 !important;
        font-family: 'Baloo 2', cursive !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        border: 4px solid #FBC02D !important;
        box-shadow: 0 6px 0 #F9A825 !important;
        transition: all 0.1s;
        margin-top: 10px;
    }
    .stButton>button:active {
        transform: translateY(4px);
        box-shadow: 0 2px 0 #F9A825 !important;
    }
    
    /* 8. Input nhập số */
    .stNumberInput input {
        font-size: 30px;
        text-align: center;
        color: #E91E63;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ================== HÀM HỖ TRỢ ==================
def phat_am_thanh(text):
    """Phát âm thanh không bị lỗi file cũ"""
    try:
        filename = f"sound_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang="vi")
        tts.save(filename)
        audio_file = open(filename, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        audio_file.close()
        os.remove(filename)
    except Exception as e:
        pass # Bỏ qua nếu lỗi âm thanh để không treo app

def hien_thi_tho(loi_noi):
    """Hiển thị thỏ và bong bóng chat"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Bong bóng lời thoại
        st.markdown(f'<div class="bubble">{loi_noi}</div>', unsafe_allow_html=True)
        # Hình ảnh thỏ (Dùng link ảnh online ổn định)
        st.markdown(
            '<div style="text-align: center;">'
            '<img src="https://cdn-icons-png.flaticon.com/512/4086/4086392.png" class="rabbit-img">'
            '</div>', 
            unsafe_allow_html=True
        )

# ================== DỮ LIỆU GAME ==================
do_vat = {
    "🍎": "quả táo",
    "🐟": "con cá",
    "🌸": "bông hoa",
    "🐰": "bạn thỏ",
    "⭐": "ngôi sao",
    "🍬": "viên kẹo"
}

chu_so = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

# ================== QUẢN LÝ TRẠNG THÁI ==================
if "buoc" not in st.session_state:
    st.session_state.buoc = 1
    st.session_state.so = random.randint(1, 5) # Mới đầu học số nhỏ thôi
    st.session_state.hinh = "🍎"
    st.session_state.ten = "quả táo"

def tao_cau_hoi_moi():
    st.session_state.so = random.randint(1, 10)
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))

# ================== GIAO DIỆN CHÍNH ==================

# --- Header ẩn (Dùng khoảng trắng để đẩy nội dung xuống dưới mây) ---
st.write("") 

# ================== BƯỚC 1: MÀN HÌNH CHÀO ==================
if st.session_state.buoc == 1:
    hien_thi_tho("Xin chào bé! <br> Mình là Thỏ Bông.<br> Cùng học đếm nhé! ❤️")
    
    # Chỉ phát âm thanh lần đầu load trang
    if 'intro_played' not in st.session_state:
        phat_am_thanh("Xin chào bé! Mình là Thỏ Bông. Cùng học đếm nhé!")
        st.session_state.intro_played = True

    col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
    with col_btn2:
        if st.button("🚀 BẮT ĐẦU THÔI"):
            st.session_state.buoc = 2
            st.rerun()

# ================== BƯỚC 2: HỌC ĐẾM (HIỂN THỊ) ==================
elif st.session_state.buoc == 2:
    hien_thi_tho(f"Bé ơi! Ở đây có bao nhiêu {st.session_state.ten} nhỉ?")
    
    # Hiển thị vật thể to rõ
    st.markdown(f"""
    <div class="number-card">
        {' '.join([st.session_state.hinh] * st.session_state.so)}
    </div>
    """, unsafe_allow_html=True)
    
    phat_am_thanh(f"Bé ơi! Ở đây có bao nhiêu {st.session_state.ten} nhỉ?")
    
    time.sleep(1) # Đợi xíu cho bé nhìn
    
    if st.button("👉 XEM ĐÁP ÁN"):
        st.session_state.buoc = 3
        st.rerun()

# ================== BƯỚC 3: KẾT QUẢ ĐẾM ==================
elif st.session_state.buoc == 3:
    hien_thi_tho(f"A! Có tất cả <b>{st.session_state.so}</b> {st.session_state.ten} đấy!")
    
    st.markdown(f"""
    <div class="number-card" style="color: #2E7D32;">
        {st.session_state.so}<br>
        <span style="font-size: 20px;">({chu_so[st.session_state.so]})</span>
    </div>
    """, unsafe_allow_html=True)
    
    phat_am_thanh(f"Có tất cả {st.session_state.so} {st.session_state.ten}. Số {st.session_state.so}.")

    if st.button("🎮 CHƠI TRÒ CHƠI"):
        st.session_state.buoc = 4
        st.rerun()

# ================== BƯỚC 4: TRÒ CHƠI KIỂM TRA ==================
elif st.session_state.buoc == 4:
    hien_thi_tho(f"Đố bé biết: <br> Có bao nhiêu {st.session_state.ten} ở dưới?")
    
    st.markdown(f"""
    <div class="number-card">
        {' '.join([st.session_state.hinh] * st.session_state.so)}
    </div>
    """, unsafe_allow_html=True)

    # Input nhập số
    tra_loi = st.number_input("Bé nhập số vào đây nhé:", 0, 20, 0)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kiểm tra ✅"):
            if tra_loi == st.session_state.so:
                st.balloons()
                phat_am_thanh("Hoan hô! Bé đếm đúng rồi!")
                time.sleep(1)
                st.session_state.buoc = 5
                st.rerun()
            else:
                phat_am_thanh(f"Chưa đúng rồi. Bé đếm lại xem nhé!")
                st.error("Bé đếm lại kỹ hơn nhé!")
    
    with col2:
        if st.button("Đổi câu khác 🔄"):
            tao_cau_hoi_moi()
            st.rerun()

# ================== BƯỚC 5: CÂU HỎI TƯ DUY (+1) ==================
elif st.session_state.buoc == 5:
    dap_an_sau = st.session_state.so + 1
    hien_thi_tho(f"Bé giỏi quá! <br> Thế số đứng sau số {st.session_state.so} là số mấy?")
    
    st.markdown(f"""
    <div class="number-card">
        {st.session_state.so} ➡️ ❓
    </div>
    """, unsafe_allow_html=True)

    tra_loi_sau = st.number_input("Số tiếp theo là:", 0, 20, 0)

    if st.button("Trả lời 🎁"):
        if tra_loi_sau == dap_an_sau:
            st.snow() # Hiệu ứng tuyết rơi chúc mừng
            phat_am_thanh("Tuyệt vời! Con rất thông minh!")
            st.success(f"Đúng rồi! Sau số {st.session_state.so} là số {dap_an_sau}")
            time.sleep(2)
            
            # Reset game
            tao_cau_hoi_moi()
            st.session_state.buoc = 2
            st.rerun()
        else:
            phat_am_thanh("Sai rồi. Con nhớ lại dãy số nhé.")
            st.warning("Gợi ý: Con đếm thêm 1 nữa nhé!")

# ================== FOOTER (Tác giả) ==================
st.markdown("---")
st.caption("🎨 Sản phẩm giáo dục mầm non - Thiết kế rực rỡ cho bé vui học")
