import os
import time
import sys

# Simple script to rename all files in a given directory
# Recommended to do this step before generating .txt files for captions
# Iterates a new number every file regardless of file extension (jpg, png, etc)
# Usage: python rename_bulk.py /path/to/dir newfilename

# Example: python rename_bulk.py /path/to/dir newfilename
# newfilename-1.png, newfilename-2.jpg, newfilename-3.png, etc

def rename_files_in_directory(directory_path, new_filename):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return
    
    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # Initialize a counter to append to the filename
    counter = 1
    
    # Initialize a counter to keep track of renamed files
    files_renamed = 0
    
    # Iterate through the files and rename them
    for file in files:
        file_extension = os.path.splitext(file)[1]
        new_file_name = f"{new_filename}-{counter}{file_extension}"
        source_path = os.path.join(directory_path, file)
        destination_path = os.path.join(directory_path, new_file_name)
        
        # Check if the destination file already exists
        while os.path.exists(destination_path):
            counter += 1
            new_file_name = f"{new_filename}-{counter}{file_extension}"
            destination_path = os.path.join(directory_path, new_file_name)
        
        try:
            # Rename the file
            os.rename(source_path, destination_path)
            print(f"Renamed '{file}' to '{new_file_name}'")
            
            # Increment the counters
            counter += 1
            files_renamed += 1
        except Exception as e:
            print(f"Error renaming '{file}': {str(e)}")

    return files_renamed

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python rename.py /path/to/directory new_filename")
    else:
        directory_path = sys.argv[1]
        new_filename = sys.argv[2]
        
        # Call the function to rename files and get the count of renamed files
        renamed_count = rename_files_in_directory(directory_path, new_filename)

    # Record the start time
    start_time = time.time()

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

    # Print the number of files renamed and the elapsed time in HH:MM:SS format
    print(f"{renamed_count} files renamed in {elapsed_time_str}.")