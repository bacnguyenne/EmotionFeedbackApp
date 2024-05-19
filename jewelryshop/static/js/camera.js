// Tạo một phần tử video để hiển thị camera
const videoElement = document.createElement('video');
videoElement.style.position = 'fixed';
videoElement.style.bottom = '10px';
videoElement.style.right = '10px';
videoElement.style.width = '300px';
videoElement.style.height = 'auto';
videoElement.style.zIndex = '9999';
document.body.appendChild(videoElement);

// Yêu cầu quyền truy cập camera và hiển thị nó trong phần tử video
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        videoElement.srcObject = stream;
        videoElement.play();
    })
    .catch(err => {
        console.error("Lỗi khi truy cập camera: ", err);
    });

// Function để gửi văn bản đến API phân tích cảm xúc
async function analyzeEmotion(text) {
    const axios = require('axios');

    const options = {
        method: 'GET',
        url: 'https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/',
        params: { text: text },
        headers: {
            'X-RapidAPI-Key': 'b6e563cec0msh651e063bea4564ep1222d3jsne387d41008ff',
            'X-RapidAPI-Host': 'twinword-emotion-analysis-v1.p.rapidapi.com'
        }
    };

    try {
        const response = await axios.request(options);
        console.log(response.data);
        sendEmotionDataToServer(response.data.emotion_scores);
    } catch (error) {
        console.error(error);
    }
}

// Function để gửi dữ liệu cảm xúc đến server
function sendEmotionDataToServer(emotions) {
    fetch('/save_emotion_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Đảm bảo bạn đã có hàm getCookie để lấy CSRF token
        },
        body: JSON.stringify({
            joy: emotions.joy,
            sadness: emotions.sadness,
            surprise: emotions.surprise,
            anger: emotions.anger,
            fear: emotions.fear,
            disgust: emotions.disgust
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data sent to server: ', data);
    })
    .catch(err => {
        console.error("Error sending data to server: ", err);
    });
}

// Hàm lấy CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Lấy văn bản để phân tích cảm xúc từ người dùng
function getTextForEmotionAnalysis() {
    return "After living abroad for such a long time, seeing my family was the best present I could have ever wished for.";
}

// Thiết lập để phân tích cảm xúc mỗi 5 giây
setInterval(() => {
    const text = getTextForEmotionAnalysis();
    analyzeEmotion(text);
}, 5000);
