import subprocess
import signal

# Framebuffer and display resolution
FB_WIDTH = 160
FB_HEIGHT = 128
FBDEV = "/dev/fb0"

# Build libcamera-vid command
cmd = [
    "libcamera-vid",
    "-t", "0",  # run indefinitely
    "--width", str(FB_WIDTH),
    "--height", str(FB_HEIGHT),
    "--nopreview",  # no X11 preview
    "-o", FBDEV
]

# Start streaming
process = subprocess.Popen(cmd, preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN))

try:
    print("Streaming camera to framebuffer. Press Ctrl+C to stop.")
    process.wait()
except KeyboardInterrupt:
    print("Stopping...")
    process.terminate()
    process.wait()