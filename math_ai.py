import streamlit as st
import random
from deep_translator import GoogleTranslator

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Na Ư",
    page_icon="📐",
    layout="wide"
)

# --- CSS LÀM ĐẸP GIAO DIỆN ---
st.markdown("""
<style>
    /* Màu nền Gradient đẹp mắt */
    .stApp {
        background: linear-gradient(to right, #e0eafc, #cfdef3);
    }
    /* Khung tiêu đề trường học */
    .school-header {
        background-color: #1a237e;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    /* Khung bài tập */
    .problem-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #ff6f00;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    /* Nút bấm xịn hơn */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC AI SINH ĐỀ (MATH GENERATOR) ---
def sinh_de_phuong_trinh():
    # Sinh ngẫu nhiên hệ số a, b cho pt: ax + b = 0
    a = random.randint(2, 10)
    b = random.randint(1, 20) * random.choice([-1, 1])
    
    # --- SỬA LỖI HIỂN THỊ DẤU ---
    # Nếu b là số âm (ví dụ -7), hiển thị là " - 7" thay vì " + -7"
    if b < 0:
        de_bai = f"Giải phương trình: {a}x - {abs(b)} = 0"
    else:
        de_bai = f"Giải phương trình: {a}x + {b} = 0"
        
    dap_an = round(-b / a, 2)
    
    # Sửa lại câu gợi ý cho dễ hiểu hơn
    goi_y = f"Bước 1: Chuyển số {b} sang vế phải (nhớ đổi dấu thành {-b}). \nBước 2: Chia cả hai vế cho {a} để tìm x."
    
    return de_bai, dap_an, goi_y

def sinh_de_dien_tich():
    # Sinh bài toán hình học thực tế
    day_lon = random.randint(10, 20)
    day_be = random.randint(5, day_lon - 1)
    chieu_cao = random.randint(5, 15)
    de_bai = f"Một thửa ruộng bậc thang hình thang có đáy lớn {day_lon}m, đáy bé {day_be}m, chiều cao {chieu_cao}m. Tính diện tích?"
    dap_an = 0.5 * (day_lon + day_be) * chieu_cao
    goi_y = f"Công thức: (Đáy lớn + Đáy bé) nhân Chiều cao rồi chia 2.\n({day_lon} + {day_be}) * {chieu_cao} / 2"
    return de_bai, dap_an, goi_y

# Hàm dịch thuật (DÙNG THƯ VIỆN MỚI DEEP-TRANSLATOR)
def dich_sang_mong(text):
    try:
        # Sử dụng GoogleTranslator mới ổn định hơn
        translated = GoogleTranslator(source='vi', target='hmn').translate(text)
        return translated
    except:
        return "Đang kết nối AI ngôn ngữ..."

# --- GIAO DIỆN CHÍNH ---

# 1. Header Trường học
st.markdown("""
<div class="school-header">
    <h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>
    <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
    <p>ĐỊA CHỈ: XÃ SAM MỨN, HUYỆN ĐIỆN BIÊN</p>
    <h2>🚀 SẢN PHẨM: GIA SƯ TOÁN HỌC AI THÍCH ỨNG</h2>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar (Thanh bên trái)
with st.sidebar:
    # Dùng icon online cho ổn định
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.header("Cấu hình học tập")
    dang_toan = st.selectbox("Chọn chuyên đề ôn thi:", ["Phương trình bậc nhất (Đại số)", "Diện tích ruộng bậc thang (Thực tế)"])
    st.info("💡 Hệ thống sẽ tự động sinh đề phù hợp với năng lực của học sinh.")

# 3. Khu vực chính
col_trai, col_phai = st.columns([1.5, 1])

# Khởi tạo biến lưu đề bài nếu chưa có (Session State)
if 'de_bai_hien_tai' not in st.session_state:
    st.session_state.de_bai_hien_tai = ""
    st.session_state.dap_an_hien_tai = 0
    st.session_state.goi_y_hien_tai = ""

with col_trai:
    st.subheader("📝 Đề bài dành cho em:")
    
    # Nút sinh đề
    if st.button("🎲 TẠO ĐỀ BÀI MỚI (AI)", type="primary"):
        if "Phương trình" in dang_toan:
            db, da, gy = sinh_de_phuong_trinh()
        else:
            db, da, gy = sinh_de_dien_tich()
        
        st.session_state.de_bai_hien_tai = db
        st.session_state.dap_an_hien_tai = da
        st.session_state.goi_y_hien_tai = gy
    
    # Hiển thị đề bài trong khung đẹp
    if st.session_state.de_bai_hien_tai:
        st.markdown(f"""
        <div class="problem-card">
            <h3>{st.session_state.de_bai_hien_tai}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Nút dịch sang tiếng Mông
        if st.button("🗣️ Dịch sang tiếng H'Mông (Hỗ trợ học sinh)"):
            ban_dich = dich_sang_mong(st.session_state.de_bai_hien_tai)
            st.success(f"**Tiếng Mông:** {ban_dich}")

with col_phai:
    st.subheader("✍️ Khu vực làm bài")
    
    if st.session_state.de_bai_hien_tai:
        # Ô nhập đáp án
        cau_tra_loi = st.number_input("Nhập kết quả của em:", step=0.1)
        
        if st.button("✅ Nộp bài"):
            # So sánh đáp án (chấp nhận sai số nhỏ 0.01)
            if abs(cau_tra_loi - st.session_state.dap_an_hien_tai) < 0.01:
                st.balloons() # Hiệu ứng bóng bay chúc mừng
                st.success(f"TUYỆT VỜI! Em làm rất đúng! Đáp án là {st.session_state.dap_an_hien_tai}")
            else:
                st.error("Chưa đúng rồi, em thử lại nhé!")
                # Hiện gợi ý thông minh
                with st.expander("💡 Xem gợi ý của Gia sư AI"):
                    st.info(st.session_state.goi_y_hien_tai)
                    # Dịch gợi ý
                    st.write(f"*Gợi ý tiếng Mông:* {dich_sang_mong(st.session_state.goi_y_hien_tai)}")

# Footer
st.markdown("---")
st.caption("© 2025 Nhóm tác giả Trường PTDTBT TH&THCS Na Ư - Sản phẩm dự thi Chuyển đổi số Ngành Giáo dục.")
