"""Shared utilities for all MTGT Lec07 chunks."""
import pandas as pd
import numpy as np

def normalize(s):
    """Convert Likert 1-5 to 0-1, or z-scores to sigmoid."""
    s = pd.to_numeric(s, errors='coerce')
    if s.min() >= 1 and s.max() <= 5:
        return s / 5.0
    elif s.min() >= 0 and s.max() <= 1:
        return s
    else:
        return 1 / (1 + np.exp(-s))

def pick_items(all_cols, keys):
    """Pick columns containing any of the keywords."""
    return [c for c in all_cols if any(k in c.lower() for k in keys)]
