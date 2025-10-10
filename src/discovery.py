
# Discovery component: traverse the file system safely.
# Why: Explicit exclusions and user-provided root reduce risk of destabilising the host.
from __future__ import annotations
import os
import psutil
from typing import Iterator, List, Set

def _platform_excludes() -> Set[str]:
    excludes = set()
    if os.name == "nt":
        excludes |= {r"C:\\Windows", r"C:\\Program Files", r"C:\\Program Files (x86)", r"C:\\$Recycle.Bin"}
    else:
        excludes |= {"/proc", "/sys", "/dev", "/run", "/var/lib/docker", "/var/run", "/snap"}
    return excludes

DEFAULT_EXCLUDES: Set[str] = _platform_excludes()

def mounted_roots() -> List[str]:
    roots = []
    for p in psutil.disk_partitions(all=False):
        if p.mountpoint and os.path.isdir(p.mountpoint):
            roots.append(p.mountpoint)
    return roots

def walk_safe(root: str, extra_excludes: Set[str] | None = None) -> Iterator[str]:
    ex = set(DEFAULT_EXCLUDES)
    if extra_excludes:
        ex |= set(extra_excludes)
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded dirs
        for d in list(dirnames):
            full = os.path.abspath(os.path.join(dirpath, d))
            if any(full == e or full.startswith(e + os.sep) for e in ex):
                dirnames.remove(d)
        for fn in filenames:
            yield os.path.join(dirpath, fn)
