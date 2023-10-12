from PIL import Image
import argparse
import os
import random
import time
import sys

# Simple script to crop and resize all images in a folder to an SDXL training value
# Usage: python resize_bulk.py /path/to/dir [--height pixels] [--width pixels] [--random] [--png] [--shortside pixels] [--longside pixels]

# By default, selects the resolution closest to the original image aspect ration
# --random to randomize the aspect ratio
# --png to save as png, slower and uses more space
# --height and --width specify the pixels respectively
# if only one --height or --width is used, the image will be scaled to its original aspect ratio
# --short-side specifies the pixels for the shortest side, ensuring a minimum width/height
# --long-side specifies the pixels for the longest side, ensuring a maximum width/height

# Record the start time
start_time = time.time()

# Define target resolutions
target_resolutions = [
    {"name": "1408x704", "width": 1408, "height": 704},
    {"name": "1344x768", "width": 1344, "height": 768},
    {"name": "1280x768", "width": 1280, "height": 768},
    {"name": "1216x832", "width": 1216, "height": 832},
    {"name": "1152x832", "width": 1152, "height": 832},
    {"name": "1152x896", "width": 1152, "height": 896},
    {"name": "1088x896", "width": 1088, "height": 896},
    {"name": "1088x960", "width": 1088, "height": 960},
    {"name": "1024x960", "width": 1024, "height": 960},
    {"name": "1024x1024", "width": 1024, "height": 1024},
    {"name": "960x1024", "width": 960, "height": 1024},
    {"name": "960x1088", "width": 960, "height": 1088},
    {"name": "896x1088", "width": 896, "height": 1088},
    {"name": "896x1152", "width": 896, "height": 1152},
    {"name": "832x1152", "width": 832, "height": 1152},
    {"name": "832x1216", "width": 832, "height": 1216},
    {"name": "768x1280", "width": 768, "height": 1280},
    {"name": "768x1344", "width": 768, "height": 1344},
    {"name": "704x1344", "width": 704, "height": 1344},
    {"name": "704x1408", "width": 704, "height": 1408},
# SDXL training resolutions with aspect ratios >2:1 and <1:2 have been excluded from this list
]

def closest_aspect_ratio(width, height):
    aspect_ratio = width / height
    closest_ratio = min(target_resolutions, key=lambda x: abs(x['width']/x['height'] - aspect_ratio))
    return closest_ratio

def random_target_resolution():
    return random.choice(target_resolutions)

def process_image(image_path, height=None, width=None, short_side=None, long_side=None, random_mode=False, png_mode=False):
    img = Image.open(image_path)
    original_width, original_height = img.size
    source_aspect_ratio = original_width / original_height

    if source_aspect_ratio.is_integer():
        source_aspect_ratio = int(source_aspect_ratio)
    else:
        source_aspect_ratio = round(source_aspect_ratio, 2)

    if long_side is not None:
        # Resize the longest side to the specified pixel count
        if original_width >= original_height:
            new_width = long_side
            new_height = int(long_side / source_aspect_ratio)
        else:
            new_height = long_side
            new_width = int(long_side * source_aspect_ratio)
    elif short_side is not None:
        # Resize the shortest side to the specified pixel count
        if original_width <= original_height:
            new_width = short_side
            new_height = int(short_side / source_aspect_ratio)
        else:
            new_height = short_side
            new_width = int(short_side * source_aspect_ratio)
    else:
        if height is not None and width is not None:
            # If both height and width are specified, crop and resize to the given dimensions
            new_width = width
            new_height = height
        elif height is not None:
            # If only height is specified, resize the image to the specified height
            new_height = height
            new_width = int(new_height * source_aspect_ratio)
        elif width is not None:
            # If only width is specified, resize the image to the specified width
            new_width = width
            new_height = int(new_width / source_aspect_ratio)
        else:
            # If neither height nor width is specified, use the closest aspect ratio resolution
            if random_mode:
                target = random_target_resolution()  # Pick a random target resolution
            else:
                target = closest_aspect_ratio(original_width, original_height)  # Find the nearest target resolution

            new_width = target['width']
            new_height = target['height']

    print(f"{os.path.basename(image_path)} resized to {new_width}x{new_height}.")

    # Crop to target aspect ratio
    target_aspect_ratio = new_width / new_height
    if source_aspect_ratio > target_aspect_ratio:
        crop_width = int(original_height * target_aspect_ratio)
        crop_height = original_height
    else:
        crop_width = original_width
        crop_height = int(original_width / target_aspect_ratio)

    left_margin = (original_width - crop_width) / 2
    top_margin = (original_height - crop_height) / 2

    img = img.crop((left_margin, top_margin, left_margin + crop_width, top_margin + crop_height))

    # Resize to target dimensions
    img = img.resize((new_width, new_height), Image.LANCZOS)

    if png_mode:
        # Convert the image to RGBA mode for lossless PNG
        img = img.convert('RGBA')
        extension = 'png'
    else:
        # Convert the image to RGB mode for JPEG
        img = img.convert('RGB')
        extension = 'jpg'

    # Create subfolder if it doesn't exist
    output_directory = os.path.join(args.directory_path, 'resized')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Save the processed image in the specified format
    output_path = os.path.join(output_directory, f"{os.path.basename(image_path).split('.')[0]}.{extension}")
    if extension.lower() == 'jpg':
        img.save(output_path, 'JPEG')
    else:
        img.save(output_path, extension.upper())

def main(directory_path, random_mode=False, png_mode=False, height=None, width=None, short_side=None, long_side=None):
    files_resized = 0  # Initialize the counter for resized files
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            full_path = os.path.join(directory_path, filename)
            process_image(full_path, height, width, short_side, long_side, random_mode, png_mode)
            files_resized += 1  # Increment the counter for each resized file
    
    # Define the output directory path
    output_directory = os.path.join(args.directory_path, 'resized')
    
    return files_resized, output_directory  # Return the total count of resized files and the output directory path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resize images in a directory.')
    parser.add_argument('directory_path', type=str, help='Path to the directory containing images')
    parser.add_argument('--height', type=int, help='Specify the height for resizing the images')
    parser.add_argument('--width', type=int, help='Specify the width for resizing the images')
    parser.add_argument('--short-side', type=int, help='Specify the pixel count for resizing the shortest side')
    parser.add_argument('--long-side', type=int, help='Specify the pixel count for resizing the longest side')
    parser.add_argument('--random', action='store_true', help='Resize images to a random aspect ratio')
    parser.add_argument('--png', action='store_true', help='Save images in lossless RGBA PNG format')
    
    args = parser.parse_args()

    # Record the start time
    start_time = time.time()

    # Call the main function with the input directory and optional flags
    files_resized, output_directory = main(args.directory_path, args.random, args.png, args.height, args.width, args.short_side, args.long_side)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time in seconds
    elapsed_time = end_time - start_time

    # Calculate hours, minutes, and seconds
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    # Construct the elapsed time string
    elapsed_time_str = f"{hours}h " if hours > 0 else ""
    elapsed_time_str += f"{minutes}m " if minutes > 0 else ""
    elapsed_time_str += f"{seconds}s"

    # Print the number of files resized, the elapsed time, and the output directory
    print(f"{files_resized} images resized in {elapsed_time_str}.")
    print(f"Output folder: {output_directory}")