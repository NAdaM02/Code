import numpy as np
import sounddevice as sd
import cv2

# === Audio Config ===
SAMPLE_RATE = 44100
BLOCKSIZE = 1024
IMG_SIZE = 25

# === Get Stereo Mix device ===
devices = sd.query_devices()
try:
    device_id = next(i for i, d in enumerate(devices) if "Stereo Mix" in d['name'])
except StopIteration:
    raise RuntimeError("No 'Stereo Mix' device found. Make sure it's enabled in Windows Sound Settings.")

# === Visualizer Function ===
def generate_circle_image(audio_chunk, sample_rate=44100, size=25):
    """
    Generate a 25x25 grayscale image of a circle that pulses with audio energy.
    """
    # RMS energy
    energy = np.sqrt(np.mean(audio_chunk**2))

    # Map energy to radius (3 to 12 pixels)
    radius = int(3 + min(energy * 100, 1.0) * 9)

    # Create blank image
    img = np.zeros((size, size), dtype=np.uint8)

    # Draw filled white circle at center
    center = (size // 2, size // 2)
    cv2.circle(img, center, radius, color=255, thickness=-1)

    return img

# === Audio Callback ===
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    data = indata[:, 0]  # Use first channel

    img = generate_circle_image(data, sample_rate=SAMPLE_RATE, size=IMG_SIZE)

# === Main Loop ===
try:
    with sd.InputStream(device=device_id,
                        channels=1,
                        samplerate=SAMPLE_RATE,
                        blocksize=BLOCKSIZE,
                        callback=audio_callback):
        print("Press Ctrl+C to stop...")
        while True:
            sd.sleep(100)  # keep script alive
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    cv2.destroyAllWindows()
