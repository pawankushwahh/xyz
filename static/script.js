function uploadVideo() {
    const fileInput = document.getElementById('video-file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/', {
        method: 'POST',
        body: formData,             
    })
    .then(response => response.json())
    .then(data => {
        const frameContainer = document.getElementById('frame-container');
        frameContainer.innerHTML = '';  // Clear any previous results

        // Debugging: Log the frames returned
        console.log("Frames:", data.frames);
        
        data.frames.forEach(framePath => {
            const imgElement = document.createElement('img');
            imgElement.src = framePath;
            imgElement.alt = "Video Frame";
            imgElement.style.width = '150px'; 
            imgElement.style.margin = '10px';  
            frameContainer.appendChild(imgElement);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


