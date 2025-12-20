<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vườn Thỏ Diệu Kỳ</title>
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap" rel="stylesheet">
    <style>
        /* 1. Thiết lập chung */
        body {
            margin: 0;
            padding: 0;
            overflow: hidden; /* Ẩn thanh cuộn */
            font-family: 'Baloo 2', cursive;
            background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 100%); /* Bầu trời xanh */
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        /* 2. Phần trang trí nền (Mây và Cỏ) */
        .cloud {
            position: absolute;
            background: white;
            border-radius: 50px;
            opacity: 0.8;
            animation: floatCloud 20s linear infinite;
        }
        
        .cloud:nth-child(1) { width: 100px; height: 40px; top: 10%; left: -10%; animation-duration: 25s; }
        .cloud:nth-child(2) { width: 150px; height: 60px; top: 20%; left: -20%; animation-duration: 35s; animation-delay: 5s; }
        .cloud:nth-child(3) { width: 80px; height: 30px; top: 15%; left: -15%; animation-duration: 18s; animation-delay: 10s; }

        .grass {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 150px;
            background: linear-gradient(to top, #4CAF50, #8BC34A);
            border-top-left-radius: 50% 20px;
            border-top-right-radius: 50% 20px;
            z-index: 1;
        }

        /* 3. Nhân vật Thỏ (Rabbit) */
        .rabbit-container {
            position: relative;
            z-index: 10;
            cursor: pointer;
            transition: transform 0.3s;
        }

        .rabbit-container:active {
            transform: scale(0.9); /* Hiệu ứng nhấn xuống */
        }

        .rabbit-img {
            width: 250px; /* Thỏ to, rõ ràng */
            height: auto;
            filter: drop-shadow(0 10px 10px rgba(0,0,0,0.2));
            animation: bounce 3s infinite ease-in-out;
        }

        /* Bong bóng lời thoại */
        .speech-bubble {
            position: absolute;
            top: -60px;
            right: -40px;
            background: #fff;
            padding: 15px 25px;
            border-radius: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            font-size: 1.2rem;
            color: #FF6F00;
            font-weight: 800;
            opacity: 0;
            transform: scale(0);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .speech-bubble.show {
            opacity: 1;
            transform: scale(1);
        }

        .speech-bubble::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 20px;
            border-width: 10px 10px 0;
            border-style: solid;
            border-color: #fff transparent;
        }

        /* 4. Tiêu đề và Nút bấm */
        .ui-container {
            text-align: center;
            z-index: 20;
            margin-top: 20px;
        }

        h1 {
            color: #FF4081;
            font-size: 3rem;
            text-shadow: 3px 3px 0px #fff;
            margin: 0 0 20px 0;
            animation: wiggle 3s infinite;
        }

        .start-btn {
            background-color: #FFC107;
            color: #fff;
            border: none;
            padding: 15px 40px;
            font-size: 1.5rem;
            font-family: 'Baloo 2', cursive;
            font-weight: 800;
            border-radius: 50px;
            box-shadow: 0 8px 0 #FFA000, 0 15px 20px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
        }

        .start-btn:hover {
            transform: translateY(-5px);
            background-color: #FFD54F;
            box-shadow: 0 13px 0 #FFA000, 0 20px 20px rgba(0,0,0,0.2);
        }

        .start-btn:active {
            transform: translateY(4px);
            box-shadow: 0 4px 0 #FFA000, 0 8px 10px rgba(0,0,0,0.2);
        }

        /* 5. Định nghĩa chuyển động (Animations) */
        @keyframes floatCloud {
            0% { transform: translateX(100vw); }
            100% { transform: translateX(-200px); }
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        @keyframes wiggle {
            0%, 100% { transform: rotate(-3deg); }
            50% { transform: rotate(3deg); }
        }

    </style>
</head>
<body>

    <div class="cloud"></div>
    <div class="cloud"></div>
    <div class="cloud"></div>

    <div class="rabbit-container" onclick="rabbitTalk()">
        <img src="https://cdn-icons-png.flaticon.com/512/3069/3069172.png" alt="Chú Thỏ" class="rabbit-img">
        <div class="speech-bubble" id="bubble">Chào bé! Chơi với tớ đi! ❤️</div>
    </div>

    <div class="ui-container">
        <h1>Bé Vui Học Toán</h1>
        <button class="start-btn" onclick="startGame()">Vào Học Thôi!</button>
    </div>

    <div class="grass"></div>

    <script>
        // Hàm khi click vào thỏ
        function rabbitTalk() {
            const bubble = document.getElementById('bubble');
            const messages = [
                "Chào bé ngoan! 👋",
                "Cùng học nhé! 📚",
                "Bé giỏi quá! 🌟",
                "Hi hi hi! 😂",
                "Bấm nút màu vàng đi! 👇"
            ];
            
            // Chọn ngẫu nhiên một câu nói
            const randomMsg = messages[Math.floor(Math.random() * messages.length)];
            bubble.innerText = randomMsg;
            
            // Hiện bong bóng chat
            bubble.classList.add('show');

            // Ẩn sau 2 giây
            setTimeout(() => {
                bubble.classList.remove('show');
            }, 2000);
        }

        // Hàm khi bấm nút Bắt đầu
        function startGame() {
            // Hiệu ứng hoặc chuyển trang
            alert("Chuyển đến bài học đầu tiên...");
            // window.location.href = "bai-hoc-1.html"; // Bỏ comment dòng này để chuyển trang thật
        }
    </script>
</body>
</html>
