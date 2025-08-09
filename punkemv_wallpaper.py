from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import glitchart
import random

# Canvas setup
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (10, 10, 18)  # #0a0a12

# Create base image
canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(canvas)

# Add concrete texture (replace with your own texture path or generate noise)
try:
    texture = Image.open("concrete.jpg").convert("RGBA").resize((WIDTH, HEIGHT))
    texture = texture.point(lambda p: p * 0.3)  # Reduce opacity
    canvas.paste(texture, (0, 0), texture)
except:
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
font = ImageFont.truetype("arial.ttf", 20)
track_color = (0, 255, 157)  # Neon green
for i, track in enumerate([track1, track2]):
    y_pos = stripe_top + 50 + (i * 30)
    draw.text((50, y_pos), track, font=font, fill=track_color)

# Glitch effect
img_array = np.array(canvas)
glitched_array = glitchart.jpeg(img_array, quality=20, chop=random.uniform(0.5, 0.8))
canvas = Image.fromarray(glitched_array)

# Add punk text
try:
    punk_font = ImageFont.truetype("impact.ttf", 92)
except:
    punk_font = ImageFont.load_default()
draw.text((1400, 540), "PUNKEMV", font=punk_font, fill=(255, 7, 58))

# Save final image
canvas.save("punkemv_wallpaper.png")
print("Wallpaper generated: punkemv_wallpaper.png")
