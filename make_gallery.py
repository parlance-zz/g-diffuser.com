import os, glob
from PIL import Image
from PIL import ImageOps

JPG_QUALITY = 90

files = glob.glob('gallery/*')

set_min_dims = {}
original_filenames = {}
gallery_filenames = {}

for file in files:
    
    basename = os.path.splitext(os.path.basename(file))[0]
    extension = os.path.splitext(file)[1].lower()
    set_name = basename.split("_")[0]
    set_index = int(basename.split("_")[1])

    if extension != ".jpg":
        new_file = os.path.splitext(file)[0] + ".jpg"
        print("Converting ", file, " to ", new_file, "...")
        Image.open(file).save(new_file, quality=JPG_QUALITY)
        print("Removing ", file, "...")
        os.remove(file)
        file = new_file

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
    
    need_resize = False
    if min_dims[0] < min_dims[1]:
        if width != min_dims[0]: need_resize = True
    else:
        if height != min_dims[1]: need_resize = True

    print(set_name, file, "dims: " + str((width, height)),"min_dims: " + str(min_dims))
    if need_resize:
        print("resizing from ", (width, height), "to", min_dims, "...")
        ImageOps.contain(image, min_dims, method=Image.Resampling.LANCZOS).save(file, quality=JPG_QUALITY)

template_string = """
<div class="row" style="padding:0%">
    <div class="column" style="width: {0}%; padding:0%"><img src="{1}"/></div>
    <div class="column" style="padding:0%; "><img src="{2}"/></div>
</div>
"""

html_str = ""
for set_name, files in gallery_filenames.items():
    for file in files:
        width_ratio = 100 * Image.open(original_filenames[set_name]).size[0] / Image.open(file).size[0]
        html_str += template_string.format(width_ratio, original_filenames[set_name], file)

with open("gallery.html", "w") as f:
    f.write(html_str)