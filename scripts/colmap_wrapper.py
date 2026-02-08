import subprocess
import os
from pathlib import Path

def run_colmap_reconstruction(image_dir, output_dir):
    img_path = Path(image_dir)
    out_path = Path(output_dir)
    database_path = out_path / "database.db"
    sparse_path = out_path / "sparse"
    
    sparse_path.mkdir(parents=True, exist_ok=True)

    try:
        print("  -> Extracting features (CPU mode)...")
        subprocess.run([
            "colmap", "feature_extractor",
            "--database_path", str(database_path),
            "--image_path", str(img_path),
            "--SiftExtraction.use_gpu", "0"  # This bypasses the Qt/GPU dependency
        ], check=True, capture_output=True)

        print("  -> Matching features...")
        subprocess.run([
            "colmap", "exhaustive_matcher",
            "--database_path", str(database_path),
            "--SiftMatching.use_gpu", "0"    # Keep it consistent on CPU
        ], check=True, capture_output=True)

        print("  -> Mapping reconstruction...")
        subprocess.run([
            "colmap", "mapper",
            "--database_path", str(database_path),
            "--image_path", str(img_path),
            "--output_path", str(sparse_path)
        ], check=True, capture_output=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"COLMAP Error: {e.stderr.decode()}")
        return False