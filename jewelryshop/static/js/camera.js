// Tạo một phần tử video để hiển thị camera
const videoElement = document.createElement('video');
videoElement.style.position = 'fixed';
videoElement.style.bottom = '10px';
videoElement.style.right = '10px';
videoElement.style.width = '300px';
videoElement.style.height = 'auto';
videoElement.style.zIndex = '9999';

// Gắn phần tử video vào body của trang
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

// Function để chụp ảnh từ video
function captureImage(videoElement) {
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
}

// Function để gửi ảnh đến Face++ API và thu thập cảm xúc
function analyzeEmotion(imageBase64) {
    const apiKey = 'ONcTk7JuiiKdOvGqrv4';
    const apiSecret = 'smBnKo0oroUL7MgFOPbnYtjt3U-PucR9';
    const formData = new FormData();
    formData.append('api_key', apiKey);
    formData.append('api_secret', apiSecret);
    formData.append('image_base64', imageBase64.split(',')[1]);
    formData.append('return_attributes', 'emotion');

    fetch('https://api-us.faceplusplus.com/facepp/v3/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.faces && data.faces.length > 0) {
            const emotions = data.faces[0].attributes.emotion;
            sendEmotionDataToServer(emotions);
        } else {
            console.log('No faces detected.');
        }
    })
    .catch(err => {
        console.error("Error in Face++ API call: ", err);
    });
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
            happiness: emotions.happiness,
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
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Thiết lập để chụp ảnh và phân tích cảm xúc mỗi 5 giây
setInterval(() => {
    const imageBase64 = captureImage(videoElement);
    analyzeEmotion(imageBase64);
}, 10000);
