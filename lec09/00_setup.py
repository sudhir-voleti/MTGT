# ═══════════════════════════════════════════════════════════════════
#  LEC09 SETUP: Imports + Base URL + Utility Load
# ═══════════════════════════════════════════════════════════════════

import requests, io, os, numpy as np, pandas as pd, matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

# Your GitHub raw base path
BASE = "https://raw.githubusercontent.com/sudhir-voleti/MTGT/refs/heads/main/lec09/"

# Load shared utilities
print("Loading utils.py …")
exec(requests.get(BASE + "utils.py").text)
print("✅ utils.py loaded")

# Yana-specific helpers
def yana_normalize(s):
    """Convert Likert or part-worths to 0-1 if needed."""
    s = pd.to_numeric(s, errors='coerce')
    if s.min() >= 1 and s.max() <= 5:
        return s / 5.0
    elif s.min() >= 0 and s.max() <= 1:
        return s
    else:
        return (s - s.min()) / (s.max() - s.min() + 1e-8)

def pick_yana_items(all_cols, keys):
    """Pick columns containing any of the keywords."""
    return [c for c in all_cols if any(k in c.lower() for k in keys)]

print("✅ Yana helpers ready")
