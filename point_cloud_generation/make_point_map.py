import numpy as np
import cv2
from tqdm import tqdm

# def normalize_point_cloud(points):
#     centroid = np.mean(points, axis=0)
#     points = points - centroid
#     furthest_distance = np.max(np.sqrt(np.sum(points ** 2, axis=1)))
#     points = points / furthest_distance
#     return points

def create_ply_from_depth_image(image_path, depth_map_path, ply_path, depth_scale=10.0):
    # Load the RGB image and depth map
    rgb_image = cv2.imread(image_path)
    depth_map = cv2.imread(depth_map_path, cv2.IMREAD_UNCHANGED)  # Load as is (depth values)

    # Check if images are loaded correctly
    if rgb_image is None:
        raise FileNotFoundError(f"Could not load image from path: {image_path}")
    if depth_map is None:
        raise FileNotFoundError(f"Could not load depth map from path: {depth_map_path}")

    # Get the dimensions of the image
    height, width = depth_map.shape

    # Create a list for points and colors
    points = []
    colors = []

    # Assuming a simple camera model with focal lengths (fx, fy) and principal point (cx, cy)
    fx = 10.0  # focal length in x direction
    fy = 10.0  # focal length in y direction
    cx = width / 2
    cy = height / 2

    for y in tqdm(range(height)):
        for x in range(width):
            z = depth_map[y, x] 
            if z > 0:  # Only consider points with valid depth
                # Calculate 3D coordinates
                X = (x - cx) * z / fx
                Y = (y - cy) * z / fy
                points.append((X, Y, z*depth_scale))

                # Get color from the RGB image
                color = rgb_image[y, x]
                colors.append((color[2], color[1], color[0]))  # BGR to RGB

    # Write to PLY file
    with open(ply_path, 'w') as ply_file:
        ply_file.write("ply\n")
        ply_file.write("format ascii 1.0\n")
        ply_file.write(f"element vertex {len(points)}\n")
        ply_file.write("property float x\n")
        ply_file.write("property float y\n")
        ply_file.write("property float z\n")
        ply_file.write("property uchar red\n")
        ply_file.write("property uchar green\n")
        ply_file.write("property uchar blue\n")
        ply_file.write("end_header\n")
        
        for (X, Y, Z), (R, G, B) in zip(points, colors):
            ply_file.write(f"{X} {Y} {Z} {R} {G} {B}\n")

# Example usage with depth exaggeration:
create_ply_from_depth_image('frame0001.png', 'oframe0001.png', 'output.ply', depth_scale=20.0)
