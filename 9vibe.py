from PIL import Image
import numpy as np
import os
import subprocess
import time

FBDEV = "/dev/fb0"
FB_WIDTH = 160
FB_HEIGHT = 128

# Open framebuffer
fb = os.open(FBDEV, os.O_RDWR)

def rgb888_to_rgb565(img):
    r = img[:,:,0] >> 3
    g = img[:,:,1] >> 2
    b = img[:,:,2] >> 3
    return ((r << 11) | (g << 5) | b).astype(np.uint16)

try:
    while True:
        # Capture JPEG with libcamera
        subprocess.run([
            "rpicam-still",
            "-o", "frame.jpg",
            "--width", str(FB_WIDTH),
            "--height", str(FB_HEIGHT),
            "--nopreview",
            "-t", "100"
        ], check=True)

        # Open and resize the image
        img = Image.open("frame.jpg").convert("RGB").resize((FB_WIDTH, FB_HEIGHT))
        frame = np.array(img, dtype=np.uint8)

        # Convert to RGB565
        rgb565 = rgb888_to_rgb565(frame)

        # Write to framebuffer
        os.lseek(fb, 0, os.SEEK_SET)
        os.write(fb, rgb565.tobytes())

        # Optional: small delay to control FPS
        time.sleep(0.05)  # ~20 FPS

except KeyboardInterrupt:
    print("Exiting...")
finally:
    os.close(fb)