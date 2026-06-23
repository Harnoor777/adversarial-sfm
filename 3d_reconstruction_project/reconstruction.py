import os
import cv2
import numpy as np
import open3d as o3d
from datetime import datetime
from pathlib import Path

def reconstruct_3d(upload_folder, output_folder):
    """
    Real 3D reconstruction using Structure-from-Motion (SfM) and point cloud generation.
    
    Pipeline:
    1. Load images
    2. Detect and match features (SIFT/ORB)
    3. Estimate camera poses
    4. Triangulate 3D points
    5. Generate point cloud
    6. Create mesh
    7. Save as .ply
    
    Args:
        upload_folder: Path to folder containing uploaded images
        output_folder: Path to folder where .ply model will be saved
    
    Returns:
        dict: Status information about the reconstruction
    """
    print("=" * 70)
    print("🚀 3D RECONSTRUCTION PIPELINE STARTED")
    print("=" * 70)
    
    try:
        # Step 1: Load images
        print("\n📸 Step 1: Loading images...")
        image_files = sorted([f for f in os.listdir(upload_folder) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        
        if len(image_files) < 2:
            raise ValueError("Need at least 2 images for reconstruction")
        
        print(f"   Found {len(image_files)} images:")
        for img in image_files:
            print(f"   - {img}")
        
        images = []
        for img_file in image_files:
            img_path = os.path.join(upload_folder, img_file)
            img = cv2.imread(img_path)
            if img is not None:
                # Resize for performance (max 800px width)
                h, w = img.shape[:2]
                if w > 800:
                    scale = 800 / w
                    img = cv2.resize(img, (800, int(h * scale)))
                images.append(img)
        
        print(f"   ✅ Loaded {len(images)} images successfully")
        
        # Step 2: Feature detection and matching
        print("\n🔍 Step 2: Detecting features...")
        keypoints_list, descriptors_list = detect_features(images)
        print(f"   ✅ Detected features in all images")
        
        print("\n🔗 Step 3: Matching features between images...")
        matches_dict = match_features(descriptors_list)
        print(f"   ✅ Matched features between {len(matches_dict)} image pairs")
        
        # Step 4: Estimate camera poses and triangulate points
        print("\n📐 Step 4: Estimating camera poses...")
        points_3d, colors_3d = estimate_structure(images, keypoints_list, matches_dict)
        print(f"   ✅ Triangulated {len(points_3d)} 3D points")
        
        # Step 5: Create point cloud
        print("\n☁️  Step 5: Creating point cloud...")
        pcd = create_point_cloud(points_3d, colors_3d)
        
        # Clean up point cloud
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        print(f"   ✅ Point cloud created with {len(pcd.points)} points")
        
        # Step 6: Generate mesh
        print("\n🔷 Step 6: Generating mesh...")
        mesh = generate_mesh(pcd)
        print(f"   ✅ Mesh created with {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles")
        
        # Step 7: Save output
        print("\n💾 Step 7: Saving model...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"model_{timestamp}.ply"
        output_path = os.path.join(output_folder, output_filename)
        
        o3d.io.write_triangle_mesh(output_path, mesh)
        print(f"   ✅ Model saved: {output_filename}")
        
        print("\n" + "=" * 70)
        print("✅ RECONSTRUCTION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
        return {
            'status': 'completed',
            'images_processed': len(images),
            'points_generated': len(points_3d),
            'vertices': len(mesh.vertices),
            'triangles': len(mesh.triangles),
            'output_path': output_folder,
            'output_filename': output_filename,
            'message': f'Successfully reconstructed 3D model from {len(images)} images'
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("=" * 70)
        raise


def detect_features(images):
    """
    Detect keypoints and compute descriptors for all images.
    Uses SIFT if available, otherwise ORB.
    """
    keypoints_list = []
    descriptors_list = []
    
    # Try SIFT first (better quality), fallback to ORB
    try:
        detector = cv2.SIFT_create(nfeatures=2000)
        print("   Using SIFT feature detector")
    except:
        detector = cv2.ORB_create(nfeatures=2000)
        print("   Using ORB feature detector")
    
    for i, img in enumerate(images):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp, desc = detector.detectAndCompute(gray, None)
        keypoints_list.append(kp)
        descriptors_list.append(desc)
        print(f"   Image {i+1}: {len(kp)} keypoints detected")
    
    return keypoints_list, descriptors_list


def match_features(descriptors_list):
    """
    Match features between consecutive image pairs.
    """
    matches_dict = {}
    
    # Use BFMatcher for SIFT or FLANN for ORB
    if descriptors_list[0].dtype == np.float32:
        matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    else:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    for i in range(len(descriptors_list) - 1):
        matches = matcher.knnMatch(descriptors_list[i], descriptors_list[i+1], k=2)
        
        # Apply ratio test (Lowe's ratio test)
        good_matches = []
        for m_n in matches:
            if len(m_n) == 2:
                m, n = m_n
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
        
        matches_dict[(i, i+1)] = good_matches
        print(f"   Pair ({i}, {i+1}): {len(good_matches)} good matches")
    
    return matches_dict


def estimate_structure(images, keypoints_list, matches_dict):
    """
    Estimate 3D structure using triangulation.
    Simplified SfM: assumes first camera at origin, estimates relative poses.
    """
    h, w = images[0].shape[:2]
    
    # Camera intrinsic matrix (estimated)
    focal_length = max(w, h)
    K = np.array([
        [focal_length, 0, w/2],
        [0, focal_length, h/2],
        [0, 0, 1]
    ], dtype=np.float64)
    
    # First camera pose (identity)
    P1 = K @ np.hstack([np.eye(3), np.zeros((3, 1))])
    
    all_points_3d = []
    all_colors = []
    
    # Process each image pair
    for (i, j), matches in matches_dict.items():
        if len(matches) < 8:
            continue
        
        # Get matched keypoints
        pts1 = np.float32([keypoints_list[i][m.queryIdx].pt for m in matches])
        pts2 = np.float32([keypoints_list[j][m.trainIdx].pt for m in matches])
        
        # Estimate essential matrix
        E, mask = cv2.findEssentialMat(pts1, pts2, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        
        if E is None:
            continue
        
        # Recover pose
        _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K, mask=mask)
        
        # Second camera pose
        P2 = K @ np.hstack([R, t])
        
        # Triangulate points
        pts1_inliers = pts1[mask.ravel() == 1]
        pts2_inliers = pts2[mask.ravel() == 1]
        
        points_4d = cv2.triangulatePoints(P1, P2, pts1_inliers.T, pts2_inliers.T)
        points_3d = (points_4d[:3] / points_4d[3]).T
        
        # Filter points (remove outliers)
        distances = np.linalg.norm(points_3d, axis=1)
        valid_mask = (distances < np.percentile(distances, 95)) & (distances > 0)
        points_3d = points_3d[valid_mask]
        
        # Get colors from first image
        for pt_2d in pts1_inliers[valid_mask]:
            x, y = int(pt_2d[0]), int(pt_2d[1])
            if 0 <= x < w and 0 <= y < h:
                color = images[i][y, x]
                all_colors.append(color[::-1] / 255.0)  # BGR to RGB, normalize
            else:
                all_colors.append([0.5, 0.5, 0.5])
        
        all_points_3d.extend(points_3d)
    
    return np.array(all_points_3d), np.array(all_colors)


def create_point_cloud(points_3d, colors_3d):
    """
    Create Open3D point cloud from 3D points and colors.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_3d)
    pcd.colors = o3d.utility.Vector3dVector(colors_3d)
    
    # Estimate normals for better mesh generation
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    
    return pcd


def generate_mesh(pcd):
    """
    Generate triangle mesh from point cloud using Poisson surface reconstruction.
    """
    # Poisson surface reconstruction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9, width=0, scale=1.1, linear_fit=False
    )
    
    # Remove low density vertices
    vertices_to_remove = densities < np.quantile(densities, 0.1)
    mesh.remove_vertices_by_mask(vertices_to_remove)
    
    # Smooth mesh
    mesh = mesh.filter_smooth_simple(number_of_iterations=2)
    
    # Compute vertex normals
    mesh.compute_vertex_normals()
    
    return mesh
