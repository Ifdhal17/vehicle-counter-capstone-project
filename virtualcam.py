import pyvirtualcam
import cv2
from pyvirtualcam import PixelFormat

camera = cv2.VideoCapture("Untitled.mp4")

with pyvirtualcam.Camera(width=1230, height=932, fmt=PixelFormat.BGR, fps=24) as cam:

    while camera.isOpened():
        _, img = camera.read()
        cam.send(img)
        cam.sleep_until_next_frame()

    camera.release()
