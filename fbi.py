import subprocess
import time

FBDEV = "/dev/fb0"
WIDTH = 160
HEIGHT = 128

try:
    while True:
        # Capture JPEG from camera
        subprocess.run([
            "rpicam-still",
            "-o", "frame.jpg",
            "--width", str(WIDTH),
            "--height", str(HEIGHT),
            "--nopreview",
            "-t", "100"  # short exposure
        ], check=True)

        # Display the JPEG on framebuffer using fbi
        subprocess.run([
            "fbi",
            "-T", "1",         # virtual console 1
            "-d", FBDEV,       # framebuffer device
            "-noverbose",
            "-a",              # auto-scale to fit
            "frame.jpg"
        ], check=True)

        time.sleep(0.05)  # optional delay (~20 FPS)

except KeyboardInterrupt:
    print("Exiting...")