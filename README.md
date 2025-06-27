# organize-files.py

## What is this?

I find myself downloading a lot of files (images and videos) on my
computer. This script automatically renames files to their hash (which
is useful in seeing if you have duplicates of a file) and places them
in a directory based on their last modified time (which I've found
useful as a way to organize my files).

## How to run

Simply run
```
python organize_media.py --source-dir A --images-dir B --videos-dir C
```

And this script will move all images in source directory `A` to directory `B`, and all videos in to directory `C`