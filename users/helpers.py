import zipfile
from os.path import basename
from pathlib import Path
from urllib.parse import unquote

import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage

from img2txt.settings import MEDIA_ROOT
from .forms import FileForm


def img_to_txt(img_path: str, txt_path: str) -> str:
    """Read image and save text in .txt format"""
    with Image.open(img_path) as img:
        text = pytesseract.image_to_string(img)
        with open(txt_path, 'w') as txt:
            txt.write(text)
    return txt_path


def clear_user_folder(username: str):
    """Clear media folder of specific user."""
    folder_name = Path(MEDIA_ROOT).joinpath(username)
    if Path.exists(folder_name):
        for f in folder_name.iterdir():
            f.unlink()


def parse_files(form: FileForm, username: str) -> str:
    """Helper function for saving uploaded files, parsing them and creating zip file from them."""
    folder_name = Path(MEDIA_ROOT).joinpath(username)
    zip_file_path = folder_name.joinpath('output.zip')
    folder_name.mkdir(exist_ok=True, parents=True)
    fs = FileSystemStorage(location=folder_name)

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for f in form.files.getlist('file'):
            name = fs.save(Path(f.name).name, f)
            path = Path(unquote(fs.url(name)))
            suffix = path.suffix
            absolute_path = folder_name.joinpath(path.stem)
            txt_path = img_to_txt(
                str(absolute_path.with_suffix(suffix)), str(absolute_path.with_suffix('.txt')))
            zip_file.write(txt_path, arcname=basename(txt_path))
    return str(zip_file_path)
