# 3D Reconstruction Studio

A web-based application for generating 3D models from multiple images using Structure-from-Motion (SfM) and point cloud reconstruction.

## Features

- 🎯 **Real 3D Reconstruction**: Uses OpenCV and Open3D for actual SfM pipeline
- 🚀 **Futuristic UI**: Holographic hero section with particle effects
- 🌓 **Dark/Light Mode**: Theme toggle with localStorage persistence
- 📤 **Drag & Drop Upload**: Easy image upload with preview thumbnails
- 📊 **Live Progress**: Real-time reconstruction pipeline visualization
- 💾 **Download Models**: Export reconstructed 3D models as .ply files
- 🔒 **100% Local**: No cloud services, all processing on your machine

## Technology Stack

### Backend
- Python 3.11
- Flask (web server)
- OpenCV (feature detection & matching)
- Open3D (point cloud & mesh generation)
- NumPy (numerical operations)

### Frontend
- HTML5 / CSS3
- Vanilla JavaScript
- Canvas API (particle effects)
- Glassmorphism design

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Open your browser**:
Navigate to `http://localhost:5000`

## Usage

### Taking Photos for Best Results

For optimal 3D reconstruction:

1. **Take 5-10 photos** of your object from different angles
2. **Move around the object** in a circular pattern
3. **Keep consistent lighting** across all photos
4. **Overlap between views**: Each photo should share ~60-70% content with the next
5. **Avoid motion blur**: Keep the camera steady
6. **Use good resolution**: 1-4 megapixels is sufficient

### Reconstruction Process

1. **Upload Images**: Drag and drop or click to select 5-10 images
2. **Start Reconstruction**: Click "Start Reconstruction" button
3. **Wait for Processing**: Watch the pipeline progress through 6 steps:
   - 📸 Loading images
   - 🔍 Detecting features (SIFT/ORB)
   - 🔗 Matching features between pairs
   - 📐 Estimating camera poses & structure
   - ☁️ Creating point cloud
   - 🔷 Generating triangle mesh
4. **Download Model**: Click "Download Model" to get your .ply file

### Viewing 3D Models

The output `.ply` files can be viewed in:
- **MeshLab** (free, cross-platform)
- **Blender** (free, powerful 3D software)
- **CloudCompare** (free, point cloud viewer)
- **Windows 3D Viewer** (built-in on Windows 10/11)
- **Online viewers**: https://3dviewer.net/

## How It Works

### Structure-from-Motion Pipeline

1. **Feature Detection**: Detects SIFT or ORB keypoints in each image
2. **Feature Matching**: Matches keypoints between consecutive image pairs using ratio test
3. **Essential Matrix**: Estimates camera motion between views
4. **Pose Recovery**: Recovers rotation and translation between cameras
5. **Triangulation**: Computes 3D positions of matched points
6. **Point Cloud**: Creates colored 3D point cloud from triangulated points
7. **Mesh Generation**: Uses Poisson surface reconstruction to create triangle mesh

### Performance Optimization

- Images automatically resized to 800px width for faster processing
- Statistical outlier removal for cleaner point clouds
- Optimized for 5-10 images on laptop CPU
- Processing time: ~10-30 seconds depending on image count and resolution

## Project Structure

```
3d_reconstruction_project/
├── app.py                      # Flask server
├── reconstruction.py           # 3D reconstruction pipeline
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main webpage
├── static/
│   ├── css/
│   │   └── style.css          # Futuristic UI styles
│   └── js/
│       └── script.js          # Frontend logic & animations
├── uploads/                    # Temporary image storage
└── output/                     # Generated 3D models (.ply)
```

## Troubleshooting

### "Need at least 2 images for reconstruction"
- Upload at least 2 images (5-10 recommended)

### "Not enough good matches"
- Ensure images have sufficient overlap
- Use better lighting and avoid motion blur
- Try different angles around the object

### Poor reconstruction quality
- Take more photos (8-10 is ideal)
- Increase overlap between consecutive views
- Ensure consistent lighting
- Avoid reflective or transparent objects
- Use textured objects (plain surfaces are difficult)

### SIFT not available
- The app will automatically fall back to ORB
- For better results, install opencv-contrib-python:
  ```bash
  pip uninstall opencv-python
  pip install opencv-contrib-python
  ```

## Limitations

- Works best with **textured objects** (not plain/uniform surfaces)
- Requires **good lighting** and **minimal motion blur**
- **Small to medium objects** work best
- Processing is **CPU-intensive** (10-30 seconds per reconstruction)
- Not suitable for **transparent, reflective, or very dark objects**

## Future Enhancements

- [ ] Real-time 3D viewer in browser (Three.js)
- [ ] Multi-view stereo (MVS) for denser reconstruction
- [ ] GPU acceleration for faster processing
- [ ] Support for video input (extract frames automatically)
- [ ] Advanced mesh texturing
- [ ] Export to multiple formats (OBJ, STL, FBX)

## Academic Context

This is a **Final Year Computer Science Project** demonstrating:
- Computer Vision techniques (feature detection, matching)
- Structure-from-Motion algorithms
- 3D geometry and reconstruction
- Full-stack web development
- Modern UI/UX design

## License

This project is for educational purposes.

## Credits

- **OpenCV**: Feature detection and matching
- **Open3D**: Point cloud and mesh processing
- **Flask**: Web framework
- **Design**: Custom futuristic UI with glassmorphism

---

**Built with ❤️ for Computer Science Final Year Project**
