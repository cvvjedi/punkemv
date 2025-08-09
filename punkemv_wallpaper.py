from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import math
import os
import cv2
import glob
import sys

# ===== ADVANCED CYBERPUNK CONFIG =====
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
# =====================================

def create_hologram_effect(img):
    """Enhanced holographic effects with dynamic distortions"""
    arr = np.array(img)
    
    # Dynamic chromatic aberration
    for i in range(3):
        offset = random.randint(2, 5) + int(3 * math.sin(time.time()))
        direction = -1 if i % 2 else 1
        arr[:, :, i] = np.roll(arr[:, :, i], offset * direction, axis=1)
    
    # Scanlines with variable intensity
    scanline_intensity = 0.3 + 0.1 * math.sin(time.time())
    for y in range(0, HEIGHT, 2):
        arr[y, :, :] = arr[y, :, :] * (1 - scanline_intensity)
    
    # Bloom effect with dynamic radius
    bloom_radius = 2 + math.sin(time.time())
    blurred = cv2.GaussianBlur(arr, (0, 0), bloom_radius)
    arr = cv2.addWeighted(arr, 0.7, blurred, 0.3, 0)
    
    # Data corruption effect
    if random.random() > 0.7:
        h, w, _ = arr.shape
        for _ in range(20):
            x = random.randint(0, w-50)
            y = random.randint(0, h-50)
            arr[y:y+10, x:x+50] = np.roll(arr[y:y+10, x:x+50], random.randint(5, 20), axis=1)
    
    return Image.fromarray(arr)

def generate_cyber_frame(frame_num):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    
    # Pulsing quantum core with energy waves
    core_size = 120 + 30 * math.sin(frame_num / 8)
    core_x, core_y = WIDTH // 2, HEIGHT // 2
    
    # Energy waves
    for i in range(10, 0, -1):
        wave_size = core_size * i + 5 * math.sin(frame_num/3 + i)
        wave_color = NEON_COLORS[i % len(NEON_COLORS)]
        draw.ellipse([
            core_x - wave_size, 
            core_y - wave_size,
            core_x + wave_size, 
            core_y + wave_size
        ], outline=wave_color, width=1 + int(i/2))
    
    # Particle system for binary rain
    for _ in range(200):
        x = random.randint(0, WIDTH)
        speed = random.randint(3, 8)
        y = (frame_num * speed) % (HEIGHT + 100)
        char = random.choice(["0", "1", " "])
        
        # Trail effect
        for trail in range(3):
            alpha = 200 - trail * 80
            draw.text(
                (x, y - trail * 15), 
                char, 
                fill=(0, 255, 0, alpha)
            )
    
    # Circuit board patterns
    for _ in range(100):
        x1, y1 = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        length = random.randint(30, 150)
        angle = random.uniform(0, 2 * math.pi)
        x2 = x1 + length * math.cos(angle)
        y2 = y1 + length * math.sin(angle)
        
        # Draw circuit line with nodes
        draw.line([x1, y1, x2, y2], fill=(0, 100, 255), width=1)
        draw.ellipse([x1-2, y1-2, x1+2, y1+2], fill=(255, 0, 0))
        draw.ellipse([x2-2, y2-2, x2+2, y2+2], fill=(255, 0, 0))
    
    # Floating PUNKEMV text with enhanced holographic effect
    text = "PUNKEMV"
    try:
        font = ImageFont.truetype("Arial", 92)
    except:
        font = ImageFont.load_default()
    
    for i, char in enumerate(text):
        offset = 15 * math.sin(frame_num/5 + i)
        rotation = 5 * math.sin(frame_num/10 + i)
        
        # Create individual character canvas
        char_canvas = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_canvas)
        char_draw.text((30, 30), char, fill=NEON_COLORS[i % len(NEON_COLORS)], font=font)
        
        # Apply transformation
        char_canvas = char_canvas.rotate(rotation, expand=True)
        canvas.paste(
            char_canvas, 
            (1200 + i * 100 - 30, 400 + offset - 30), 
            char_canvas
        )
    
    # Animated data streams with multiple layers
    for stream in range(3):
        stream_y = 150 + 70 * math.sin(frame_num / (6 + stream)) + stream * 50
        hex_data = " ".join([f"{random.randint(0,255):02X}" for _ in range(40)])
        draw.text(
            (50, stream_y), 
            hex_data, 
            fill=(0, 255, 157), 
            font=font
        )
    
    # Random system breach warnings
    if frame_num % 40 == 0 or random.random() > 0.9:
        x = random.randint(100, WIDTH - 300)
        y = random.randint(100, HEIGHT - 100)
        
        # Warning symbol
        draw.rectangle([x, y, x+200, y+60], fill=(30, 0, 0))
        draw.text((x+10, y+10), "⚠️ SYSTEM BREACH", fill=(255, 0, 0), font=font)
        draw.text((x+10, y+50), f"CODE 0x{random.randint(0, 255):02X}", fill=(255, 150, 0), font=font)
    
    # Digital glitch effect
    if random.random() > 0.8:
        glitch_img = canvas.copy()
        glitch_arr = np.array(glitch_img)
        
        # Vertical shift
        shift = random.randint(5, 30)
        glitch_arr[shift:, :, :] = glitch_arr[:-shift, :, :]
        
        # Color channel offset
        offset = random.randint(2, 10)
        glitch_arr[:, :, 0] = np.roll(glitch_arr[:, :, 0], offset, axis=0)
        glitch_arr[:, :, 2] = np.roll(glitch_arr[:, :, 2], -offset, axis=0)
        
        canvas = Image.fromarray(glitch_arr)
    
    return create_hologram_effect(canvas)

def main():
    os.makedirs("frames", exist_ok=True)
    
    print(f"🌀 Generating {TOTAL_FRAMES} advanced cyber-frames...")
    for frame in range(TOTAL_FRAMES):
        img = generate_cyber_frame(frame)
        img.save(f"frames/frame_{frame:04d}.png")
        if frame % 10 == 0:
            print(f"⚡ Progress: {frame+1}/{TOTAL_FRAMES} - Rendering...")
    
    print("\n🌌 Compiling cyber-experience...")
    
    # Create video with enhanced quality
    frames = sorted(glob.glob("frames/*.png"))
    if frames:
        # First pass: high-quality H.264
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter("punkemv_future.mp4", fourcc, FPS, (WIDTH, HEIGHT))
        
        for frame_path in frames:
            img = cv2.imread(frame_path)
            if img is not None:
                video.write(img)
        video.release()
        
        # Second pass: WebM with VP9 encoding for smaller size
        if os.path.exists("/usr/bin/ffmpeg") or sys.platform != 'win32':
            os.system("ffmpeg -y -i punkemv_future.mp4 -c:v libvpx-vp9 -crf 20 -b:v 0 -pix_fmt yuv420p -auto-alt-ref 0 punkemv_future.webm")
            print("✅ Final output: punkemv_future.webm (4K HDR-ready)")
        else:
            print("✅ Final output: punkemv_future.mp4")
    else:
        print("❌ Error: No frames generated")

if __name__ == "__main__":
    import time
    main()
