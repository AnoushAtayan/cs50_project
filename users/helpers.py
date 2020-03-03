from pathlib import Path
from typing import List, Tuple
from urllib.parse import unquote

import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage

from img2txt.settings import MEDIA_ROOT
from .forms import FileForm


def get_file_paths(form: FileForm) -> Tuple[List, List]:
    """Helper function for saving uploaded files and returning paths."""
    img_paths = []
    txt_paths = []
    fs = FileSystemStorage()

    for f in form.files.values():
        name = fs.save(Path(f.name).name, f)
        path = Path(unquote(fs.url(name)))
        suffix = path.suffix
        absolute_path = Path(MEDIA_ROOT).joinpath(path.stem)
        img_paths.append(str(absolute_path.with_suffix(suffix)))
        txt_paths.append(str(absolute_path.with_suffix('.txt')))
    return img_paths, txt_paths


def img_to_txt(img_path: str, txt_path: str):
    """Read image and save text in .txt format"""
    with Image.open(img_path) as img:
        text = pytesseract.image_to_string(img)
        with open(txt_path, 'w') as txt:
            txt.write(text)
