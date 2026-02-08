import struct
import numpy as np

def read_images_binary(path_to_images_bin):
    """
    Minimal parser for COLMAP images.bin to get camera positions.
    """
    images = {}
    with open(path_to_images_bin, "rb") as fid:
        num_images = struct.unpack("<Q", fid.read(8))[0]
        for _ in range(num_images):
            image_properties = struct.unpack("<idddddddi", fid.read(64))
            image_id = image_properties[0]
            # Quaternion (qvec) and Translation (tvec) in COLMAP space
            qvec = np.array(image_properties[1:5])
            tvec = np.array(image_properties[5:8])
            camera_id = image_properties[8]
            
            # Read name
            name = ""
            while True:
                char = fid.read(1).decode("utf-8")
                if char == "\0":
                    break
                name += char
            
            # Skip points2D data
            num_points2D = struct.unpack("<Q", fid.read(8))[0]
            fid.read(24 * num_points2D)
            
            # COLMAP tvec is NOT the camera position, it's the translation.
            # Camera center in world coordinates = -R^T * t
            R = quaternion_to_rotation_matrix(qvec)
            camera_center = -R.T @ tvec
            images[name] = camera_center
    return images

def quaternion_to_rotation_matrix(qvec):
    qvec = qvec / np.linalg.norm(qvec)
    w, x, y, z = qvec
    return np.array([
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
        [2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2]
    ])