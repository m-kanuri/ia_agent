
# Learner: minimal supervised demo with scikit-learn (if available).
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
    size = float(meta.get("size", 0.0))
    mime = str(meta.get("mime", ""))
    return [
        math.log1p(size),
        1.0 if mime.startswith("text/") else 0.0,
        1.0 if mime.startswith("image/") else 0.0,
        1.0 if mime == "application/pdf" else 0.0,
    ]

def train_demo(X: List[List[float]], y: List[int], model_path: str | None = None):
    if not _HAVE_SK:
        return None
    pipe = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=200))])
    pipe.fit(X, y)
    if model_path:
        joblib.dump(pipe, model_path)
    return pipe
