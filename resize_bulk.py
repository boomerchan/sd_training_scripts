from PIL import Image
import argparse
import os
import random
import time
import sys

# Simple script to crop and resize all images in a folder to an SDXL training value
# Usage: python resize_bulk.py /path/to/dir

# By default, selects the resolution closest to the original image aspect ratio
# --random to randomize the aspect ratio
# --png to save as png, slower and uses more space
# Example: python resize_bulk.py /path/to/dir --random --png

# Record the start time
start_time = time.time()

# Define target resolutions
target_resolutions = [
    {"name": "1024x1024 (1:1)", "width": 1024, "height": 1024},
    {"name": "1152x896 (1.28:1)", "width": 1152, "height": 896},
    {"name": "896x1152 (0.78:1)", "width": 896, "height": 1152},
    {"name": "1216x832 (1.46:1)", "width": 1216, "height": 832},
    {"name": "832x1216 (0.68:1)", "width": 832, "height": 1216},
    {"name": "1344x768 (1.75:1)", "width": 1344, "height": 768},
    {"name": "768x1344 (0.57:1)", "width": 768, "height": 1344},
# I hashed these resolutions because they tend to break most images
# Simply remove the hashes if you would like to use them
#    {"name": "1536x640 (2.4:1)", "width": 1536, "height": 640},
#    {"name": "640x1536 (1:2.4)", "width": 640, "height": 1536},
]

def closest_aspect_ratio(width, height):
    aspect_ratio = width / height
    closest_ratio = min(target_resolutions, key=lambda x: abs(x['width']/x['height'] - aspect_ratio))
    return closest_ratio

def random_target_resolution():
    return random.choice(target_resolutions)

def process_image(image_path, random_mode=False, png_mode=False):
    img = Image.open(image_path)
    width, height = img.size
    source_aspect_ratio = width / height
    
    if source_aspect_ratio.is_integer():
        source_aspect_ratio = int(source_aspect_ratio)
    else:
        source_aspect_ratio = round(source_aspect_ratio, 2)

    if random_mode:
        target = random_target_resolution()  # Pick a random target resolution
    else:
        target = closest_aspect_ratio(width, height)  # Find the nearest target resolution

    print(f"{os.path.basename(image_path)} converted to {target['name']}.")

    # Define subfolder name based on target resolution
    subfolder_name = f"{target['width']}_{target['height']}"

    # Crop to target aspect ratio
    target_aspect_ratio = target['width'] / target['height']
    if source_aspect_ratio > target_aspect_ratio:
        new_width = int(height * target_aspect_ratio)
        new_height = height
    else:
        new_width = width
        new_height = int(width / target_aspect_ratio)
    
    left_margin = (width - new_width) / 2
    top_margin = (height - new_height) / 2

    img = img.crop((left_margin, top_margin, left_margin + new_width, top_margin + new_height))

    # Resize to target dimensions
    img = img.resize((target['width'], target['height']), Image.LANCZOS)

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

def main(directory_path, random_mode=False, png_mode=False):
    files_resized = 0  # Initialize the counter for resized files
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            full_path = os.path.join(directory_path, filename)
            process_image(full_path, random_mode, png_mode)
            files_resized += 1  # Increment the counter for each resized file
    
    # Define the output directory path
    output_directory = os.path.join(args.directory_path, 'resized')
    
    return files_resized, output_directory  # Return the total count of resized files and the output directory path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resize images in a directory.')
    parser.add_argument('directory_path', type=str, help='Path to the directory containing images')
    parser.add_argument('--random', action='store_true', help='Resize images to a random aspect ratio')
    parser.add_argument('--png', action='store_true', help='Save images in lossless RGBA PNG format')
    
    args = parser.parse_args()

    # Record the start time
    start_time = time.time()

    # Call the main function with the input directory and optional flags
    files_resized, output_directory = main(args.directory_path, args.random, args.png)

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