import subprocess
import os
import time
import numpy as np

FBDEV = "/dev/fb0"
FB_WIDTH = 160
FB_HEIGHT = 128
fb = os.open(FBDEV, os.O_RDWR)

def rgb888_to_rgb565(frame):
    r = frame[:,:,0] >> 3
    g = frame[:,:,1] >> 2
    b = frame[:,:,2] >> 3
    return ((r << 11) | (g << 5) | b).astype(np.uint16)

try:
    while True:
        # Capture raw frame from libcamera-still
        subprocess.run([
            "rpicam-still",
            "-o", "frame.rgb",
            "--width", str(FB_WIDTH),
            "--height", str(FB_HEIGHT),
            "--raw",
            "--nopreview"
        ])

        # Read raw RGB frame
        data = np.fromfile("frame.rgb", dtype=np.uint8).reshape(FB_HEIGHT, FB_WIDTH, 3)

        # Convert to RGB565
        rgb565 = rgb888_to_rgb565(data)

        # Write to framebuffer
        os.lseek(fb, 0, os.SEEK_SET)
        os.write(fb, rgb565.tobytes())

        # Optional: small delay to control FPS
        time.sleep(0.05)

except KeyboardInterrupt:
    os.close(fb)