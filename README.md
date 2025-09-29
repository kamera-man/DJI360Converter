# DJI360Converter

A powerful web-based tool for converting DJI 360° images to Facebook-optimized format. This tool provides both a user-friendly web interface and a command-line tool for processing 360° images to ensure they display perfectly on Facebook and other social media platforms.

## Features

- **Web Interface**: Drag-and-drop web interface for easy image conversion
- **Batch Processing**: Process multiple images at once
- **Facebook Optimization**: Automatically optimizes images for Facebook's 360° image requirements
- **Smart Resizing**: Maintains optimal 2:1 aspect ratio for 360° content
- **Quality Enhancement**: Applies contrast and sharpening for better social media appearance
- **Client-Side Processing**: Web interface processes images locally for privacy
- **Command Line Tool**: Python script for advanced processing and automation

## Quick Start

### Web Interface

1. **Start the server**:
   ```bash
   python3 server.py
   ```

2. **Open your browser** to `http://localhost:8000`

3. **Upload your DJI 360° images** using drag-and-drop or the file picker

4. **Download the optimized images** ready for Facebook posting

### Command Line Tool

1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Process a single image**:
   ```bash
   python3 dji360_converter.py your_image.jpg
   ```

3. **Process multiple images**:
   ```bash
   python3 dji360_converter.py /path/to/images/ --batch
   ```

## Installation

### Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kamera-man/DJI360Converter.git
   cd DJI360Converter
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 server.py
   ```

## Usage

### Web Interface

The web interface provides an intuitive way to convert your DJI 360° images:

1. **Upload Images**: Drag and drop your images or click to browse
2. **Automatic Processing**: Images are processed client-side for privacy
3. **Preview Results**: See before/after comparisons with file size information
4. **Download**: Get your Facebook-optimized images instantly

### Command Line Interface

The CLI tool offers advanced options for power users:

```bash
# Basic usage
python3 dji360_converter.py input_image.jpg

# Specify output file
python3 dji360_converter.py input.jpg -o output.jpg

# Process all images in a directory
python3 dji360_converter.py /path/to/images/ --batch -o /path/to/output/

# Adjust quality (1-100, default: 90)
python3 dji360_converter.py input.jpg -q 95

# Get JSON output for scripting
python3 dji360_converter.py input.jpg --json
```

## Optimization Features

### Facebook-Specific Optimizations

- **Aspect Ratio**: Converts to optimal 2:1 aspect ratio for 360° content
- **Resolution**: Resizes to Facebook's recommended maximum of 2048x1024
- **Quality**: Applies high-quality JPEG compression (90% default)
- **Enhancement**: Subtle sharpening and contrast enhancement for mobile viewing

### Technical Details

- **Format**: Converts to JPEG for optimal Facebook compatibility
- **Color Space**: Ensures RGB color space for proper display
- **Compression**: Optimized compression to balance quality and file size
- **Metadata**: Preserves important image metadata where possible

## File Structure

```
DJI360Converter/
├── index.html          # Main web interface
├── styles.css          # Web interface styling
├── script.js           # Client-side JavaScript
├── dji360_converter.py # Python processing engine
├── server.py           # Local web server
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Privacy & Security

- **Client-Side Processing**: The web interface processes images entirely in your browser
- **No Upload Required**: Images never leave your device when using the web interface
- **Local Server**: All processing happens locally on your machine

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation above

## Changelog

### v1.0.0
- Initial release with web interface
- Command-line tool for batch processing
- Facebook optimization algorithms
- Client-side image processing
- Drag-and-drop interface
