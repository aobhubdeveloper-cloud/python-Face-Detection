# Face Photo Utility - Professional Image Capture System

A comprehensive Python-based face photo capture application with real-time face detection, automatic enhancement, and MS Access integration.

## Features

### 🎯 Core Functionality
- **Real-time Face Detection**: Uses OpenCV Haar Cascades for accurate face and eye detection
- **Auto-Capture Mode**: Automatically captures the best quality photo when face is detected
- **Manual Capture**: Click-to-capture functionality for manual control
- **Dual Output**: Saves both color and grayscale versions simultaneously

### 📸 Image Processing
- **Background Replacement**: White, Light Gray, Dark Gray, Light Blue options
- **Auto-Enhancement**: Automatic brightness, contrast, and sharpness adjustment
- **Quality Control**: Adjustable JPEG/PNG compression settings
- **Smart Cropping**: Intelligent face cropping with proper aspect ratio

### 🖥️ User Interface
- **Live Preview**: Real-time webcam feed with face detection overlay
- **Dual Preview**: Side-by-side color and grayscale previews
- **Dark/Light Theme**: Toggle between interface themes
- **Responsive Layout**: Optimized for different screen sizes

### 🔗 Integration
- **MS Access Compatible**: Seamless integration with database applications
- **Command Line Support**: Can be launched with parameters
- **Path Management**: Robust file path handling and validation
- **Clipboard Integration**: Automatic path copying to clipboard

## Installation

### Prerequisites
```bash
pip install opencv-python numpy pillow pyperclip
```

### Files Required
- `face-utility.py` - Main application
- `working.py` - Alternative version
- Haar cascade XML files (included with OpenCV)

## Usage

### Standalone Mode
```bash
python face-utility.py
```

### MS Access Integration
```bash
python face-utility.py "C:\Photos" "employee_photo.jpg"
```

### VBA Integration
```vba
Private Sub CapturePhoto_Click()
    Dim cmd As String
    cmd = "python face-utility.py """ & photoPath & """ """ & filename & """"
    Shell cmd, vbNormalFocus
End Sub
```

## Interface Guide

### Main Controls
- **File Path**: Directory where photos will be saved
- **Filename**: Name for the captured photo
- **Browse**: Select save directory
- **RETAKE**: Clear current capture and start over
- **Auto-Capture**: Enable automatic photo capture

### Capture Process
1. **Position Face**: Align face within the yellow guideline box
2. **Wait for Detection**: Green rectangle appears around detected face
3. **Auto-Capture**: Photo automatically taken after 3-second countdown
4. **Manual Capture**: Click on detected face to capture immediately
5. **Save**: Click on color or grayscale preview to save

### Settings
- **Background**: Choose background color for photos
- **Format**: Select JPEG or PNG output format
- **Quality**: Adjust compression level (0-100)
- **Theme**: Toggle between dark and light interface

## Technical Specifications

### Image Processing
- **Input Resolution**: Webcam native resolution
- **Output Size**: 200x250 pixels (standard ID photo size)
- **Supported Formats**: JPEG, PNG
- **Color Modes**: RGB color, Grayscale
- **Enhancement**: Auto brightness/contrast adjustment

### Face Detection
- **Algorithm**: OpenCV Haar Cascade Classifiers
- **Detection Models**: Frontal face and eye detection
- **Quality Scoring**: Centering, size, and feature detection
- **Auto-Enhancement**: Pre-capture frame optimization

### System Requirements
- **Python**: 3.7 or higher
- **Webcam**: Any USB or built-in camera
- **OS**: Windows, macOS, Linux
- **Memory**: 512MB RAM minimum
- **Storage**: 50MB free space

## Configuration

### Logging
Logs are automatically saved to `face_utility.log` with:
- Application startup/shutdown events
- Error tracking and debugging info
- System information and version details

### Customization
Key parameters can be modified in the code:
```python
# Window size
self.root.geometry("1200x650")

# Face detection parameters
faces = self.face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
)

# Auto-capture timing
countdown = 3 - int(elapsed)  # 3-second countdown
```

## Troubleshooting

### Common Issues
- **Camera Not Found**: Check webcam connection and permissions
- **Face Not Detected**: Ensure good lighting and face visibility
- **Save Path Error**: Verify directory exists and has write permissions
- **Import Errors**: Install required Python packages

### Error Logs
Check `face_utility.log` for detailed error information and debugging data.

### Performance Tips
- Use good lighting for better face detection
- Position face within the guideline box
- Ensure stable internet connection for package updates
- Close other camera applications before running

## MS Access Integration

### VBA Code Example
```vba
Private Sub Command398_Click()
    Dim wsh As Object
    Dim cmd As String
    Dim photoPath As String
    Dim filename As String
    
    photoPath = Me.txtImagePath.Value
    filename = Me.txtImageName.Value
    
    ' Remove trailing backslash
    If Right(photoPath, 1) = "\" Then
        photoPath = Left(photoPath, Len(photoPath) - 1)
    End If
    
    cmd = "python face-utility.py """ & photoPath & """ """ & filename & """"
    
    Set wsh = CreateObject("WScript.Shell")
    wsh.Run cmd, 1, True  ' Wait for completion
    
    ' Display captured image
    If Dir(photoPath & "\" & filename) <> "" Then
        Me.imgPhoto.Picture = photoPath & "\" & filename
        MsgBox "Photo captured successfully!"
    End If
End Sub
```

## License

This project is provided as-is for educational and professional use.

## Support

For issues and questions:
1. Check the log file for error details
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Test with different lighting conditions