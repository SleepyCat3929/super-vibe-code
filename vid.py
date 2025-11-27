import numpy as np
import os
import subprocess

FBDEV = "/dev/fb0"
FB_WIDTH = 160
FB_HEIGHT = 128

# Open framebuffer
fb = os.open(FBDEV, os.O_RDWR)

cmd = [
    "rpicam-vid",
    "-t", "0",
    "--width", str(FB_WIDTH),
    "--height", str(FB_HEIGHT),
    "--raw",
    "--inline",
    "-o", "-"
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

def rgb888_to_rgb565(img):
    r = img[:,:,0] >> 3
    g = img[:,:,1] >> 2
    b = img[:,:,2] >> 3
    return ((r << 11) | (g << 5) | b).astype(np.uint16)

while True:
    # Read one frame from stdout
    raw_frame = proc.stdout.read(FB_WIDTH * FB_HEIGHT)  # adjust for Bayer format
    if not raw_frame:
        break

    # Debayer the frame (convert Bayer → RGB)
    # img = debayer(raw_frame)  # implement simple debayer
    # rgb565 = rgb888_to_rgb565(img)

    # Write to framebuffer
    os.lseek(fb, 0, os.SEEK_SET)
    os.write(fb, rgb565.tobytes())