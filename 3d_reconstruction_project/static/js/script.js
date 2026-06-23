// Theme Management
const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'dark';
if (savedTheme === 'light') {
    body.setAttribute('data-theme', 'light');
    themeSwitch.checked = true;
}

themeSwitch.addEventListener('change', () => {
    if (themeSwitch.checked) {
        body.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    } else {
        body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
    }
});

// File Upload Management
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const previewContainer = document.getElementById('previewContainer');
const previewGrid = document.getElementById('previewGrid');
const uploadBtn = document.getElementById('uploadBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const statusSection = document.getElementById('statusSection');
const statusIcon = document.getElementById('statusIcon');
const statusTitle = document.getElementById('statusTitle');
const statusMessage = document.getElementById('statusMessage');
const progressBar = document.getElementById('progressBar');
const progressFill = document.getElementById('progressFill');
const outputSection = document.getElementById('outputSection');
const modelFilename = document.getElementById('modelFilename');
const downloadBtn = document.getElementById('downloadBtn');

let selectedFiles = [];
let currentModelFilename = null;

// Browse button click
browseBtn.addEventListener('click', () => {
    fileInput.click();
});

// Upload zone click
uploadZone.addEventListener('click', (e) => {
    if (e.target !== browseBtn) {
        fileInput.click();
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

// Drag and drop
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('drag-over');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
});

// Handle selected files
function handleFiles(files) {
    const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
    
    if (imageFiles.length === 0) {
        showStatus('error', 'No Images', 'Please select valid image files');
        return;
    }
    
    selectedFiles = imageFiles;
    displayPreviews();
    previewContainer.classList.add('active');
    showStatus('ready', 'Images Selected', `${selectedFiles.length} images ready for reconstruction`);
}

// Display image previews
function displayPreviews() {
    previewGrid.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="Preview ${index + 1}">
                <button class="remove-btn" onclick="removeImage(${index})">×</button>
            `;
            previewGrid.appendChild(previewItem);
        };
        
        reader.readAsDataURL(file);
    });
}

// Remove image from selection
window.removeImage = function(index) {
    selectedFiles.splice(index, 1);
    
    if (selectedFiles.length === 0) {
        previewContainer.classList.remove('active');
        fileInput.value = '';
        showStatus('ready', 'Ready', 'Upload images to begin reconstruction');
    } else {
        displayPreviews();
        showStatus('ready', 'Images Selected', `${selectedFiles.length} images ready for reconstruction`);
    }
};

// Upload and process images
uploadBtn.addEventListener('click', async () => {
    if (selectedFiles.length === 0) {
        showStatus('error', 'No Images', 'Please select images first');
        return;
    }
    
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('images', file);
    });
    
    // Show loading
    loadingOverlay.classList.add('active');
    showStatus('processing', 'Processing', 'Reconstructing 3D model from images...');
    progressBar.classList.add('active');
    
    // Animate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
    }, 300);
    
    // Simulate reconstruction steps
    const steps = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6'];
    const reconstructionSteps = document.getElementById('reconstructionSteps');
    reconstructionSteps.style.display = 'block';
    
    let currentStep = 0;
    const stepInterval = setInterval(() => {
        if (currentStep > 0) {
            const prevStep = document.getElementById(steps[currentStep - 1]);
            prevStep.classList.remove('active');
            prevStep.classList.add('completed');
            prevStep.querySelector('.step-status').textContent = '✅';
        }
        
        if (currentStep < steps.length) {
            const step = document.getElementById(steps[currentStep]);
            step.classList.add('active');
            currentStep++;
        }
    }, 2000);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        clearInterval(progressInterval);
        clearInterval(stepInterval);
        progressFill.style.width = '100%';
        
        // Mark all steps as completed
        steps.forEach(stepId => {
            const step = document.getElementById(stepId);
            step.classList.remove('active');
            step.classList.add('completed');
            step.querySelector('.step-status').textContent = '✅';
        });
        
        setTimeout(() => {
            loadingOverlay.classList.remove('active');
            
            if (result.success) {
                const details = result.reconstruction;
                const message = `Generated ${details.vertices || 0} vertices, ${details.triangles || 0} triangles from ${details.images_processed} images`;
                showStatus('success', 'Success!', message);
                
                // Update output section with new model
                if (result.model_filename) {
                    currentModelFilename = result.model_filename;
                    updateOutputSection(result.model_filename, details);
                }
                
                // Reset after success
                setTimeout(() => {
                    selectedFiles = [];
                    previewContainer.classList.remove('active');
                    fileInput.value = '';
                    progressBar.classList.remove('active');
                    progressFill.style.width = '0%';
                    reconstructionSteps.style.display = 'none';
                    
                    // Reset steps
                    steps.forEach(stepId => {
                        const step = document.getElementById(stepId);
                        step.classList.remove('active', 'completed');
                        step.querySelector('.step-status').textContent = '⏳';
                    });
                    
                    showStatus('ready', 'Ready', 'Upload images to begin reconstruction');
                }, 5000);
            } else {
                showStatus('error', 'Error', result.error || 'Upload failed');
                progressBar.classList.remove('active');
                progressFill.style.width = '0%';
                reconstructionSteps.style.display = 'none';
            }
        }, 500);
        
    } catch (error) {
        clearInterval(progressInterval);
        loadingOverlay.classList.remove('active');
        showStatus('error', 'Error', 'Failed to connect to server');
        progressBar.classList.remove('active');
        progressFill.style.width = '0%';
    }
});

// Update status display
function showStatus(type, title, message) {
    const icons = {
        ready: '⏳',
        processing: '⚙️',
        success: '✅',
        error: '❌'
    };
    
    statusIcon.textContent = icons[type] || '⏳';
    statusTitle.textContent = title;
    statusMessage.textContent = message;
    
    // Add animation
    statusSection.style.animation = 'none';
    setTimeout(() => {
        statusSection.style.animation = 'fadeInUp 0.5s ease';
    }, 10);
}

// Update output section with new model
function updateOutputSection(filename, details) {
    currentModelFilename = filename;
    modelFilename.textContent = filename;
    downloadBtn.disabled = false;
    
    // Update stats if available
    if (details) {
        const statsHtml = `
            <div class="stat-item">
                <span class="stat-icon">📊</span>
                <span class="stat-text">${details.vertices || 0} vertices</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">🔺</span>
                <span class="stat-text">${details.triangles || 0} triangles</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">☁️</span>
                <span class="stat-text">${details.points_generated || 0} points</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">✅</span>
                <span class="stat-text">Ready</span>
            </div>
        `;
        document.getElementById('modelStats').innerHTML = statsHtml;
    }
    
    // Show output section with animation
    outputSection.style.display = 'block';
    outputSection.style.animation = 'none';
    setTimeout(() => {
        outputSection.style.animation = 'fadeInUp 0.8s ease';
    }, 10);
}

// Download button handler
downloadBtn.addEventListener('click', () => {
    if (currentModelFilename) {
        window.location.href = `/download/${currentModelFilename}`;
        
        // Visual feedback
        downloadBtn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            downloadBtn.style.transform = 'scale(1)';
        }, 200);
    }
});

// Initial status
showStatus('ready', 'Ready', 'Upload images to begin reconstruction');

// ===== HERO SECTION EFFECTS =====

// Particle System
const canvas = document.getElementById('particlesCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const particleCount = 100;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * 0.5 - 0.25;
        this.opacity = Math.random() * 0.5 + 0.2;
    }
    
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        
        if (this.x > canvas.width) this.x = 0;
        if (this.x < 0) this.x = canvas.width;
        if (this.y > canvas.height) this.y = 0;
        if (this.y < 0) this.y = canvas.height;
    }
    
    draw() {
        ctx.fillStyle = `rgba(0, 212, 255, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Initialize particles
for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

// Animation loop
function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw connections
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 100) {
                ctx.strokeStyle = `rgba(0, 212, 255, ${0.2 * (1 - distance / 100)})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }
    
    // Update and draw particles
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });
    
    requestAnimationFrame(animateParticles);
}

animateParticles();

// Resize canvas on window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Parallax effect on mouse move
const heroSection = document.getElementById('heroSection');
const heroTitle = document.getElementById('heroTitle');
const heroSubtitle = document.getElementById('heroSubtitle');

document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    const moveX = (mouseX - 0.5) * 20;
    const moveY = (mouseY - 0.5) * 20;
    
    heroTitle.style.transform = `translate(${moveX}px, ${moveY}px)`;
    heroSubtitle.style.transform = `translate(${moveX * 0.5}px, ${moveY * 0.5}px)`;
});

// Scroll reveal animation
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe upload section
const uploadSection = document.querySelector('.upload-section');
if (uploadSection) {
    uploadSection.style.opacity = '0';
    uploadSection.style.transform = 'translateY(50px)';
    uploadSection.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    observer.observe(uploadSection);
}
