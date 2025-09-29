#!/usr/bin/env python3
"""
Demo script to create a sample 360° image for testing DJI360Converter
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_360_image():
    """Create a sample panoramic image for testing"""
    
    # Create a wide panoramic image (3600x1800 - typical 360° dimensions)
    width, height = 3600, 1800
    img = Image.new('RGB', (width, height), color='skyblue')
    draw = ImageDraw.Draw(img)
    
    # Create a gradient sky
    for y in range(height // 2):
        color_value = int(135 + (120 * y / (height // 2)))  # Sky blue to light blue gradient
        color = (color_value, color_value + 20, 255)
        draw.rectangle([(0, y), (width, y + 1)], fill=color)
    
    # Create ground
    for y in range(height // 2, height):
        color_value = int(100 - (50 * (y - height // 2) / (height // 2)))  # Green gradient
        color = (color_value, color_value + 50, color_value)
        draw.rectangle([(0, y), (width, y + 1)], fill=color)
    
    # Add some simple landscape elements
    # Sun
    sun_x, sun_y = width // 4, height // 4
    draw.ellipse([sun_x - 80, sun_y - 80, sun_x + 80, sun_y + 80], fill='yellow')
    
    # Mountains (simple triangles)
    mountain_points = [
        (0, height // 2),
        (width // 6, height // 3),
        (width // 3, height // 2)
    ]
    draw.polygon(mountain_points, fill='darkgray')
    
    mountain_points2 = [
        (width // 3, height // 2),
        (width // 2, height // 4),
        (2 * width // 3, height // 2)
    ]
    draw.polygon(mountain_points2, fill='gray')
    
    # Trees (simple rectangles and circles)
    for i in range(20):
        tree_x = width // 8 + (i * width // 25)
        tree_y = height // 2 + 50
        # Trunk
        draw.rectangle([tree_x - 10, tree_y, tree_x + 10, tree_y + 100], fill='brown')
        # Leaves
        draw.ellipse([tree_x - 30, tree_y - 40, tree_x + 30, tree_y + 20], fill='darkgreen')
    
    # Add text overlay
    try:
        font = ImageFont.load_default()
        text = "Sample DJI 360° Image - Ready for Facebook Conversion"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, height - 100), text, fill='white', font=font)
    except:
        # Fallback if font loading fails
        draw.text((width // 2 - 200, height - 100), 
                 "Sample 360° Image for Testing", fill='white')
    
    return img

def main():
    print("Creating sample DJI 360° image for testing...")
    
    # Create the sample image
    sample_image = create_sample_360_image()
    
    # Save it
    output_path = "sample_dji_360_image.jpg"
    sample_image.save(output_path, 'JPEG', quality=95)
    
    file_size = os.path.getsize(output_path)
    print(f"✓ Created sample image: {output_path}")
    print(f"  Size: {sample_image.size[0]}x{sample_image.size[1]}")
    print(f"  File size: {file_size / 1024:.1f} KB")
    print("\nYou can now test the converter with this sample image:")
    print(f"  python3 dji360_converter.py {output_path}")
    print("  or upload it to the web interface at http://localhost:8000")

if __name__ == '__main__':
    main()