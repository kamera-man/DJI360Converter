#!/usr/bin/env python3
"""
DJI 360 Converter - Backend Processing Module
Handles advanced image processing for DJI 360 images to optimize them for Facebook posting

This module provides both command-line interface and programmatic access for converting
DJI 360° images to Facebook's optimal format for better social media engagement.
"""

import os
import sys
from PIL import Image, ImageEnhance, ImageFilter
import argparse
from pathlib import Path
import json
from typing import Dict, List, Union, Optional

class DJI360Processor:
    """
    Main processor class for DJI 360° image optimization.
    
    This class handles the conversion of DJI 360° images to Facebook's optimal format,
    including resizing, aspect ratio correction, and quality enhancement.
    """
    
    def __init__(self):
        self.facebook_optimal_width = 2048
        self.facebook_optimal_height = 1024
        self.quality = 90

    def process_image(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> Dict:
        """
        Process a single DJI 360 image for Facebook optimization
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path for output image (optional)
            
        Returns:
            dict: Processing results with metadata
        """
        try:
            # Validate input file exists and is readable
            input_path_obj = Path(input_path)
            if not input_path_obj.exists():
                raise FileNotFoundError(f"Input file does not exist: {input_path}")
            if not input_path_obj.is_file():
                raise ValueError(f"Input path is not a file: {input_path}")
                
            # Open and validate image
            with Image.open(input_path) as img:
                original_size = img.size
                original_file_size = os.path.getsize(input_path)
                
                # Validate image dimensions
                if original_size[0] < 100 or original_size[1] < 100:
                    raise ValueError(f"Image too small: {original_size}. Minimum size is 100x100 pixels.")
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate optimal dimensions
                optimal_size = self._calculate_optimal_size(img.size)
                
                # Resize image
                processed_img = img.resize(optimal_size, Image.Resampling.LANCZOS)
                
                # Apply Facebook optimization filters
                processed_img = self._apply_facebook_optimization(processed_img)
                
                # Generate output path if not provided
                if output_path is None:
                    output_path = input_path_obj.parent / f"{input_path_obj.stem}_facebook_optimized.jpg"
                
                # Ensure output directory exists
                output_path_obj = Path(output_path)
                output_path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                # Save processed image
                processed_img.save(output_path, 'JPEG', quality=self.quality, optimize=True)
                
                # Get processed file size
                processed_file_size = os.path.getsize(output_path)
                
                return {
                    'success': True,
                    'input_path': str(input_path),
                    'output_path': str(output_path),
                    'original_dimensions': original_size,
                    'processed_dimensions': optimal_size,
                    'original_size_bytes': original_file_size,
                    'processed_size_bytes': processed_file_size,
                    'compression_ratio': round(processed_file_size / original_file_size, 3),
                    'size_reduction': round((1 - processed_file_size / original_file_size) * 100, 1)
                }
                
        except (FileNotFoundError, ValueError) as e:
            return {
                'success': False,
                'error': str(e),
                'input_path': str(input_path)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'input_path': str(input_path)
            }

    def _calculate_optimal_size(self, original_size: tuple) -> tuple:
        """
        Calculate optimal dimensions for Facebook posting.
        
        Facebook prefers 2:1 aspect ratio for 360° images for optimal display.
        This method calculates the best dimensions while maintaining image quality.
        
        Args:
            original_size (tuple): Original image dimensions (width, height)
            
        Returns:
            tuple: Optimal dimensions (width, height) for Facebook
        """
        orig_width, orig_height = original_size
        target_ratio = 2.0  # 2:1 aspect ratio ideal for 360 images
        
        # If image is already close to target ratio, just resize to max dimensions
        current_ratio = orig_width / orig_height
        
        if abs(current_ratio - target_ratio) < 0.1:  # Close enough to target ratio
            if orig_width > self.facebook_optimal_width or orig_height > self.facebook_optimal_height:
                # Scale down maintaining aspect ratio
                scale_factor = min(
                    self.facebook_optimal_width / orig_width,
                    self.facebook_optimal_height / orig_height
                )
                return (int(orig_width * scale_factor), int(orig_height * scale_factor))
            else:
                return original_size
        
        # Calculate new dimensions based on target ratio
        if current_ratio > target_ratio:
            # Image is wider than target ratio - use height to determine size
            new_height = min(orig_height, self.facebook_optimal_height)
            new_width = min(int(new_height * target_ratio), self.facebook_optimal_width)
        else:
            # Image is taller than target ratio - use width to determine size
            new_width = min(orig_width, self.facebook_optimal_width)
            new_height = min(int(new_width / target_ratio), self.facebook_optimal_height)
        
        return (new_width, new_height)

    def _apply_facebook_optimization(self, img: Image.Image) -> Image.Image:
        """
        Apply Facebook-specific optimizations to enhance social media appearance.
        
        This applies subtle enhancements that improve how images appear on mobile devices
        and in social media feeds, including sharpening and contrast adjustments.
        
        Args:
            img (PIL.Image.Image): Input image to optimize
            
        Returns:
            PIL.Image.Image: Optimized image
        """
        # Slight sharpening for better appearance on mobile devices
        sharpened = img.filter(ImageFilter.UnsharpMask(radius=1, percent=110, threshold=3))
        
        # Enhance contrast slightly for better visibility
        enhancer = ImageEnhance.Contrast(sharpened)
        contrasted = enhancer.enhance(1.05)
        
        # Slight color enhancement
        color_enhancer = ImageEnhance.Color(contrasted)
        enhanced = color_enhancer.enhance(1.02)
        
        return enhanced

    def process_batch(self, input_directory: Union[str, Path], output_directory: Optional[Union[str, Path]] = None) -> List[Dict]:
        """
        Process multiple images in a directory
        """
        input_path = Path(input_directory)
        if not input_path.exists():
            raise ValueError(f"Input directory does not exist: {input_directory}")
        
        if output_directory:
            output_path = Path(output_directory)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = input_path / "facebook_optimized"
            output_path.mkdir(exist_ok=True)
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}
        image_files = [f for f in input_path.iterdir() 
                      if f.suffix.lower() in image_extensions and f.is_file()]
        
        results = []
        for img_file in image_files:
            output_file = output_path / f"{img_file.stem}_facebook_optimized.jpg"
            result = self.process_image(img_file, output_file)
            results.append(result)
            
            if result['success']:
                print(f"✓ Processed: {img_file.name} -> {output_file.name}")
            else:
                print(f"✗ Failed: {img_file.name} - {result['error']}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='DJI 360 Image Converter for Facebook')
    parser.add_argument('input', help='Input image file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-b', '--batch', action='store_true', 
                       help='Process all images in input directory')
    parser.add_argument('-j', '--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('-q', '--quality', type=int, default=90,
                       help='JPEG quality (1-100, default: 90)')
    
    args = parser.parse_args()
    
    processor = DJI360Processor()
    processor.quality = args.quality
    
    try:
        if args.batch:
            results = processor.process_batch(args.input, args.output)
            
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                successful = sum(1 for r in results if r['success'])
                failed = len(results) - successful
                print(f"\nProcessing complete: {successful} successful, {failed} failed")
                
                if successful > 0:
                    total_original = sum(r['original_size_bytes'] for r in results if r['success'])
                    total_processed = sum(r['processed_size_bytes'] for r in results if r['success'])
                    overall_reduction = (1 - total_processed / total_original) * 100
                    print(f"Overall size reduction: {overall_reduction:.1f}%")
        else:
            result = processor.process_image(args.input, args.output)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if result['success']:
                    print(f"✓ Successfully processed: {args.input}")
                    print(f"  Original: {result['original_dimensions']} ({result['original_size_bytes']} bytes)")
                    print(f"  Processed: {result['processed_dimensions']} ({result['processed_size_bytes']} bytes)")
                    print(f"  Size reduction: {result['size_reduction']}%")
                    print(f"  Output: {result['output_path']}")
                else:
                    print(f"✗ Failed to process: {args.input}")
                    print(f"  Error: {result['error']}")
                    sys.exit(1)
                    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()