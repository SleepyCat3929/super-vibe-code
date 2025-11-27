from picamera import PiCamera
import os

os.environ["FRAMEBUFFER"] = "/dev/fb0"

camera = PiCamera()
camera.resolution = (160, 128)
camera.start_preview()

try:
    while True:
        pass
except KeyboardInterrupt:
    camera.stop_preview()