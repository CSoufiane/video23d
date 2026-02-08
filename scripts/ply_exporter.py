import struct
from pathlib import Path

def export_scaled_ply(bin_path, output_path, scale):
    print(f"  -> Reading COLMAP binary points from {bin_path}")
    
    try:
        with open(bin_path, "rb") as f:
            # 1. Read the number of points (uint64)
            num_points = struct.unpack("<Q", f.read(8))[0]
            
            with open(output_path, "w") as ply:
                # 2. Write PLY Header
                ply.write("ply\n")
                ply.write("format ascii 1.0\n")
                ply.write(f"element vertex {num_points}\n")
                ply.write("property float x\n")
                ply.write("property float y\n")
                ply.write("property float z\n")
                ply.write("property uchar red\n")
                ply.write("property uchar green\n")
                ply.write("property uchar blue\n")
                ply.write("end_header\n")

                # 3. Parse each point
                for _ in range(num_points):
                    # Point3D structure: 
                    # id(Q), x(d), y(d), z(d), r(B), g(B), b(B), error(d)
                    data = struct.unpack("<QdddBBBd", f.read(43))
                    
                    # Apply the scale factor to coordinates
                    x, y, z = data[1] * scale, data[2] * scale, data[3] * scale
                    r, g, b = data[4], data[5], data[6]
                    
                    ply.write(f"{x} {y} {z} {r} {g} {b}\n")
                    
                    # Each point entry is followed by variable-length 'track' data
                    # We must skip the track length (uint64) and the track data itself
                    track_len = struct.unpack("<Q", f.read(8))[0]
                    f.read(track_len * 8) # Each track element is 2 * uint32 = 8 bytes

        print(f"  -> Successfully exported {num_points} points to {output_path}")
        return True

    except Exception as e:
        print(f"  -> Error during PLY export: {e}")
        return False