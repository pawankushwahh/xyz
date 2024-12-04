from flask import Flask, request, jsonify, render_template, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)

# Directory to save uploaded videos and images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to extract frames from the video
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    return frames


# Function to analyze frames (sharpness and brightness)
def analyze_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()  # Sharpness measure
    brightness = np.mean(gray)  # Brightness measure
    return sharpness, brightness


# Serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Route to handle file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            frames = extract_frames(filename)
            
            frame_data = []
            for idx, frame in enumerate(frames):
                sharpness, brightness = analyze_frame(frame)
                frame_data.append({
                    'index': idx,
                    'sharpness': sharpness,
                    'brightness': brightness,
                })
            
            # Sort frames by sharpness and brightness
            frame_data.sort(key=lambda x: (x['sharpness'], x['brightness']), reverse=True)
            
            # Save top 10 frames and return their URLs
            top_frames = frame_data[:10]
            top_frame_urls = []
            for i, data in enumerate(top_frames):
                frame_path = os.path.join(app.config['UPLOAD_FOLDER'], f"frame_{i}.jpg")
                cv2.imwrite(frame_path, frames[data['index']])
                top_frame_urls.append(f"/uploads/frame_{i}.jpg")
            
            return jsonify({'frames': top_frame_urls})
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
