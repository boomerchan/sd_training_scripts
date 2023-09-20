# sd_training_scripts
 Miscellaneous python scripts for managing SD training datasets.

## rename_bulk.py

**Recommended to complete this step before generating txt files for captions.** Renames all files within a specified directory and sequentially appends a number to each file, regardless of the file extension (jpg, png, etc). Usage:
```
python rename_bulk.py /path/to/dir newfilename
```
Output: newfilename-1.png, newfilename-2.jpg, newfilename-3.png, etc.

## resize_bulk.py

Simple script to crop and resize all images in a folder to the closest SDXL training resolution based on its resolution. **The original images are not modified.** New cropped and resized images are placed inside of a folder named `/resized`. Default usage:
```
python resize_bulk.py /path/to/dir [--width pixels] [--height pixels] [--random] [--png] [--shortside pixels] [--longside pixels]
```
By default, selects the resolution closest to the original image aspect ratio and outputs as jpg. Use commandline flag `--random` to randomize the aspect ratio. Use commandline flag `--png` to save as png (this is slower and uses more space). Example:
```
python resize_bulk.py /path/to/dir --random --png
```
### --height and --width
`--height` and `--width` specify the pixels respectively. If only one --height or --width is used, the image will be scaled to its original aspect ratio. For example, you would crop and resize all images to 512x768 by entering:
```
python resize_bulk.py /path/to/dir --width 512 --height 768
```
Or, to resize the width to 512 and the height according to the original aspect ratio, you would enter:
```
python resize_bulk.py /path/to/dir --width 512
```
### --short-side and --long-side
`--short-side` specifies the pixels for the shortest side, ensuring a minimum width/height. `--long-side` specifies the pixels for the longest side, ensuring a maximum width/height.

For example, let's resize 2 images. `1167x1500` and `1200x960`:
```
python resize_bulk.py /path/to/dir --short-side 768
```
Would resize the images to `768x984` and `960x768` respectively.
```
python resize_bulk.py /path/to/dir --long-side 768
```
Would resize the images to `599x768` and `768x614` respectively.
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