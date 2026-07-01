import numpy as np
import open3d as o3d
import os

def load_point_cloud(path):
    """Load a .ply file and return as numpy array"""
    pcd = o3d.io.read_point_cloud(path)
    points = np.asarray(pcd.points)
    print(f"Loaded {path} — {len(points)} points")
    return pcd, points

def chamfer_distance(points1, points2):
    """
    Compute Chamfer Distance between two point clouds.
    Lower = more similar
    Higher = more different (attack caused more damage)
    """
    # For each point in cloud1, find nearest point in cloud2
    pcd2 = o3d.geometry.PointCloud()
    pcd2.points = o3d.utility.Vector3dVector(points2)
    pcd2_tree = o3d.geometry.KDTreeFlann(pcd2)

    dist1 = []
    for point in points1:
        _, _, d = pcd2_tree.search_knn_vector_3d(point, 1)
        dist1.append(d[0])

    # For each point in cloud2, find nearest point in cloud1
    pcd1 = o3d.geometry.PointCloud()
    pcd1.points = o3d.utility.Vector3dVector(points1)
    pcd1_tree = o3d.geometry.KDTreeFlann(pcd1)

    dist2 = []
    for point in points2:
        _, _, d = pcd1_tree.search_knn_vector_3d(point, 1)
        dist2.append(d[0])

    # Chamfer distance = mean of both directions
    chamfer = np.mean(dist1) + np.mean(dist2)
    return chamfer

def main():
    clean_path = r"E:\adversarial-sfm\results\clean.ply"
    attacked_path = r"E:\adversarial-sfm\results\attacked_eps003.ply"

    # Load both point clouds
    clean_pcd, clean_points = load_point_cloud(clean_path)
    attacked_pcd, attacked_points = load_point_cloud(attacked_path)

    print(f"\nClean points: {len(clean_points)}")
    print(f"Attacked points: {len(attacked_points)}")

    # Compute Chamfer distance
    print("\nComputing Chamfer distance...")
    cd = chamfer_distance(clean_points, attacked_points)

    print(f"\n--- RESULTS ---")
    print(f"Chamfer Distance (clean vs attacked): {cd:.6f}")
    print(f"Higher = more damage from attack")

    # Save results to file
    results_path = r"E:\adversarial-sfm\results\chamfer_results.txt"
    with open(results_path, "w") as f:
        f.write(f"Chamfer Distance (clean vs attacked): {cd:.6f}\n")
        f.write(f"Clean point count: {len(clean_points)}\n")
        f.write(f"Attacked point count: {len(attacked_points)}\n")
    
    print(f"\nResults saved to {results_path}")

if __name__ == "__main__":
    main()