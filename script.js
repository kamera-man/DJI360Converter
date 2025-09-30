class DJI360Converter {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.processingSection = document.getElementById('processingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        this.processingInfo = document.getElementById('processingInfo');
        this.imagesGrid = document.getElementById('imagesGrid');
        this.downloadAllBtn = document.getElementById('downloadAllBtn');
        this.resetBtn = document.getElementById('resetBtn');
        
        this.processedImages = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Upload area click
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });

        // Keyboard support for upload area
        this.uploadArea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.fileInput.click();
            }
        });

        // File input change
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(Array.from(e.target.files));
        });

        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            const files = Array.from(e.dataTransfer.files).filter(file => 
                file.type.startsWith('image/')
            );
            this.handleFiles(files);
        });

        // Reset button
        this.resetBtn.addEventListener('click', () => {
            this.reset();
        });

        // Download all button
        this.downloadAllBtn.addEventListener('click', () => {
            this.downloadAll();
        });
    }

    showError(message) {
        // Create or update error message element
        let errorDiv = document.getElementById('errorMessage');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'errorMessage';
            errorDiv.className = 'error-message';
            this.uploadArea.parentNode.insertBefore(errorDiv, this.uploadArea.nextSibling);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Hide error after 5 seconds
        setTimeout(() => {
            if (errorDiv) {
                errorDiv.style.display = 'none';
            }
        }, 5000);
    }

    hideError() {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }

    handleFiles(files) {
        this.hideError(); // Clear any previous errors
        
        if (files.length === 0) {
            this.showError('Please select at least one image file.');
            return;
        }

        // Validate file types and sizes
        const maxFileSize = 50 * 1024 * 1024; // 50MB limit
        const supportedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff', 'image/tif'];
        const validFiles = [];
        const errors = [];

        for (const file of files) {
            if (!supportedTypes.includes(file.type.toLowerCase())) {
                errors.push(`${file.name}: Unsupported file type. Please use JPEG, PNG, or TIFF.`);
                continue;
            }
            if (file.size > maxFileSize) {
                errors.push(`${file.name}: File too large. Maximum size is 50MB.`);
                continue;
            }
            validFiles.push(file);
        }

        if (errors.length > 0) {
            this.showError('Some files could not be processed:\n\n' + errors.join('\n'));
        }

        if (validFiles.length === 0) {
            return;
        }

        console.log(`Processing ${validFiles.length} files:`, validFiles.map(f => f.name));
        this.showProcessingSection();
        this.processImages(validFiles);
    }

    showProcessingSection() {
        this.processingSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
        this.updateProgress(0, 'Initializing conversion...');
    }

    updateProgress(percentage, info) {
        this.progressFill.style.width = `${percentage}%`;
        this.progressText.textContent = `${Math.round(percentage)}%`;
        this.processingInfo.textContent = info;
    }

    async processImages(files) {
        this.processedImages = [];
        const totalFiles = files.length;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const progress = ((i / totalFiles) * 90); // Reserve 10% for finalization
            
            this.updateProgress(progress, `Processing ${file.name}...`);

            try {
                const processedImage = await this.convertImage(file);
                this.processedImages.push(processedImage);
            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);
                this.showError(`Error processing ${file.name}: ${error.message}`);
            }
        }

        this.updateProgress(100, 'Conversion complete!');
        
        setTimeout(() => {
            this.showResults();
        }, 500);
    }

    async convertImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = async (e) => {
                const img = new Image();
                img.onload = async () => {
                    try {
                        const result = await this.processImageForFacebook(img, file);
                        resolve(result);
                    } catch (error) {
                        reject(error);
                    }
                };
                img.onerror = () => reject(new Error('Failed to load image'));
                img.src = e.target.result;
            };
            reader.onerror = () => reject(new Error('Failed to read file'));
            reader.readAsDataURL(file);
        });
    }

    processImageForFacebook(img, originalFile) {
        // Create canvas for processing
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        // Facebook optimal dimensions for 360 images
        const maxWidth = 2048;
        const maxHeight = 1024;
        
        // Calculate optimal dimensions maintaining aspect ratio
        let { width, height } = this.calculateOptimalSize(
            img.width, 
            img.height, 
            maxWidth, 
            maxHeight
        );

        canvas.width = width;
        canvas.height = height;

        // Apply Facebook-optimized processing
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, width, height);

        // Draw image with proper scaling
        ctx.drawImage(img, 0, 0, width, height);

        // Apply enhancement filters for social media
        this.applyFacebookOptimization(ctx, width, height);

        // Convert to blob
        return new Promise((resolve, reject) => {
            canvas.toBlob((blob) => {
                if (!blob) {
                    reject(new Error('Failed to process image to blob'));
                    return;
                }
                const url = URL.createObjectURL(blob);
                resolve({
                    originalName: originalFile.name,
                    processedName: this.generateProcessedName(originalFile.name),
                    url: url,
                    blob: blob,
                    originalSize: originalFile.size,
                    processedSize: blob.size,
                    dimensions: `${width}x${height}`,
                    originalDimensions: `${img.width}x${img.height}`
                });
            }, 'image/jpeg', 0.9); // High quality JPEG for Facebook
        });
    }

    calculateOptimalSize(originalWidth, originalHeight, maxWidth, maxHeight) {
        // For 360 images, prefer 2:1 aspect ratio
        let targetRatio = 2;
        
        if (originalWidth / originalHeight > targetRatio) {
            // Image is wider than target ratio
            let width = Math.min(originalWidth, maxWidth);
            let height = width / targetRatio;
            
            if (height > maxHeight) {
                height = maxHeight;
                width = height * targetRatio;
            }
            
            return { width: Math.round(width), height: Math.round(height) };
        } else {
            // Image is taller than target ratio or equal
            let height = Math.min(originalHeight, maxHeight);
            let width = height * targetRatio;
            
            if (width > maxWidth) {
                width = maxWidth;
                height = width / targetRatio;
            }
            
            return { width: Math.round(width), height: Math.round(height) };
        }
    }

    applyFacebookOptimization(ctx, width, height) {
        // Apply subtle sharpening and contrast enhancement
        // This simulates the processing that would make images more social media friendly
        
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;

        // Simple contrast and brightness adjustment
        const contrast = 1.1;
        const brightness = 5;

        for (let i = 0; i < data.length; i += 4) {
            // Red
            data[i] = Math.min(255, Math.max(0, (data[i] - 128) * contrast + 128 + brightness));
            // Green
            data[i + 1] = Math.min(255, Math.max(0, (data[i + 1] - 128) * contrast + 128 + brightness));
            // Blue
            data[i + 2] = Math.min(255, Math.max(0, (data[i + 2] - 128) * contrast + 128 + brightness));
        }

        ctx.putImageData(imageData, 0, 0);
    }

    generateProcessedName(originalName) {
        const nameWithoutExt = originalName.replace(/\.[^/.]+$/, "");
        return `${nameWithoutExt}_facebook_optimized.jpg`;
    }

    showResults() {
        this.processingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
        this.displayProcessedImages();
    }

    displayProcessedImages() {
        this.imagesGrid.innerHTML = '';

        this.processedImages.forEach((image, index) => {
            const imageResult = document.createElement('div');
            imageResult.className = 'image-result fade-in';
            
            imageResult.innerHTML = `
                <img src="${image.url}" alt="${image.processedName}">
                <div class="image-info">
                    <h4>${image.processedName}</h4>
                    <p>Original: ${image.originalDimensions} (${this.formatFileSize(image.originalSize)})</p>
                    <p>Optimized: ${image.dimensions} (${this.formatFileSize(image.processedSize)})</p>
                    <button class="btn btn-primary" onclick="converter.downloadImage(${index})">
                        Download
                    </button>
                </div>
            `;

            this.imagesGrid.appendChild(imageResult);
        });
    }

    downloadImage(index) {
        const image = this.processedImages[index];
        const link = document.createElement('a');
        link.href = image.url;
        link.download = image.processedName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    downloadAll() {
        this.processedImages.forEach((image, index) => {
            setTimeout(() => {
                this.downloadImage(index);
            }, index * 100); // Small delay between downloads
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    reset() {
        // Clear processed images and URLs to prevent memory leaks
        this.processedImages.forEach(image => {
            if (image.url.startsWith('blob:')) {
                URL.revokeObjectURL(image.url);
            }
        });
        
        this.processedImages = [];
        this.fileInput.value = '';
        this.processingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.imagesGrid.innerHTML = '';
        this.updateProgress(0, '');
    }
}

// Initialize the converter when the page loads
let converter;
document.addEventListener('DOMContentLoaded', () => {
    converter = new DJI360Converter();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (converter && converter.processedImages) {
        converter.processedImages.forEach(image => {
            if (image.url.startsWith('blob:')) {
                URL.revokeObjectURL(image.url);
            }
        });
    }
});