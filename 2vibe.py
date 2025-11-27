import sys
import io
from PIL import Image
import numpy as np

WIDTH = 160
HEIGHT = 128
FB = "/dev/fb1"

fb = open(FB, "wb")

buffer = b""

while True:
    chunk = sys.stdin.buffer.read1(4096)
    if not chunk:
        break
    buffer += chunk

    # Detect JPEG frame boundaries (SOI and EOI)
    while True:
        start = buffer.find(b'\xff\xd8')  # JPEG Start
        end = buffer.find(b'\xff\xd9')    # JPEG End

        if start != -1 and end != -1 and end > start:
            jpg = buffer[start:end+2]
            buffer = buffer[end+2:]

            # Decode JPEG
            img = Image.open(io.BytesIO(jpg))
            img = img.resize((WIDTH, HEIGHT)).convert("RGB")

            arr = np.array(img)

            # Convert to RGB565
            r = (arr[:, :, 0] >> 3).astype(np.uint16)
            g = (arr[:, :, 1] >> 2).astype(np.uint16)
            b = (arr[:, :, 2] >> 3).astype(np.uint16)
            rgb565 = ((r << 11) | (g << 5) | b).astype(np.uint16)

            fb.seek(0)
            fb.write(rgb565.tobytes())
        else:
            break