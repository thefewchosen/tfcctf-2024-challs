async function fetchImages() {
  try {
      const response = await fetch('/uploads');
      const images = await response.json();
      renderImages(images);
  } catch (error) {
      console.error('Error fetching images:', error);
  }
}

function renderImages(images) {
  const gallery = document.getElementById('gallery');
  gallery.innerHTML = ''; // Clear existing content

  images.forEach((image, index) => {
      const imageCard = document.createElement('div');
      imageCard.className = 'image-card';
      
      const imageContainer = document.createElement('div');
      imageContainer.className = 'image-container';
      
      const img = document.createElement('img');
      img.src = `/static/images/${image}`;
      img.alt = `${image}`;

      const overlay = document.createElement('div');
      overlay.className = 'overlay';
      
      const viewButton = document.createElement('button');
      viewButton.className = 'icon-button';
      viewButton.innerHTML = '<i class="fas fa-eye"></i>';
      viewButton.onclick = () => openPopup(img.src);

      const reportButton = document.createElement('button');
      reportButton.className = 'icon-button';
      reportButton.innerHTML = '<i class="fas fa-flag"></i>';
      reportButton.onclick = () => reportImage(image);

      overlay.appendChild(viewButton);
      overlay.appendChild(reportButton);

      imageContainer.appendChild(img);
      imageContainer.appendChild(overlay);

      imageCard.appendChild(imageContainer);

      gallery.appendChild(imageCard);
  });
}

function openPopup(src) {
  const popup = document.getElementById('popup');
  const popupImg = document.getElementById('popup-img');
  popup.style.display = 'block';
  popupImg.src = src;

  // Update the URL with the image ID parameter
  const newUrl = new URL(window.location);
  newUrl.searchParams.set('image', imageId);
  window.history.pushState({}, '', newUrl);
}

function closePopup() {
  const popup = document.getElementById('popup');
  popup.style.display = 'none';

  // Remove the image parameter from the URL
  const newUrl = new URL(window.location);
  newUrl.searchParams.delete('image');
  window.history.pushState({}, '', newUrl);
}

// Custom Alert Function
function customAlert(message) {
  const alertBox = document.getElementById('customAlert');
  const alertMessage = document.getElementById('customAlertMessage');
  alertMessage.textContent = message;
  alertBox.style.display = 'block';
}

function closeCustomAlert() {
  const alertBox = document.getElementById('customAlert');
  alertBox.style.display = 'none';
}

// Override native alert
window.alert = function(message) {
  customAlert(message);
}

function previewImage(event) {
  const file = event.target.files[0];
  const fileName = document.getElementById('fileName');
  const imagePreview = document.getElementById('imagePreview');

  fileName.textContent = file ? file.name : 'No file chosen';

  if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
          imagePreview.innerHTML = `<img src="${e.target.result}" alt="Image Preview" class="preview-img">`;
      };
      reader.readAsDataURL(file);
  } else {
      imagePreview.innerHTML = '';
  }
}

function uploadImage() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
  .then(response => {
    if (response.ok) {
      alert('File uploaded successfully');
    } else {
      alert('File upload failed');
    }
  });
}

function reportImage(id) {
  fetch(`/report`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `id=${id}`,
  })
    .then(response => {
      if (response.ok) {
        alert('Image reported successfully');
      } else {
        alert('Image report failed');
      }
    });
}