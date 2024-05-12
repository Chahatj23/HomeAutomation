import random
import threading
import cv2
import os
from waitress import serve
import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

def upload_image_to_storage(image_path, destination_path):
    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url

def adjust_brightness(image, brightness_factor):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.multiply(v, brightness_factor).astype('uint8')
    adjusted_hsv = cv2.merge([h, s, v])
    adjusted_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)
    return adjusted_image

def capture_photos(output_folder, num_photos_per_angle=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    cap = cv2.VideoCapture(0)
    angles = list(range(0, 180,5))
    images = []
    count = 1
    total_iterations = len(angles) * num_photos_per_angle
    for angle in angles:
        for i in range(num_photos_per_angle):
            ret, frame = cap.read()
            rows, cols, _ = frame.shape
            rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
            rotated_frame = cv2.warpAffine(frame, rotation_matrix, (cols, rows))
            brightness_factor = 2 * random.random()
            adjusted_frame = adjust_brightness(rotated_frame, brightness_factor)
            count += 1
            photo_name = f'{count}.png'
            photo_path = os.path.join(output_folder, photo_name)
            cv2.imwrite(photo_path, adjusted_frame)
            images.append(photo_path)

    cap.release()
    return images

def capture_and_upload():
    output_folder = "face_detection_database/"
    num_photos_per_angle = 5
    while True:
        images = capture_photos(output_folder, num_photos_per_angle)
        for i, image_path in enumerate(images):
            destination_path = f"images/{i}.png"
            image_url = upload_image_to_storage(image_path, destination_path)
            if(i==89):
                return
            print("Image uploaded. URL:", image_url)

@app.route('/capture_photos', methods=['POST'])
def handle_capture_photos():
    t = threading.Thread(target=capture_and_upload)
    t.start()
    return jsonify({'message': 'Photos capture and upload process started.'})

if __name__ == '__main__':
    cred = credentials.Certificate("doorlock-f45f3-firebase-adminsdk-cxiwp-d1b48b4e9a.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'doorlock-f45f3.appspot.com'})
    app.run(debug=True)
    #serve(app, host='0.0.0.0', port=5000)
    #serve(app, host='0.0.0.0', port=5000, threads=4)
    db = firestore.client()
    doc_ref = db.collection('users').document('user_id')
    doc_ref.set({'name': 'John Doe', 'email': 'johndoe@example.com'})
