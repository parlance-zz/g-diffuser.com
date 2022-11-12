import os, glob
from PIL import Image
from PIL import ImageOps

files = glob.glob('gallery/*')

set_min_dims = {}
original_filenames = {}
gallery_filenames = {}

for file in files:
    
    basename = os.path.splitext(os.path.basename(file))[0]
    set_name = basename.split("_")[0]
    set_index = int(basename.split("_")[1])

    if set_index == 0:
        original_filenames[set_name] = file
        continue

    if set_index == 1:
        image = Image.open(file)
        width, height = image.size
        set_min_dims[set_name] = (width, height)

    gallery_filenames[set_name] = gallery_filenames.get(set_name, []) + [file]

for set_name, file in original_filenames.items():

    min_dims = set_min_dims[set_name]
    image = Image.open(file)
    width, height = image.size
    min_width = min(width, min_dims[0]); min_height = min(height, min_dims[1])

    print(set_name, file, "dims: " + str((width, height)),"min_dims: " + str(min_dims))
    if (width, height) != (min_width, min_height):
        print("resizing from ", (width, height), "to", min_dims, "...")
        ImageOps.contain(image, min_dims, method=Image.Resampling.LANCZOS).save(file, quality=90)

template_string = """
<div class="row" style="padding:0%">
    <div class="column" style="width: 50%; padding:0%"><img src="{0}"/></div>
    <div class="column" style="padding:0%; "><img src="{1}"/></div>
</div>
"""

html_str = ""
for set_name, files in gallery_filenames.items():
    for file in files:
        html_str += template_string.format(original_filenames[set_name], file)

with open("gallery.html", "w") as f:
    f.write(html_str)