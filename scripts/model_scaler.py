from scripts.colmap_loader import read_images_binary
import numpy as np
import json

def calculate_scale(aruco_json, images_bin_path):
    with open(aruco_json, 'r') as f:
        aruco_data = json.load(f)
    
    colmap_images = read_images_binary(images_bin_path)
    
    scales = []
    # Find frames present in both datasets
    common_frames = sorted(list(set(aruco_data.keys()) & set(colmap_images.keys())))
    
    if len(common_frames) < 2:
        return 1.0

    # Calculate distance between consecutive common frames
    for i in range(len(common_frames) - 1):
        f1, f2 = common_frames[i], common_frames[i+1]
        
        # ArUco distance (meters)
        dist_aruco = np.linalg.norm(np.array(aruco_data[f1][0]['tvec']) - 
                                    np.array(aruco_data[f2][0]['tvec']))
        
        # COLMAP distance (units)
        dist_colmap = np.linalg.norm(colmap_images[f1] - colmap_images[f2])
        
        if dist_colmap > 1e-6:
            scales.append(dist_aruco / dist_colmap)
    
    return np.median(scales) if scales else 1.0