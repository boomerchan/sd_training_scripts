import os
import sys
import argparse
import time

# Simple script to prepend a tag or activation word to txt files in a training dataset
# Usage: python prepend_tag.py /path/to/dir tag

# Example: python prepend_tag.py /SD_LoRA/samdoesart/100_samdoesart samdoesart
# "samdoesart, " would be prepended to every txt file in the directory

# Enclose strings with spaces in quotations: "samdoesart, 1girl"
# "samdoesart, 1girl, " would be prepended to every txt file in the directory

# --appened to add the tag to the end of the txt file
# Example: python prepend_tag.py /SD_LoRA/samdoesart/100_samdoesart samdoesart --append
# ", samdoesart" would be appended to every txt file in the directory

def prepend_string_to_files(directory, prepend_string, append=False):
    count_edited = 0
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                with open(file_path, 'w') as file:
                    if append:
                        lines[-1] = lines[-1].rstrip() + ', ' + prepend_string + '\n'
                    else:
                        lines[0] = prepend_string + ', ' + lines[0]
                    file.writelines(lines)
                count_edited += 1
    return count_edited

def main():
    parser = argparse.ArgumentParser(description="Prepend or append a string to all .txt files in a directory.")
    parser.add_argument("directory", help="The directory containing .txt files to edit.")
    parser.add_argument("string", help="The string to prepend or append.")
    parser.add_argument("--append", action="store_true", help="Append the string to the end of each file.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: The specified directory does not exist.")
        sys.exit(1)

    # Record the start time
    start_time = time.time()

    # Call the main function with the input directory and optional flags
    count_edited = prepend_string_to_files(args.directory, args.string, args.append)

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

    action = "appended" if args.append else "prepended"

    print(f"{action.capitalize()} '{args.string}' to {count_edited} files in {elapsed_time_str}.")

if __name__ == "__main__":
    main()