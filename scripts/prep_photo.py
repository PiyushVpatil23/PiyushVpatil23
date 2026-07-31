"""Prepare a portrait for high-contrast ASCII conversion.
Usage: python scripts/prep_photo.py source-photo.jpg
"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/prep_photo.py source-photo.jpg")

source = Image.open(sys.argv[1]).convert("RGBA")
subject = remove(source)
white = Image.new("RGBA", subject.size, "white")
composite = Image.alpha_composite(white, subject).convert("RGB")

gray = cv2.cvtColor(np.array(composite), cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
boosted = clahe.apply(gray)
Image.fromarray(boosted).save("source-prepped.png")
print("Wrote source-prepped.png")
