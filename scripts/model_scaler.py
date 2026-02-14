from scripts.colmap_loader import read_images_binary
import numpy as np
import json
from pathlib import Path

def calculate_scale(aruco_json, images_bin_path):
    # Guard clause: If path is None or file doesn't exist, return default scale 
    if images_bin_path is None or not Path(images_bin_path).exists():
        return 1.0

    with open(aruco_json, 'r') as f:
        aruco_data = json.load(f)
    
    colmap_images = read_images_binary(images_bin_path)
    
    scales = []
    # Find frames present in both datasets [cite: 12, 14]
    common_frames = sorted(list(set(aruco_data.keys()) & set(colmap_images.keys())))
    
    if len(common_frames) < 2:
        return 1.0

    for i in range(len(common_frames) - 1):
        f1, f2 = common_frames[i], common_frames[i+1]
        
        # Accessing the first marker's tvec for scale estimation [cite: 12]
        # Implementation change: accessing list index [0] safely
        try:
            tvec1 = np.array(aruco_data[f1][0]['tvec'])
            tvec2 = np.array(aruco_data[f2][0]['tvec'])
            
            dist_aruco = np.linalg.norm(tvec1 - tvec2)
            dist_colmap = np.linalg.norm(colmap_images[f1] - colmap_images[f2])
            
            if dist_colmap > 1e-6:
                scales.append(dist_aruco / dist_colmap)
        except (IndexError, KeyError):
            continue
    
    return float(np.median(scales)) if scales else 1.0