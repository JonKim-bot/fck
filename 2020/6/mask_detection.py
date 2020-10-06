from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

import board
import busio as io
import adafruit_mlx90614
import time
import os

os.environ['OPENVC_VIDEOIO_PRIORITY_MSMF'] = '0'
model = load_model('models/mask_detector.h5')
cap = cv2.VideoCapture(0,cv2.CAP_V4L2)

camera = PiCamera()
camera.rotation = 180
# camera.framerate = 32
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)


def detect_mask(image):
    copy_img = image.copy()

    resized = cv2.resize(copy_img, (254, 254))

    resized = img_to_array(resized)
    resized = preprocess_input(resized)

    resized = np.expand_dims(resized, axis=0)

    mask, _ = model.predict([resized])[0]

    return mask


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    ret = True

    if ret:

        mask_prob = detect_mask(img)

        if mask_prob > 0.5:
            cv2.putText(img, 'Mask Detected', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 0), 3)

            print("mask detected")
            cv2.destroyAllWindows()



            cap.release()
            break
        
        elif mask_prob < 0.5:
             cv2.putText(img, 'No Mask', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
             cap.release()
             cv2.destroyAllWindows()
             break
#             for i in range(5):
#                 time.sleep(2)
#                 cv2.putText(img, 'No Mask' + str(i), (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
#                 cv2.imshow('window', img)
#             print("no mark detected")
            
        cv2.imshow('window', img)

    else:
        cv2.imshow('window', img)
    
    rawCapture.truncate(0)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('a'):
        cv2.imwrite('my_pic.jpg', img)


cap.release()
print("cap released")
cv2.destroyAllWindows()

