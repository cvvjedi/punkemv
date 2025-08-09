import numpy as np
import pygame
import math
import random
import os
import subprocess
from pygame import gfxdraw
from PIL import Image, ImageDraw, ImageFont

# ===== ADVANCED CYBERPUNK CONFIG =====
WIDTH, HEIGHT = 1920, 1080
FPS = 60
DURATION_SEC = 5
TOTAL_FRAMES = FPS * DURATION_SEC
OUTPUT_DIR = "frames"
# =====================================

# Initialize pygame with OpenGL acceleration
pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("PUNKEMV Cyberpunk Generator")

# Color palette with energy colors
NEON_PALETTE = [
    (0, 255, 157),   # Matrix green
    (255, 20, 147),  # Cyber pink
    (0, 191, 255),   # Electric blue
    (138, 43, 226),  # Purple haze
    (255, 215, 0),   # Cyber gold
    (0, 255, 255),   # Cyan
]

# Advanced particle system
class CyberParticle:
    def __init__(self, x, y, particle_type):
        self.x = x
        self.y = y
        self.type = particle_type
        self.size = random.uniform(1.0, 4.0)
        self.color = random.choice(NEON_PALETTE)
        self.life = random.uniform(30, 150)
        self.velocity = [random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)]
        self.trail = []
        self.max_trail = 5
        self.osc_speed = random.uniform(0.01, 0.05)
        
        if particle_type == "binary":
            self.char = random.choice(["0", "1"])
            self.size = random.uniform(8, 14)
            self.velocity = [0, random.uniform(2, 6)]
        elif particle_type == "energy":
            self.size = random.uniform(2, 8)
            self.velocity = [
                random.uniform(-2, 2), 
                random.uniform(-2, 2)
            ]
        elif particle_type == "circuit":
            self.size = random.uniform(1, 3)
            self.target = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            self.velocity = [
                (self.target[0] - self.x) / 60,
                (self.target[1] - self.y) / 60
            ]
    
    def update(self):
        self.life -= 1
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
        # Particle-specific behaviors
        if self.type == "energy":
            self.velocity[0] += random.uniform(-0.1, 0.1)
            self.velocity[1] += random.uniform(-0.1, 0.1)
            self.size = max(1, self.size + random.uniform(-0.2, 0.2))
        elif self.type == "binary" and self.y > HEIGHT:
            self.y = -20
            self.x = random.randint(0, WIDTH)
        elif self.type == "circuit" and math.dist((self.x, self.y), self.target) < 10:
            self.target = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            self.velocity = [
                (self.target[0] - self.x) / 60,
                (self.target[1] - self.y) / 60
            ]
        
        return self.life > 0

# Main generator class
class CyberpunkGenerator:
    def __init__(self):
        self.particles = []
        self.core_size = 100
        self.core_pulse = 0
        self.data_streams = []
        self.warnings = []
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 92, bold=True)
        
        # Initialize data streams
        for _ in range(3):
            self.data_streams.append({
                'y': random.randint(100, HEIGHT - 100),
                'speed': random.uniform(0.5, 2.0),
                'data': " ".join([f"{random.randint(0,255):02X}" for _ in range(25)])
            })
    
    def add_particles(self, count, particle_type, x=None, y=None):
        for _ in range(count):
            px = x if x is not None else random.randint(0, WIDTH)
            py = y if y is not None else random.randint(0, HEIGHT)
            self.particles.append(CyberParticle(px, py, particle_type))
    
    def update(self, frame_num):
        # Update core pulse
        self.core_pulse = 100 + 30 * math.sin(frame_num / 10)
        
        # Add new particles periodically
        if frame_num % 2 == 0:
            self.add_particles(10, "binary")
        if frame_num % 5 == 0:
            self.add_particles(3, "energy", WIDTH//2, HEIGHT//2)
        if frame_num % 20 == 0:
            self.add_particles(15, "circuit")
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Update data streams
        for stream in self.data_streams:
            stream['y'] = 200 + 50 * math.sin(frame_num / (6 + random.random()))
            if frame_num % 60 == 0:
                stream['data'] = " ".join([f"{random.randint(0,255):02X}" for _ in range(25)])
        
        # Add random warnings
        if random.random() < 0.02 or (frame_num % 100 == 0):
            self.warnings.append({
                'x': random.randint(100, WIDTH - 300),
                'y': random.randint(100, HEIGHT - 100),
                'life': 90
            })
        
        # Update warnings
        for warning in self.warnings:
            warning['life'] -= 1
        self.warnings = [w for w in self.warnings if w['life'] > 0]
    
    def render(self, surface):
        # Draw dark background with subtle grid
        surface.fill((5, 5, 15))
        
        # Draw subtle grid
        for x in range(0, WIDTH, 40):
            alpha = min(255, abs(x - WIDTH//2) // 2)
            pygame.draw.line(surface, (20, 20, 30), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 40):
            alpha = min(255, abs(y - HEIGHT//2) // 2)
            pygame.draw.line(surface, (20, 20, 30), (0, y), (WIDTH, y), 1)
        
        # Draw energy core
        core_x, core_y = WIDTH // 2, HEIGHT // 2
        for i in range(10, 0, -1):
            size = self.core_pulse * i / 10
            color = NEON_PALETTE[i % len(NEON_PALETTE)]
            pygame.draw.circle(
                surface, 
                color, 
                (core_x, core_y), 
                size, 
                max(1, int(i/2))
        
        # Draw particles with trails
        for particle in self.particles:
            # Draw trail
            for i, (trail_x, trail_y) in enumerate(particle.trail):
                alpha = int(200 * i / len(particle.trail))
                size = particle.size * i / len(particle.trail)
                
                if particle.type == "binary":
                    text = self.font.render(particle.char, True, (*particle.color, alpha))
                    surface.blit(text, (trail_x, trail_y))
                else:
                    pygame.draw.circle(
                        surface, 
                        (*particle.color, alpha), 
                        (int(trail_x), int(trail_y)), 
                        size
                    )
            
            # Draw main particle
            if particle.type == "binary":
                text = self.font.render(particle.char, True, particle.color)
                surface.blit(text, (particle.x, particle.y))
            else:
                pygame.draw.circle(
                    surface, 
                    particle.color, 
                    (int(particle.x), int(particle.y)), 
                    particle.size
                )
        
        # Draw data streams
        for stream in self.data_streams:
            text = self.font.render(stream['data'], True, NEON_PALETTE[0])
            surface.blit(text, (50, stream['y']))
        
        # Draw system warnings
        for warning in self.warnings:
            # Warning background
            pygame.draw.rect(surface, (30, 0, 0), 
                            (warning['x'], warning['y'], 300, 60))
            pygame.draw.rect(surface, (200, 0, 0), 
                            (warning['x'], warning['y'], 300, 60), 2)
            
            # Warning text
            title = self.font.render("⚠️ SYSTEM BREACH", True, (255, 100, 100))
            code = self.font.render(f"SECURITY VIOLATION 0x{random.randint(0, 255):02X}", 
                                   True, (255, 200, 100))
            surface.blit(title, (warning['x'] + 10, warning['y'] + 5))
            surface.blit(code, (warning['x'] + 10, warning['y'] + 35))
        
        # Draw PUNKEMV title with glow effect
        title = "PUNKEMV"
        for i in range(5):
            offset = 5 - i
            color = NEON_PALETTE[i % len(NEON_PALETTE)]
            text = self.title_font.render(title, True, color)
            surface.blit(text, (WIDTH - 700 + offset, 100 + offset))
        
        # Draw frame counter
        counter = self.font.render(f"FRAME: {frame_num:04d}/300", True, (150, 150, 150))
        surface.blit(counter, (20, HEIGHT - 40))
        
        # Add scanlines effect
        self.apply_scanlines(surface)
        
        # Apply chromatic aberration
        return self.apply_chromatic_aberration(surface)
    
    def apply_scanlines(self, surface):
        """Apply scanline effect to the surface"""
        for y in range(0, HEIGHT, 3):
            pygame.draw.line(surface, (0, 0, 0, 50), (0, y), (WIDTH, y), 1)
    
    def apply_chromatic_aberration(self, surface):
        """Apply chromatic aberration effect"""
        # Convert surface to array
        pixels = pygame.surfarray.array3d(surface)
        
        # Create RGB channels with offsets
        r_channel = np.roll(pixels[:, :, 0], shift=-2, axis=1)
        g_channel = pixels[:, :, 1]
        b_channel = np.roll(pixels[:, :, 2], shift=2, axis=1)
        
        # Combine channels
        aberrated = np.stack([r_channel, g_channel, b_channel], axis=2)
        
        # Convert back to surface
        return pygame.surfarray.make_surface(aberrated)

# Main rendering function
def generate_frames():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create generator
    generator = CyberpunkGenerator()
    
    # Add initial particles
    generator.add_particles(200, "binary")
    generator.add_particles(50, "energy", WIDTH//2, HEIGHT//2)
    generator.add_particles(100, "circuit")
    
    # Generate frames
    print(f"🌀 Generating {TOTAL_FRAMES} cyber-frames...")
    for frame in range(TOTAL_FRAMES):
        # Update generator state
        generator.update(frame)
        
        # Render frame
        frame_surface = generator.render(screen)
        
        # Save frame
        pygame.image.save(frame_surface, f"{OUTPUT_DIR}/frame_{frame:04d}.png")
        
        # Print progress
        if frame % 10 == 0:
            print(f"⚡ Progress: {frame+1}/{TOTAL_FRAMES}")
    
    print("\n🌌 Compiling cyber-experience...")
    compile_video()

def compile_video():
    """Compile frames into a video using ffmpeg"""
    # First pass: MP4 with H.264
    mp4_cmd = [
        'ffmpeg', '-y', '-framerate', str(FPS),
        '-i', f'{OUTPUT_DIR}/frame_%04d.png',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-preset', 'slow', '-crf', '18',
        'punkemv_cyber.mp4'
    ]
    
    # Second pass: WebM with VP9
    webm_cmd = [
        'ffmpeg', '-y', '-i', 'punkemv_cyber.mp4',
        '-c:v', 'libvpx-vp9', '-b:v', '0',
        '-crf', '20', '-pix_fmt', 'yuv420p',
        '-auto-alt-ref', '0', 'punkemv_cyber.webm'
    ]
    
    try:
        # Run MP4 conversion
        print("Creating MP4 version...")
        subprocess.run(mp4_cmd, check=True)
        
        # Run WebM conversion
        print("Creating WebM version...")
        subprocess.run(webm_cmd, check=True)
        
        print("✅ Final outputs: punkemv_cyber.mp4 and punkemv_cyber.webm")
    except Exception as e:
        print(f"❌ Video compilation failed: {str(e)}")
        print("Frames are saved in the 'frames' directory")

if __name__ == "__main__":
    generate_frames()
