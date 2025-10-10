
import sys, os
sys.path.insert(0, '/mnt/data/ia_agent/src')
from identifier import detect_mime

def test_detect_mime_text():
    mime, method = detect_mime('/mnt/data/ia_agent/sample_data/note1.txt')
    assert isinstance(mime, str) and len(mime) > 0
    assert isinstance(method, str)

def test_detect_mime_pdf():
    mime, _ = detect_mime('/mnt/data/ia_agent/sample_data/report.pdf')
    assert "pdf" in mime or mime in ("application/octet-stream",)
