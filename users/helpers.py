from pathlib import Path
from typing import List, Tuple
from urllib.parse import unquote

from django.core.files.storage import FileSystemStorage

from .forms import FileForm
from img2txt.settings import MEDIA_ROOT


def get_file_paths(form: FileForm) -> Tuple[List, List]:
    """Helper function for saving uploaded files and returning paths."""
    img_paths = []
    txt_paths = []
    fs = FileSystemStorage()

    for f in form.files.values():
        name = fs.save(Path(f.name).name, f)
        img_path = Path(MEDIA_ROOT).joinpath(Path(unquote(fs.url(name))))
        img_paths.append(str(img_path))
        txt_paths.append(str(img_path.with_suffix('.txt')))
    return img_paths, txt_paths
