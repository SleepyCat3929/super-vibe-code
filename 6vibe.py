import cv2
import numpy as np
import os

FBDEV = "/dev/fb0"
FB_WIDTH = 160
FB_HEIGHT = 128

# Open framebuffer
fb = os.open(FBDEV, os.O_RDWR)

# Open camera with OpenCV (uses libcamera backend)
cap = cv2.VideoCapture(0)  # 0 = default camera

def rgb888_to_rgb565(frame):
    r = frame[:,:,2] >> 3  # OpenCV uses BGR
    g = frame[:,:,1] >> 2
    b = frame[:,:,0] >> 3
    rgb565 = (r << 11) | (g << 5) | b
    return rgb565.astype(np.uint16)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Resize to 160x128
    frame = cv2.resize(frame, (FB_WIDTH, FB_HEIGHT))

    # Convert to RGB565
    rgb565 = rgb888_to_rgb565(frame)

    # Write to framebuffer
    os.lseek(fb, 0, os.SEEK_SET)
    os.write(fb, rgb565.tobytes())