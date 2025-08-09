from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
try:
    import glitchart  # type: ignore
except Exception:
    glitchart = None
import random
import argparse
import os

# Canvas setup
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (10, 10, 18)  # #0a0a12

# Parse simple CLI options
parser = argparse.ArgumentParser(description="Generate PUNKEMV wallpaper as video or image")
parser.add_argument("--format", choices=["mp4", "webm", "png"], default="mp4", help="Output format")
parser.add_argument("--fps", type=int, default=24, help="Frames per second for video")
parser.add_argument("--seconds", type=float, default=3.0, help="Duration for video in seconds")
parser.add_argument("--output", type=str, default=None, help="Output filename; if omitted, inferred from format")
args = parser.parse_args()

# Create base image
canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(canvas)

# Add concrete texture (replace with your own texture path or generate noise)
try:
    texture = Image.open("concrete.jpg").convert("RGBA").resize((WIDTH, HEIGHT))
    texture = texture.point(lambda p: p * 0.3)  # Reduce opacity
    canvas.paste(texture, (0, 0), texture)
except Exception:
    print("No texture found - proceeding without")

# Generate magnetic stripe
def generate_track_data():
    # Realistic Track 1/Track 2 data structure
    track1 = "%B4485" + "".join(random.choice("0123456789") for _ in range(11)) + f"^PUNKEMV/DMP^{random.randint(23,27)}{random.randint(1,12):02d}1******?;"
    track2 = ";" + "".join(random.choice("0123456789") for _ in range(16)) + f"={random.randint(23,27)}{random.randint(1,12):02d}1******?"
    return track1, track2

track1, track2 = generate_track_data()

# Draw stripe
stripe_top, stripe_bottom = 300, 800
draw.rectangle([(0, stripe_top), (WIDTH, stripe_bottom)], fill=(0, 0, 0))

# Add track data
try:
    font = ImageFont.truetype("arial.ttf", 20)
except Exception:
    try:
        # Try common DejaVu fallback if available on many systems
        font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
track_color = (0, 255, 157)  # Neon green
for i, track in enumerate([track1, track2]):
    y_pos = stripe_top + 50 + (i * 30)
    draw.text((50, y_pos), track, font=font, fill=track_color)

# Add punk text
try:
    punk_font = ImageFont.truetype("impact.ttf", 92)
except Exception:
    try:
        punk_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 92)
    except Exception:
        punk_font = ImageFont.load_default()

draw.text((1400, 540), "PUNKEMV", font=punk_font, fill=(255, 7, 58))

# Glitch effect helper

def apply_glitch(image_array: np.ndarray) -> np.ndarray:
    if glitchart is not None:
        try:
            return glitchart.jpeg(image_array, quality=20, chop=random.uniform(0.5, 0.8))
        except Exception:
            pass
    # Fallback: jpeg re-encode to introduce compression artifacts
    from io import BytesIO
    buffer = BytesIO()
    Image.fromarray(image_array).save(buffer, format="JPEG", quality=10)
    buffer.seek(0)
    return np.array(Image.open(buffer).convert("RGB"))

# Determine output
if args.output:
    output_path = args.output
else:
    output_ext = args.format
    output_path = f"punkemv_wallpaper.{output_ext}"

# Render frames and save
if args.format == "png":
    # Single frame image
    img_array = np.array(canvas)
    glitched_array = apply_glitch(img_array)
    Image.fromarray(glitched_array).save(output_path)
    print(f"Image generated: {output_path}")
else:
    # Animated video
    import imageio

    fps = max(1, args.fps)
    total_frames = max(1, int(round(args.seconds * fps)))

    # Choose codec and extra options per container
    if args.format == "mp4":
        codec = "libx264"
        pixfmt = "yuv420p"
    else:  # webm
        codec = "libvpx-vp9"
        pixfmt = None  # default

    writer_kwargs = {"fps": fps, "codec": codec}
    # Help with odd sizes for some codecs
    writer_kwargs["macro_block_size"] = None
    if pixfmt is not None:
        writer_kwargs["pixelformat"] = pixfmt

    with imageio.get_writer(output_path, **writer_kwargs) as writer:
        base_array = np.array(canvas)
        for _ in range(total_frames):
            frame = apply_glitch(base_array)
            writer.append_data(frame)

    print(f"Video generated: {output_path}")
