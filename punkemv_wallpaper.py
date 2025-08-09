from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import math
import os
import cv2
import glob

# ===== FUTURISTIC CONFIG =====
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (5, 5, 15)  # Deep space black
NEON_COLORS = [
    (0, 255, 157),   # Matrix green
    (255, 20, 147),  # Cyber pink
    (0, 191, 255),   # Electric blue
    (138, 43, 226)   # Purple haze
]
FPS = 60
DURATION_SEC = 5
TOTAL_FRAMES = FPS * DURATION_SEC
# ===========================

def install_dependencies():
    print("⚙️ Installing dependencies...")
    os.system("pip install opencv-python numpy")
    os.system("apt-get update && apt-get install -y ffmpeg")

def create_hologram_effect(img):
    """Adds holographic scanlines and chromatic aberration"""
    arr = np.array(img)
    
    # Chromatic aberration
    for i in range(3):  # For each RGB channel
        offset = random.randint(1, 3)
        arr[:, :, i] = np.roll(arr[:, :, i], offset * (-1 if i % 2 else 1), axis=1)
    
    # Scanlines
    scanline_intensity = 0.3
    for y in range(0, HEIGHT, 2):
        arr[y, :, :] = arr[y, :, :] * (1 - scanline_intensity)
    
    # Bloom effect
    blurred = cv2.GaussianBlur(arr, (0, 0), 2)
    arr = cv2.addWeighted(arr, 0.8, blurred, 0.2, 0)
    
    return Image.fromarray(arr)

def generate_cyber_frame(frame_num):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    
    # Animated data core (pulsing center)
    core_size = 100 + 20 * math.sin(frame_num / 10)
    core_x, core_y = WIDTH // 2, HEIGHT // 2
    for i in range(5, 0, -1):
        draw.ellipse([
            core_x - core_size * i, 
            core_y - core_size * i,
            core_x + core_size * i, 
            core_y + core_size * i
        ], outline=random.choice(NEON_COLORS), width=2)
    
    # Binary rain
    for _ in range(150):
        x = random.randint(0, WIDTH)
        speed = random.randint(2, 5)
        y = (frame_num * speed) % HEIGHT
        char = random.choice(["0", "1", " "])
        draw.text((x, y), char, fill=(0, 255, 0, 100), 
                font=ImageFont.load_default())
    
    # Floating PUNKEMV text (holographic)
    text = "PUNKEMV"
    for i, char in enumerate(text):
        offset = 10 * math.sin(frame_num/5 + i)
        draw.text(
            (1200 + i * 80, 400 + offset),
            char,
            fill=random.choice(NEON_COLORS),
            font=ImageFont.truetype("arial.ttf", 72),
            stroke_width=2,
            stroke_fill=(255, 255, 255, 50)
        )
    
    # Data stream (animated)
    stream_y = 200 + 50 * math.sin(frame_num / 8)
    hex_data = " ".join([f"{random.randint(0,255):02X}" for _ in range(25)])
    draw.text((100, stream_y), hex_data, fill=(0, 255, 157), 
             font=ImageFont.truetype("arial.ttf", 24))
    
    return create_hologram_effect(canvas)

def main():
    install_dependencies()
    os.makedirs("frames", exist_ok=True)
    
    print(f"🌀 Generating {TOTAL_FRAMES} cyber-frames...")
    for frame in range(TOTAL_FRAMES):
        generate_cyber_frame(frame).save(f"frames/frame_{frame:04d}.png")
        print(f"⚡ Progress: {frame+1}/{TOTAL_FRAMES}", end="\r")
    for _ in range(50):
    x1, y1 = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    x2, y2 = x1 + random.randint(20, 100), y1 + random.randint(-10, 10)
    draw.line([x1, y1, x2, y2], fill=(0, 100, 255), width=1)

# Add warning symbols
if frame_num % 40 == 0:
    draw.text((random.randint(0, WIDTH), random.randint(0, HEIGHT)),
              "⚠️ SYSTEM BREACH", fill=(255, 0, 0), font=font)
    print("\n🌌 Compiling cyber-experience...")
    
    # Create video
    frames = sorted(glob.glob("frames/*.png"))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter("punkemv_future.mp4", fourcc, FPS, (WIDTH, HEIGHT))
    
    for frame in frames:
        img = cv2.imread(frame)
        video.write(img)
    video.release()
    
    # Convert to WebM if possible
    if os.path.exists("/usr/bin/ffmpeg"):
        os.system("ffmpeg -y -i punkemv_future.mp4 -c:v libvpx-vp9 -crf 25 -b:v 0 punkemv_future.webm")
        print("✅ Final output: punkemv_future.webm (4K HDR-ready)")
    else:
        print("✅ Final output: punkemv_future.mp4")

if __name__ == "__main__":
    main()
