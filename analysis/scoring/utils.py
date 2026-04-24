
import numpy as np

def normalize(series, hist_series):
    denom = hist_series.max() - hist_series.min()
    if denom == 0:
        return series * 0
    return (series - hist_series.min()) / denom

def normalize_scaled(series, hist_series):
    min_val = hist_series.min()
    max_val = hist_series.max()

    scaled = (series - min_val) / (max_val - min_val)
    scaled = scaled.clip(0, 1)
    return 0.1 + 0.8 * scaled
