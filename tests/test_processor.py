
import sys, os
sys.path.insert(0, '/mnt/data/ia_agent/src')
from processor import basic_metadata

def test_basic_metadata_has_sha256():
    meta = basic_metadata('/mnt/data/ia_agent/sample_data/note1.txt', "text/plain")
    assert "sha256" in meta and len(meta["sha256"]) == 64
