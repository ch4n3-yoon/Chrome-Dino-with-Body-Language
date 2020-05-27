import tensorflow.keras
import cv2
from PIL import Image, ImageOps
import numpy as np
import keyboard

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('./Model/keras_model.h5')

# webcam size : 480 x 640
data = np.ndarray(shape=(1, 480, 640, 3), dtype=np.float32)

# 0 : default camera mode
cap = cv2.VideoCapture(0)

i = 0
while cap.isOpened():
    i += 1

    success, frame = cap.read()
    if success:
        cv2.imshow('Camera Window', frame)

        # press ESC key to quit
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        # code to reduce calculating
        if i % 7 != 0:
            continue

        # Normalize the image
        normalized_image_array = (frame.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array
        [[jump, hold]] = model.predict(data)

        # for debugging
        print("[*] prediction :")
        print(" - Jump :", jump * 100)
        print(" - Hold :", hold * 100)


        if hold * 100 < 1:
            keyboard.send_spacebar()



cap.release()
cv2.destroyAllWindows()
