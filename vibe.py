from picamera2 import Picamera2
from PIL import Image
import numpy as np

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (160, 128)}))
picam2.start()

# Open framebuffer
with open("/dev/fb1", "wb") as fb:
    while True:
        frame = picam2.capture_array()
        img = Image.fromarray(frame).resize((160, 128)).convert("RGB")

        # Convert to RGB565
        arr = np.array(img)
        r = (arr[:, :, 0] >> 3).astype(np.uint16)
        g = (arr[:, :, 1] >> 2).astype(np.uint16)
        b = (arr[:, :, 2] >> 3).astype(np.uint16)
        rgb565 = ((r << 11) | (g << 5) | b).astype(np.uint16)

        fb.seek(0)
        fb.write(rgb565.tobytes())
