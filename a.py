import cv2
import os

def adjust_brightness(image, brightness_factor):
    """
    Adjust the brightness of the input image.

    Args:
        image: Input image (numpy array).
        brightness_factor: Brightness adjustment factor.
                           1.0 indicates no change, less than 1.0 decreases brightness,
                           and greater than 1.0 increases brightness.

    Returns:
        Adjusted image.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Multiply the V (Value) channel by the brightness factor
    v = cv2.multiply(v, brightness_factor).astype('uint8')

    # Combine the adjusted V channel with the original H and S channels
    adjusted_hsv = cv2.merge([h, s, v])

    # Convert back to BGR color space
    adjusted_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)
    return adjusted_image

def capture_photos(output_folder, num_photos_per_angle=10, brightness_factor=1.5):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    angles=[]
    for i in range(180):
        angles.append(i)
    # List of angles to capture photos from
    count =0

    for angle in angles:
        for i in range(num_photos_per_angle):
            # Capture frame from the webcam
            ret, frame = cap.read()

            # Rotate the frame by the specified angle
            rows, cols, _ = frame.shape
            rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
            rotated_frame = cv2.warpAffine(frame, rotation_matrix, (cols, rows))

            # Adjust brightness of the rotated frame
            adjusted_frame = adjust_brightness(rotated_frame, brightness_factor)

            # Save the captured photo
            # photo_name = f'angle_{angle}_photo_{i}.jpg'
            count+=1
            print(count)
            photo_name = f'{count}.png'
            photo_path = os.path.join(output_folder, photo_name)
            cv2.imwrite(photo_path, adjusted_frame)

    # Release the webcam
    cap.release()

# Specify the output folder where the captured photos will be saved
output_folder = 'face_detection_database'

# Specify the number of photos to capture per angle
num_photos_per_angle = 5

# Specify the brightness adjustment factor
brightness_factor = 1.5  # Increase or decrease as needed

# Call the function to capture photos
capture_photos(output_folder, num_photos_per_angle, brightness_factor)


