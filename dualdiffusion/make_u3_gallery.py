import os

from urllib.parse import urlparse, urlunparse


source = "dualdiffusion/u3_gallery"
dest = "dualdiffusion/u3_gallery.html"


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    normalized_url = parsed_url._replace(
        scheme=parsed_url.scheme.lower(),
        netloc=parsed_url.netloc.lower(),
    )
    return urlunparse(normalized_url).replace("\\", "/")

def get_step_count(file: str) -> int:
    prefix = "step_"
    start = file.index(prefix) + len(prefix)
    end = file.find("_", start)
    return file[start:end] if end != -1 else file[start:]

url_prefix = f"/{source}/"
cat_dirs = sorted(os.listdir(source), key=lambda x: int(x.split("_")[0]))
categories = []
total_samples = 0

for cat_dir in cat_dirs:

    samples = [s for s in os.listdir(os.path.join(source, cat_dir)) if s.endswith(".flac")]
    samples = sorted(samples, key=lambda s: int(get_step_count(s)), reverse=True)
    samples = [(get_step_count(s) + " steps", normalize_url(os.path.join(url_prefix, cat_dir, s))) for s in samples]
    total_samples += len(samples)

    cat_name = " ".join(cat_dir.split("_")[1:])
    desc_file = os.path.join(source, cat_dir, "description.txt")
    if os.path.isfile(desc_file):
        with open(desc_file, "r") as f:
            cat_description = f.read().strip()
    else:
        cat_description = ""
    categories.append((cat_name, cat_description, cat_dir, samples))

print(f"Total categories: {len(categories)}", f"Total samples: {total_samples}\n")

for cat_name, cat_description, cat_dir, samples in categories:
    print(f"Category: '{cat_name}'", f"Dir: '{cat_dir}'", f"Num Samples: {len(samples)}")
    for label, url in samples:
        print(f"  Label: '{label}'", f"URL: '{url}'")
    print("")

cat_start_template_description = """
<div class="sample_category_box">
    <h4 class="sample_category_description" style="color: violet;">{0}</h4>
    <p class="row sample_category_description" style="padding: 12px">{1}</p>
"""
cat_start_template_no_description = """
<div class="sample_category_box">
    <h4 class="sample_category_description" style="color: violet;">{0}</h4>
"""
sample_template = """
    <div class="row sample_row">
        <figure><figcaption class="audio-caption">{0}</figcaption></figure>
        <audio controls preload="none" src="{1}"></audio>
        </figure>
    </div>
"""

cat_end_template = """
</div>
"""

html_str = ""

for cat_name, cat_description, cat_dir, samples in categories:

    cat_start_template = cat_start_template_no_description if not cat_description else cat_start_template_description
    html_str += cat_start_template.format(cat_name, cat_description)
    for label, url in samples:
        html_str += sample_template.format(label, url)
    html_str += cat_end_template

with open(dest, "w") as f:
    f.write(html_str)