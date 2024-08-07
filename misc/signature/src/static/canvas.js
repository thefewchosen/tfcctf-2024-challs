const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;

ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

canvas.addEventListener('mousedown', (e) => {
  isDrawing = true;
  ctx.beginPath();
  draw(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
});

canvas.addEventListener('mousemove', (e) => {
  if (isDrawing) {
    draw(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  }
});

canvas.addEventListener('mouseup', () => {
  isDrawing = false;
});

function draw(x, y) {
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';
  ctx.strokeStyle = '#000';
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
}

const submitBtn = document.getElementById('submit-btn');
submitBtn.addEventListener('click', () => {
  const image = canvas.toDataURL('image/png');
  sendDataToServer(image);

});

function sendDataToServer(imageData) {
  const url = '/';

  // Prepare the data to be sent as as URL-encoded format
  const formData = new URLSearchParams();
  formData.append('signature', imageData);

  const loadingText = document.getElementById('loading-text');
  loadingText.style.display = 'block';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData,
    timeout: 20000
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.text();
  })
  .then(data => {
    loadingText.style.display = 'none';
    const responseMessage = document.getElementById('response-message');
    responseMessage.textContent = data;

    const messagesContainer = document.getElementById('messages-container');
    messagesContainer.style.display = 'block';
  })
  .catch(error => {
    loadingText.style.display = 'none'
    console.error('Error:', error);
  });
}

const deleteBtn = document.getElementById('delete-btn');
deleteBtn.addEventListener('click', () => {
  clearCanvas();
});

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}