"""Run with Python and Pillow after adding images to the portfolio."""
from pathlib import Path
import re
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "images/optimized"
OUTPUT.mkdir(exist_ok=True)
sources = {}
pages_text = '\n'.join(page.read_text() for page in ROOT.glob('*.html'))
for path in (ROOT / 'images').iterdir():
    if path.suffix.lower() in ('.jpg', '.jpeg', '.png') and (path.name in pages_text or f'images/optimized/{path.stem}-' in pages_text):
        sources[path.relative_to(ROOT).as_posix()] = path
for page in ROOT.glob("*.html"):
    for name in re.findall(r'images/[^\s\"\'<>]+\.(?:jpg|jpeg|png)', page.read_text()):
        path = ROOT / name
        if path.exists():
            sources[name] = path

metadata = {}
for name, path in sources.items():
    with Image.open(path) as source:
        original = ImageOps.exif_transpose(source).convert("RGBA" if "A" in source.getbands() else "RGB")
        variants = []
        for limit in (640, 1280):
            resized = original.copy()
            resized.thumbnail((limit, limit), Image.Resampling.LANCZOS)
            target = OUTPUT / f"{path.stem}-{limit}.webp"
            resized.save(target, "WEBP", quality=90, method=6)
            variants.append((target.relative_to(ROOT).as_posix(), resized.width))
        target = OUTPUT / f"{path.stem}-full.webp"
        original.save(target, "WEBP", quality=92, method=6)
        metadata[name] = (original.size, variants, target.relative_to(ROOT).as_posix())

for page in ROOT.glob("*.html"):
    content = page.read_text()
    def update(match):
        tag = match.group()
        if 'id="largeImage"' in tag:
            return '<img id="largeImage" decoding="async" alt="Project preview">'
        src = re.search(r'src="([^"]+)"', tag)
        if src and src[1].startswith('images/optimized/'):
            for name, (_, variants, _) in metadata.items():
                if src[1] in [variant[0] for variant in variants]:
                    tag = tag.replace(src.group(), f'src="{name}"')
                    tag = re.sub(r'\s+(?:srcset|sizes|width|height|decoding|loading)="[^"]*"', '', tag)
                    src = re.search(r'src="([^"]+)"', tag)
                    break
        if not src or src[1] not in metadata:
            return tag
        size, variants, full = metadata[src[1]]
        logo = 'corner-logo' in tag
        about = src[1].endswith('new-8429.jpeg')
        sizes = '500px' if logo else '(max-width: 800px) 50vw, 25vw' if about else '(max-width: 500px) calc(100vw - 100px), (max-width: 800px) 45vw, 33vw'
        attrs = f' srcset="{variants[0][0]} {variants[0][1]}w, {variants[1][0]} {variants[1][1]}w" sizes="{sizes}" width="{size[0]}" height="{size[1]}" decoding="async"'
        if page.name == 'work.html':
            attrs += ' loading="lazy"'
        tag = tag.replace(src.group(), f'src="{variants[1][0]}"')
        return tag[:-1] + attrs + '>'
    content = re.sub(r'<img\b[^>]*>', update, content)
    for name, (_, _, full) in metadata.items():
        content = content.replace("'" + name + "'", "'" + full + "'")
    content = re.sub(r'(<img id="largeImage"\s+)src="[^"]+"', r'\1decoding="async"', content)
    page.write_text(content)

print(f"Optimized {len(metadata)} images. Originals preserved.")
print(f"Original referenced images: {sum(p.stat().st_size for p in sources.values()):,} bytes")
print(f"1280px versions: {sum((ROOT / v[1][1][0]).stat().st_size for v in metadata.values()):,} bytes")
