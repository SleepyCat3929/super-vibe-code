import numpy as np
import os

FBDEV = "/dev/fb0"
FB_WIDTH = 160
FB_HEIGHT = 128

# Open framebuffer
fb = os.open(FBDEV, os.O_RDWR)

# Read raw frame
with open("frame.rgb", "rb") as f:
    data = np.frombuffer(f.read(), dtype=np.uint8)
    data = data.reshape((FB_HEIGHT, FB_WIDTH, 3))

# Convert RGB888 → RGB565
r = data[:,:,0] >> 3
g = data[:,:,1] >> 2
b = data[:,:,2] >> 3
rgb565 = ((r << 11) | (g << 5) | b).astype(np.uint16)

# Write to framebuffer
os.write(fb, rgb565.tobytes())
os.close(fb)