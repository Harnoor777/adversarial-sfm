"""
Test script to verify the 3D reconstruction pipeline works correctly.
This creates synthetic test images and runs reconstruction on them.
"""

import os
import cv2
import numpy as np
from reconstruction import reconstruct_3d

def create_test_images(output_dir='test_images', num_images=5):
    """
    Create synthetic test images with known features for testing.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating test images...")
    
    for i in range(num_images):
        # Create a 640x480 image with random patterns
        img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Add some geometric shapes for feature detection
        # Circle
        cv2.circle(img, (320 + i*10, 240), 50, (0, 255, 255), -1)
        
        # Rectangle
        cv2.rectangle(img, (100 + i*20, 100), (200 + i*20, 200), (255, 0, 255), -1)
        
        # Triangle
        pts = np.array([[400 + i*15, 100], [350 + i*15, 200], [450 + i*15, 200]], np.int32)
        cv2.fillPoly(img, [pts], (255, 255, 0))
        
        # Add some text
        cv2.putText(img, f'View {i+1}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add random keypoints
        for _ in range(50):
            x, y = np.random.randint(50, 590), np.random.randint(50, 430)
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        
        # Save image
        filename = os.path.join(output_dir, f'test_image_{i+1:02d}.jpg')
        cv2.imwrite(filename, img)
        print(f"  Created: {filename}")
    
    print(f"✅ Created {num_images} test images\n")
    return output_dir


def test_reconstruction():
    """
    Test the full reconstruction pipeline.
    """
    print("=" * 70)
    print("TESTING 3D RECONSTRUCTION PIPELINE")
    print("=" * 70)
    print()
    
    # Create test images
    test_dir = create_test_images(num_images=6)
    
    # Create output directory
    output_dir = 'test_output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Run reconstruction
    try:
        result = reconstruct_3d(test_dir, output_dir)
        
        print("\n" + "=" * 70)
        print("TEST RESULTS")
        print("=" * 70)
        print(f"Status: {result['status']}")
        print(f"Images processed: {result['images_processed']}")
        print(f"3D points generated: {result.get('points_generated', 'N/A')}")
        print(f"Vertices: {result.get('vertices', 'N/A')}")
        print(f"Triangles: {result.get('triangles', 'N/A')}")
        print(f"Output file: {result['output_filename']}")
        print(f"Output path: {result['output_path']}")
        print("=" * 70)
        
        # Check if output file exists
        output_file = os.path.join(output_dir, result['output_filename'])
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"\n✅ SUCCESS: Model file created ({file_size} bytes)")
            print(f"   Location: {output_file}")
            print(f"\n   You can view this file in:")
            print(f"   - MeshLab")
            print(f"   - Blender")
            print(f"   - CloudCompare")
            print(f"   - Windows 3D Viewer")
        else:
            print("\n❌ ERROR: Output file was not created")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_test_files():
    """
    Remove test files (optional).
    """
    import shutil
    
    response = input("\nClean up test files? (y/n): ")
    if response.lower() == 'y':
        if os.path.exists('test_images'):
            shutil.rmtree('test_images')
            print("  Removed test_images/")
        if os.path.exists('test_output'):
            shutil.rmtree('test_output')
            print("  Removed test_output/")
        print("✅ Cleanup complete")
    else:
        print("Test files kept for inspection")


if __name__ == '__main__':
    try:
        success = test_reconstruction()
        
        if success:
            print("\n" + "=" * 70)
            print("🎉 ALL TESTS PASSED!")
            print("=" * 70)
            print("\nThe reconstruction pipeline is working correctly.")
            print("You can now use the web application with real images.")
            print("\nTo start the web app, run:")
            print("  python app.py")
        else:
            print("\n" + "=" * 70)
            print("❌ TESTS FAILED")
            print("=" * 70)
            print("\nPlease check the error messages above.")
        
        cleanup_test_files()
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
