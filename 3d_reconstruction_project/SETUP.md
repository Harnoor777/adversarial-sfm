# Setup Instructions

## Quick Start

### 1. Install Dependencies

Run this command to install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web server)
- opencv-python (computer vision)
- open3d (3D processing)
- numpy (numerical operations)
- Pillow (image handling)
- trimesh (mesh utilities)

### 2. Verify Installation

Test that everything is installed correctly:

```bash
python -c "import cv2; import open3d; import numpy; print('✅ All packages installed successfully!')"
```

### 3. Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

## Troubleshooting Installation

### Issue: opencv-python fails to install

**Solution**: Try installing build tools first:

**Windows**:
```bash
pip install --upgrade pip setuptools wheel
pip install opencv-python
```

**Linux/Mac**:
```bash
sudo apt-get install python3-dev  # Ubuntu/Debian
pip install opencv-python
```

### Issue: open3d fails to install

**Solution**: Ensure you have Python 3.7-3.11 (Open3D doesn't support 3.12 yet)

Check your Python version:
```bash
python --version
```

If needed, create a virtual environment with Python 3.11:
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Issue: "No module named 'cv2'" when running

**Solution**: Make sure you're using the same Python that has the packages:
```bash
python -m pip install -r requirements.txt
python app.py
```

## System Requirements

- **Python**: 3.7 - 3.11 (3.11 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core processor recommended
- **Storage**: 500MB for dependencies + space for models
- **OS**: Windows 10/11, Linux, or macOS

## Testing the Reconstruction

1. Prepare 5-10 photos of an object from different angles
2. Upload them via the web interface
3. Click "Start Reconstruction"
4. Wait 10-30 seconds for processing
5. Download the generated .ply model

## Performance Tips

- **Reduce image size**: Large images (>2MB) will be auto-resized
- **Optimal image count**: 5-10 images work best
- **Good overlap**: Each photo should share 60-70% with the next
- **Textured objects**: Plain surfaces are difficult to reconstruct

## Next Steps

After successful setup:
1. Read the main **README.md** for usage instructions
2. Try reconstructing a simple textured object
3. View the output .ply file in MeshLab or Blender
4. Experiment with different objects and camera angles

---

**Need Help?** Check the Troubleshooting section in README.md
