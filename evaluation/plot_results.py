import matplotlib.pyplot as plt
import numpy as np

# Your experimental results
epsilons = [0.01, 0.02, 0.03, 0.05]
chamfer_distances = [15.74, 90.50, 36.05, 6.69]
point_counts = [1923, 1607, 2768, 2296]
clean_points = 1639

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- Plot 1: Chamfer Distance vs Epsilon ---
ax1.plot(epsilons, chamfer_distances, 'ro-', linewidth=2, markersize=8)
ax1.axhline(y=0, color='green', linestyle='--', label='Clean baseline (0)')
ax1.set_xlabel('Epsilon (perturbation strength)', fontsize=12)
ax1.set_ylabel('Chamfer Distance', fontsize=12)
ax1.set_title('Reconstruction Damage vs Attack Strength', fontsize=13)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Annotate peak
ax1.annotate('Peak damage\nat ε=0.02', 
             xy=(0.02, 90.50), 
             xytext=(0.03, 85),
             arrowprops=dict(arrowstyle='->', color='black'),
             fontsize=10)

# --- Plot 2: Point Count vs Epsilon ---
ax2.bar(epsilons, point_counts, width=0.008, 
        color='steelblue', alpha=0.7, label='Attacked')
ax2.axhline(y=clean_points, color='green', 
            linestyle='--', linewidth=2, label=f'Clean baseline ({clean_points})')
ax2.set_xlabel('Epsilon (perturbation strength)', fontsize=12)
ax2.set_ylabel('Reconstructed Point Count', fontsize=12)
ax2.set_title('Point Cloud Density vs Attack Strength', fontsize=13)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.suptitle('FGSM Attack Impact on Structure-from-Motion Pipeline', 
             fontsize=14, fontweight='bold')
plt.tight_layout()

# Save
output_path = r"E:\adversarial-sfm\results\attack_results.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Graph saved to {output_path}")
plt.show()