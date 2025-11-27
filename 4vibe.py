from picamera2 import Picamera2
import numpy as np
import time
import os

# Framebuffer properties for ST7735S via fbcp-ili9341
FB_WIDTH = 160
FB_HEIGHT = 128
FBDEV = "/dev/fb0"

# Initialize camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (FB_WIDTH, FB_HEIGHT), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

# Open framebuffer
fb = os.open(FBDEV, os.O_RDWR)

def rgb888_to_rgb565(img):
    r = img[:,:,0] >> 3
    g = img[:,:,1] >> 2
    b = img[:,:,2] >> 3
    rgb565 = (r << 11) | (g << 5) | b
    return rgb565.astype(np.uint16)

try:
    while True:
        frame = picam2.capture_array()

        # Convert to RGB565
        rgb565 = rgb888_to_rgb565(frame)

        # Write to framebuffer
        os.lseek(fb, 0, os.SEEK_SET)
        os.write(fb, rgb565.tobytes())

except KeyboardInterrupt:
    pass

os.close(fb)
picam2.stop()