# sd_training_scripts
 Miscellaneous python scripts for managing SD training datasets.

## rename_bulk.py

**Recommended to complete this step before generating txt files for captions.** Renames all files within a specified directory and sequentially appends a number to each file, regardless of the file extension (jpg, png, etc). Usage:
```
python rename_bulk.py /path/to/dir newfilename
```
Output: newfilename-1.png, newfilename-2.jpg, newfilename-3.png, etc.

## resize_bulk.py

Simple script to crop and resize all images in a folder to an SDXL training value. **The original images are not modified.** New cropped and resized images are placed inside of a folder named `/resized`. Usage:
```
python resize_bulk.py /path/to/dir
```
By default, selects the resolution closest to the original image aspect ratio and outputs as jpg. Use commandline flag `--random` to randomize the aspect ratio. Use commandline flag `--png` to save as png (this is slower and uses more space). Example:
```
python resize_bulk.py /path/to/dir --random --png
```

## prepend_tag.py
Simple script to prepend a tag or activation word to txt files in a training dataset. Example:
```
python prepend_tag.py /path/to/100_samdoesart samdoesart
```
"samdoesart, " would be prepended to every txt file in the directory. Enclose strings with spaces in quotations:
```
python prepend_tag.py /path/to/100_samdoesart "samdoesart, 1girl"
```
"samdoesart, 1girl, " would be prepended to every txt file in the directory.

Use the commandline flag `--appened` to add the tag to the end of the txt file. Example:
```
python prepend_tag.py /path/to/100_samdoesart samdoesart --append
```
", samdoesart" would be appended to every txt file in the directory.

All scripts were written with the help of ChatGPT.