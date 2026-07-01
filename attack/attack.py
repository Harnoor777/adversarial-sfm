import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def apply_fgsm(image, epsilon=0.02):
    """
    Apply FGSM perturbation to an image.
    epsilon controls perturbation strength — higher = more damage but more visible.
    0.02 is a good starting point (nearly invisible to human eye)
    """
    image_float = image.astype(np.float32) / 255.0
    
    grad_x = cv2.Sobel(image_float, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image_float, cv2.CV_32F, 0, 1, ksize=3)
    
    perturbation = epsilon * (np.sign(grad_x) + np.sign(grad_y))
    
    perturbed = image_float + perturbation
    perturbed = np.clip(perturbed, 0, 1)
    perturbed = (perturbed * 255).astype(np.uint8)
    
    return perturbed

def process_folder(input_folder, output_folder, epsilon=0.02):
    """
    Process all images in a folder and save perturbed versions
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image formats
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    
    images = [f for f in os.listdir(input_folder) 
              if f.lower().endswith(valid_extensions)]
    
    if not images:
        print(f"No images found in {input_folder}")
        return
    
    print(f"Found {len(images)} images — processing...")
    
    for filename in images:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Load
        image = cv2.imread(input_path)
        if image is None:
            print(f"Skipping {filename} — could not load")
            continue
        
        # Perturb
        perturbed = apply_fgsm(image, epsilon=epsilon)
        
        # Save
        cv2.imwrite(output_path, perturbed)
        print(f"Saved perturbed: {filename}")
    
    print(f"\nDone. All perturbed images saved to {output_folder}")

def save_comparison(input_folder, output_folder, sample_filename):
    """
    Save a side by side comparison of one sample image
    """
    clean = cv2.imread(os.path.join(input_folder, sample_filename))
    perturbed = cv2.imread(os.path.join(output_folder, sample_filename))
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Clean Image')
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(perturbed, cv2.COLOR_BGR2RGB))
    axes[1].set_title('Perturbed Image (FGSM)')
    axes[1].axis('off')
    
    diff = np.abs(clean.astype(np.float32) - perturbed.astype(np.float32))
    diff_amplified = np.clip(diff * 10, 0, 255).astype(np.uint8)
    axes[2].imshow(cv2.cvtColor(diff_amplified, cv2.COLOR_BGR2RGB))
    axes[2].set_title('Difference x10')
    axes[2].axis('off')
    
    plt.tight_layout()
    
    comparison_path = os.path.join(
        r"E:\adversarial-sfm\results", 
        "comparison.png"
    )
    plt.savefig(comparison_path)
    print(f"Comparison saved to {comparison_path}")
    plt.show()

def main():
    # --- Input folder: your clean images ---
    input_folder = r"E:\adversarial-sfm\clean_images"
    
    # --- Output folder: perturbed images saved here ---
    output_folder = r"E:\adversarial-sfm\results\perturbed_eps003"
    
    # Process all images
    process_folder(input_folder, output_folder, epsilon=0.03)
    
    # Save comparison using first image as sample
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    images = [f for f in os.listdir(input_folder) 
              if f.lower().endswith(valid_extensions)]
    
    if images:
        save_comparison(input_folder, output_folder, images[0])

if __name__ == "__main__":
    main()