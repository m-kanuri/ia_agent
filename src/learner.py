# Intelligent Forensics Agent (Agent 1) — Identifier v1.0
# Module: learner.py
# Author: Murthy Kanuri
# Date: 10 October 2025
# Purpose:
#   Tiny, advisory model that learns a simple rule of thumb from metadata
#   (no file contents). Used to flag “likely non-text” files for archiving.
from __future__ import annotations
from typing import List, Dict
import math
try:
    from sklearn.linear_model import LogisticRegression  # type: ignore
    from sklearn.pipeline import Pipeline  # type: ignore
    from sklearn.preprocessing import StandardScaler  # type: ignore
    import joblib  # type: ignore
    _HAVE_SK = True
except Exception:
    _HAVE_SK = False

def features_from_meta(meta: Dict) -> List[float]:
    """
    Build a small, content-free feature vector from file metadata.

    Features (order matters for the simple pipeline):
      0) log1p(size)         — compresses the heavy-tailed size distribution
      1) is_text             — 1.0 if MIME starts with 'text/'
      2) is_image            — 1.0 if MIME starts with 'image/'
      3) is_pdf              — 1.0 if MIME is exactly 'application/pdf'

    """
    size = float(meta.get("size", 0.0))
    mime = str(meta.get("mime", ""))
    return [
        math.log1p(size),
        1.0 if mime.startswith("text/") else 0.0,
        1.0 if mime.startswith("image/") else 0.0,
        1.0 if mime == "application/pdf" else 0.0,
    ]

def train_demo(X: List[List[float]], y: List[int], model_path: str | None = None):
     """
    Fit a very small model (scale -> logistic regression) on these features.

    Notes
    -----
    - Advisory only: this is to show where learning lives in the design.
      It does not replace human judgement.
    - If scikit-learn isn’t installed, we just return None and carry on.

    Args:
        X: feature rows from `features_from_meta`.
        y: labels you provide (e.g. 1 = likely archive, 0 = keep).
        model_path: optional path to save the fitted pipeline with joblib.

    Returns:
        sklearn Pipeline or None (when scikit-learn isn’t available).
    """
    if not _HAVE_SK:
        return None
    pipe = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=200))])
    pipe.fit(X, y)
    if model_path:
        joblib.dump(pipe, model_path)
    return pipe
