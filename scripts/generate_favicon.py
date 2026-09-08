#!/usr/bin/env python3
"""
Generate high-contrast circular portrait favicons from Marian's photo.
Produces all standard favicon sizes + apple-touch-icon.
"""

import os
from PIL import Image, ImageDraw, ImageOps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_IMAGE = os.path.join(BASE_DIR, 'profile-big.webp')
if not os.path.exists(SRC_IMAGE):
    SRC_IMAGE = os.path.join(BASE_DIR, 'profile.webp')

def make_circular_portrait():
    print(f"Loading source image from {SRC_IMAGE}...")
    img = Image.open(SRC_IMAGE).convert("RGBA")
    
    # Square crop to center
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Target high-res canvas (512x512)
    size = 512
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Create output circular image
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)
    
    # Add high-contrast bronze ring border
    draw_out = ImageDraw.Draw(output)
    border_width = 12
    draw_out.ellipse(
        (border_width // 2, border_width // 2, size - border_width // 2, size - border_width // 2),
        outline=(205, 127, 50, 255),
        width=border_width
    )
    
    sizes = [16, 32, 48, 64, 96, 128, 180, 192, 512]
    ico_images = []
    
    for s in sizes:
        resized = output.resize((s, s), Image.Resampling.LANCZOS)
        out_name = f"favicon-{s}x{s}.png"
        out_path = os.path.join(BASE_DIR, out_name)
        resized.save(out_path, format="PNG")
        print(f"Saved {out_name}")
        
        if s in [16, 32, 48]:
            ico_images.append(resized)
            
    # Save standard favicon.png
    fav_png = output.resize((32, 32), Image.Resampling.LANCZOS)
    fav_png.save(os.path.join(BASE_DIR, 'favicon.png'), format="PNG")
    
    # Save apple-touch-icon.png
    apple_icon = output.resize((180, 180), Image.Resampling.LANCZOS)
    apple_icon.save(os.path.join(BASE_DIR, 'apple-touch-icon.png'), format="PNG")
    
    # Save favicon.ico with multi-resolutions
    ico_path = os.path.join(BASE_DIR, 'favicon.ico')
    ico_images[0].save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico_images[1:])
    print("Saved favicon.ico with multi-resolution portrait!")

if __name__ == '__main__':
    make_circular_portrait()
