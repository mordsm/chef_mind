"""Extract every PDF page locally and queue image-containing pages for local OCR.

Requires PyMuPDF. Run with the local Python that has it installed; no API calls.
The resulting source material remains inside this project's local Vault.
"""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import fitz

PROJECT = Path(__file__).resolve().parents[1]
DEST = PROJECT / "vault/Culinary-Knowledge/09_Sources/Full-Books"
SCRATCH = PROJECT / "tmp-book-processing"


def prepare(paths, book, offsets):
    assets = DEST / "_assets" / book
    assets.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(exist_ok=True)
    pages, queue = [], []
    for source, offset in zip(paths, offsets, strict=True):
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        source_asset = assets / f"source-{offset:03}.pdf"
        shutil.copyfile(source, source_asset)
        doc = fitz.open(source)
        for split_page, page in enumerate(doc, 1):
            number = offset + split_page - 1
            text = page.get_text(sort=True)
            target = SCRATCH / f"{book}-{number:03}.txt"
            target.write_text(text, encoding="utf-8")
            images = len(page.get_images())
            record = {"book": book, "pdf_page": number, "split_page": split_page,
                      "source_filename": source.name, "source_sha256": digest,
                      "native_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                      "native_text_chars": len(text), "images": images, "text_path": str(target)}
            record["source_asset"] = source_asset.relative_to(DEST).as_posix()
            if images:
                image = assets / f"page-{number:03}.jpg"
                if not image.exists():
                    page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(image, jpg_quality=88)
                output = SCRATCH / f"{book}-{number:03}.ocr.json"
                record["image_path"] = image.relative_to(DEST).as_posix()
                record["ocr_path"] = str(output)
                queue.append({"image": str(image), "output": str(output)})
            pages.append(record)
    (SCRATCH / f"{book}-pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    queue_path = SCRATCH / f"{book}-ocr-queue.json"
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{book}: {len(pages)} pages extracted; {len(queue)} image pages queued at {queue_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("book", choices=["nosrat", "avir"])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--offsets", nargs="+", type=int)
    args = parser.parse_args()
    prepare(args.paths, args.book, args.offsets or [1])
