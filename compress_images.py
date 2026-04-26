#!/usr/bin/env python3
"""
Image Compression Script for Sylva Lens Photography Portfolio
Optimizes JPEG, PNG, and other image formats while maintaining quality
Automatically creates WebP versions for modern browsers
"""

import os
import sys
from PIL import Image
from pathlib import Path
import json
from datetime import datetime

# Configuration
CATEGORIES = ['Weddings', 'Portraits', 'Sports',
              'Ceremonies', 'Pre weddings', 'Creative']
MAX_WIDTH = 1200
MAX_HEIGHT = 1200
JPEG_QUALITY = 40
PNG_QUALITY = 40
WEBP_QUALITY = 40

# Log file
LOG_FILE = 'compression_log.json'


def load_compression_log():
    """Load the compression log to track which files have been compressed"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_compression_log(log):
    """Save the compression log"""
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)


def get_file_hash(filepath):
    """Get a simple hash of file modification time and size"""
    stat = os.stat(filepath)
    return f"{stat.st_mtime}_{stat.st_size}"


def compress_image(input_path, output_path, format='JPEG', quality=85):
    """Compress a single image"""
    try:
        img = Image.open(input_path)

        # Convert RGBA to RGB if saving as JPEG
        if format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()
                          [-1] if img.mode == 'RGBA' else None)
            img = rgb_img

        # Resize if necessary
        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)

        # Save with compression
        if format.upper() == 'WEBP':
            img.save(output_path, format='WEBP', quality=quality, method=6)
        elif format.upper() == 'JPEG':
            img.save(output_path, format='JPEG',
                     quality=quality, optimize=True)
        elif format.upper() == 'PNG':
            img.save(output_path, format='PNG', optimize=True)
        else:
            img.save(output_path, format=format, quality=quality)

        return True
    except Exception as e:
        print(f"  ❌ Error compressing {input_path}: {str(e)}")
        return False


def process_images():
    """Process all images in portfolio categories"""
    log = load_compression_log()
    total_original_size = 0
    total_compressed_size = 0
    processed_count = 0
    skipped_count = 0

    print("🖼️  Starting image compression process...\n")

    for category in CATEGORIES:
        category_path = Path(category)

        if not category_path.exists():
            print(f"⏭️  Skipping {category} (directory not found)")
            continue

        print(f"📁 Processing {category}...")

        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
        image_files = [f for f in category_path.iterdir()
                       if f.is_file() and f.suffix.lower() in image_extensions]

        for image_file in image_files:
            file_key = str(image_file)
            current_hash = get_file_hash(str(image_file))

            # Check if already compressed
            if file_key in log and log[file_key] == current_hash:
                print(f"  ⏭️  {image_file.name} (already compressed)")
                skipped_count += 1
                continue

            # Get original file size
            original_size = os.path.getsize(str(image_file))
            total_original_size += original_size

            # Compress original to JPEG
            if image_file.suffix.lower() != '.jpg':
                jpg_path = image_file.with_suffix('.jpg')
            else:
                jpg_path = image_file

            # Only recompress if not the original JPG or if it needs updating
            if compress_image(str(image_file), str(jpg_path), format='JPEG', quality=JPEG_QUALITY):
                new_size = os.path.getsize(str(jpg_path))
                total_compressed_size += new_size
                reduction = ((original_size - new_size) /
                             original_size * 100) if original_size > 0 else 0
                print(
                    f"  ✓ {image_file.name}: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB ({reduction:.1f}% reduction)")
                processed_count += 1

                # Create WebP version
                webp_path = jpg_path.with_suffix('.webp')
                if compress_image(str(jpg_path), str(webp_path), format='WEBP', quality=WEBP_QUALITY):
                    webp_size = os.path.getsize(str(webp_path))
                    print(f"    → WebP: {webp_size/1024:.1f}KB")

                # Update log
                log[file_key] = current_hash

    save_compression_log(log)

    print("\n" + "="*60)
    print("📊 COMPRESSION SUMMARY")
    print("="*60)
    print(f"Files processed: {processed_count}")
    print(f"Files skipped: {skipped_count}")
    if total_original_size > 0:
        print(f"Total original size: {total_original_size/1024/1024:.2f}MB")
        print(
            f"Total compressed size: {total_compressed_size/1024/1024:.2f}MB")
        overall_reduction = (
            (total_original_size - total_compressed_size) / total_original_size * 100)
        print(f"Overall reduction: {overall_reduction:.1f}%")
    print("="*60)
    print("\n✅ Image compression complete!")
    print("💡 Tip: Images are automatically lazy-loaded on your website")
    print("   for faster page loads and better user experience.\n")


if __name__ == '__main__':
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("❌ Error: PIL (Pillow) is not installed.")
        print("   Install it with: pip install Pillow")
        sys.exit(1)

    process_images()
