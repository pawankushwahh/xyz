import cv2
import os

# Define the directory to save frames
output_dir = "frame"

# Ensure the 'frame' directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_frames(video_path, frame_interval=30):
    """
    Extracts frames from the specified video file and saves them in the 'frame' folder.

    Args:
        video_path (str): The path to the input video file.
        frame_interval (int): The interval between frames to save (e.g., every 30th frame).

    Returns:
        str: A message indicating the result of the operation.
    """
    # Check if the video file exists
    if not os.path.isfile(video_path):
        return f"Error: Video file not found at '{video_path}'"

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error: Unable to open video file. Please check the file path or format."

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # No more frames to process

        # Save every `frame_interval` frame
        if frame_count % frame_interval == 0:
            frame_name = os.path.join(output_dir, f"frame_{saved_count}.jpg")
            cv2.imwrite(frame_name, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    return f"Frame extraction complete! Total frames saved: {saved_count}"
