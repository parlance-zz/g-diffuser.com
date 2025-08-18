import os, glob

from urllib.parse import urlparse, urlunparse


source = "dualdiffusion/u3_gallery/**"
dest = "dualdiffusion/u3_gallery.html"


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    normalized_url = parsed_url._replace(
        scheme=parsed_url.scheme.lower(),
        netloc=parsed_url.netloc.lower(),
    )
    return urlunparse(normalized_url)

def get_step_count(file: str) -> int:
    prefix = "step_"
    start = file.index(prefix) + len(prefix)
    end = file.find("_", start)
    return file[start:end] if end != -1 else file[start:]
    
files = glob.glob(source, recursive=True)

gallery = {}
label_counts = {}

for file in sorted(files):
    if not os.path.isfile(file) or not os.path.splitext(file)[1].lower() == ".flac":
        continue
    
    if " " in os.path.basename(file):
        new_file = os.path.basename(file).replace(" ", "_")
        new_file = os.path.join(os.path.dirname(file), new_file)
        os.rename(file, new_file)
        file = new_file

    name = os.path.basename(os.path.dirname(file)).replace("_", " ")
    step_count = get_step_count(os.path.basename(file))

    if name not in label_counts:
        label_counts[name] = 1
    else:
        label_counts[name] += 1
    
    name += f" {label_counts[name]} ({step_count})"
    gallery[name] = os.path.relpath(file, "dualdiffusion/").replace("\\", "/")

print(len(gallery), "file(s) found\n")

gallery = {
    k.split(" ", 1)[1]: v
    for k, v in sorted(
        gallery.items(),
        key=lambda item: (
            int(item[0].split(" ")[0]),                          # primary sort
            -int(item[0].rsplit("(", 1)[1].rstrip(")"))          # secondary sort (descending)
        )
    )
}

for k, v in gallery.items():
    print("key:", k, "val:", v)

#exit()

template_string = """
<div class="row" style="padding:0%">
    <figure><figcaption class="audio-caption">{0}</figcaption></figure>
    <audio controls preload="none" src="{1}"></audio>
    </figure>
</div>
"""

html_str = ""
for name, file in gallery.items():
    print(name, file)
    html_str += template_string.format(name, file)

with open(dest, "w") as f:
    f.write(html_str)