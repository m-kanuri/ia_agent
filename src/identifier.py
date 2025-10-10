
# Identifier: prefer content-based MIME detection (python-magic), fallback to filetype, then extension.
from __future__ import annotations
import mimetypes
from typing import Tuple

_HAVE_MAGIC = False
_HAVE_FILETYPE = False
try:
    import magic  # type: ignore
    _HAVE_MAGIC = True
except Exception:
    pass
try:
    import filetype  # type: ignore
    _HAVE_FILETYPE = True
except Exception:
    pass

def detect_mime(path: str) -> Tuple[str, str]:
    """
    Attempts to determine the file's MIME type using a layered approach:
    1. python-magic (most reliable content check)
    2. filetype (lightweight content check)
    3. mimetypes (least reliable extension guess)
    
   The layered approach mitigates the risk that MIME-type analysis is not foolproof and behaves unpredictably. 
    """
    if _HAVE_MAGIC:
        try:
            m = magic.Magic(mime=True)
            mime = m.from_file(path) or ""
            if mime:
                return mime, "python-magic"
        except Exception:
            pass
    if _HAVE_FILETYPE:
        try:
            kind = filetype.guess(path)
            if kind and kind.mime:
                return kind.mime, "filetype"
        except Exception:
            pass
    mime, _ = mimetypes.guess_type(path)
    return (mime or "application/octet-stream"), "extension-guess"
