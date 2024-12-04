import os
import cv2

# Function to calculate image brightness
def calculate_brightness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.mean()

# Function to calculate image sharpness
def calculate_sharpness(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return laplacian.var()

# Function to filter and rank images
def rank_images(frame_folder, output_folder, top_n=10, brightness_threshold=50, sharpness_threshold=10, 
                resize_factor=0.5, compression_quality=50):
    """
    Ranks images in the frame folder based on brightness and sharpness.

    Args:
        frame_folder (str): Path to the folder containing input images.
        output_folder (str): Path to the folder to save ranked images.
        top_n (int): Number of top-ranked images to save.
        brightness_threshold (float): Minimum brightness for image selection.
        sharpness_threshold (float): Minimum sharpness for image selection.
        resize_factor (float): Resize factor for images (e.g., 0.5 = 50% size).
        compression_quality (int): Quality for JPEG compression (0-100).

    Returns:
        list: Details of saved ranked images (filename and score).
    """
    if not os.path.exists(frame_folder):
        return {"error": f"Folder '{frame_folder}' does not exist."}

    os.makedirs(output_folder, exist_ok=True)

    ranked_images = []
    for filename in os.listdir(frame_folder):
        file_path = os.path.join(frame_folder, filename)

        if not (filename.endswith(".jpg") or filename.endswith(".png")):
            continue

        image = cv2.imread(file_path)
        if image is None:
            continue

        # Resize image to decrease quality
        new_dim = (int(image.shape[1] * resize_factor), int(image.shape[0] * resize_factor))
        image_resized = cv2.resize(image, new_dim)

        brightness = calculate_brightness(image_resized)
        sharpness = calculate_sharpness(image_resized)

        # Apply filters
        if brightness > brightness_threshold and sharpness > sharpness_threshold:
            ranked_images.append((filename, brightness + sharpness, image_resized))

    # Sort by brightness + sharpness and save top N
    ranked_images.sort(key=lambda x: x[1], reverse=True)
    ranked_images = ranked_images[:top_n]

    saved_images = []
    for i, (filename, score, image) in enumerate(ranked_images):
        dst_path = os.path.join(output_folder, f"ranked_{i + 1}_{filename}")

        if dst_path.endswith(".jpg"):
            cv2.imwrite(dst_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality])
        else:
            cv2.imwrite(dst_path, image)

        saved_images.append({"filename": dst_path, "score": score})

    return {"success": True, "ranked_images": saved_images}
