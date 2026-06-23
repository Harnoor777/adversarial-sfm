import open3d as o3d
import os
import glob

# Path to the output folder
output_folder = "output"

# Find all .ply files
ply_files = glob.glob(os.path.join(output_folder, "*.ply"))

if not ply_files:
    print("No .ply files found in output folder.")
    exit()

# Pick the most recently modified file
latest_file = max(ply_files, key=os.path.getmtime)
print(f"Loading latest model: {latest_file}")

# Load the mesh or point cloud
try:
    mesh = o3d.io.read_triangle_mesh(latest_file)
    if mesh.is_empty():
        # fallback to point cloud
        pcd = o3d.io.read_point_cloud(latest_file)
        if pcd.is_empty():
            print("PLY file is empty or invalid.")
            exit()
        # Try interactive display
        o3d.visualization.draw_geometries([pcd])
    else:
        # Try interactive display
        o3d.visualization.draw_geometries([mesh])

except Exception as e:
    print(f"Interactive display failed: {e}")
    print("Saving an offscreen snapshot instead...")

    # Offscreen rendering
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)  # No window
    vis.add_geometry(mesh)
    vis.poll_events()
    vis.update_renderer()
    # Save snapshot
    snapshot_path = os.path.join(output_folder, "model_preview.png")
    vis.capture_screen_image(snapshot_path)
    vis.destroy_window()
    print(f"Snapshot saved to: {snapshot_path}")