import os, glob

from urllib.parse import urlparse, urlunparse

def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    normalized_url = parsed_url._replace(
        scheme=parsed_url.scheme.lower(),
        netloc=parsed_url.netloc.lower(),
    )
    return urlunparse(normalized_url)

files = glob.glob('dualdiffusion/gallery/*')

gallery = {}

for file in files:
    if not os.path.isfile(file) or not os.path.splitext(file)[1].lower() == ".flac":
        continue
    
    if " " in os.path.basename(file):
        new_file = os.path.basename(file).replace(" ", "_")
        new_file = os.path.join(os.path.dirname(file), new_file)
        os.rename(file, new_file)
        file = new_file

    name = os.path.splitext(os.path.basename(file))[0].replace("_", " ")
    gallery[name] = os.path.relpath(file, "dualdiffusion/").replace("\\", "/")

# sort gallery by number that is at beginning of filename followed by an underscore
gallery = {k.split(" ", 1)[1]: v for k, v in sorted(gallery.items(), key=lambda item: int(item[0].split(" ")[0]))}

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

with open("dualdiffusion/gallery.html", "w") as f:
    f.write(html_str)