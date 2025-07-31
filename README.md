# Face Photo Utility - Professional Image Capture System

A comprehensive Python-based face photo capture application with real-time face detection, automatic enhancement, and MS Access integration.

## Features

### 🎯 Core Functionality
- **Real-time Face Detection**: Uses OpenCV Haar Cascades for accurate face and eye detection
- **Auto-Capture Mode**: Automatically captures the best quality photo when face is detected
- **Auto-Save & Close**: Automatically saves images after capture and closes app when configured
- **Manual Capture**: Click-to-capture functionality for manual control
- **Dual Output**: Saves both color and grayscale versions simultaneously
- **Grayscale-Only Mode**: Option to save only grayscale images for specific workflows
- **Audio Feedback**: System beep notifications for capture events and alerts

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
- **Audio Notifications**: Beep sounds for successful captures and system alerts

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

### Command Line Parameters
```bash
# Basic usage with path and filename
python face.py "C:\Photos" "employee.jpg"

# Save only grayscale version (auto-saves and closes)
python face.py "C:\Photos" "employee.jpg" grayscale

# Manual auto-close control
python face.py "C:\Photos" "employee.jpg" grayscale autoclose

# Save both color and grayscale versions
python face.py "C:\Photos" "employee.jpg"
```

### Parameter Options
- **save_path**: Directory where images will be saved
- **filename**: Name for the captured image file
- **grayscale**: (Optional) Save only grayscale version and auto-close
- **autoclose**: (Optional) Close application automatically after saving

### MS Access Integration
```bash
python face-utility.py "C:\Photos" "employee_photo.jpg"
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
3. **Auto-Capture**: Photo automatically taken after 3-second countdown with beep confirmation
4. **Auto-Save**: Images automatically saved after capture (both color and grayscale by default)
5. **Manual Capture**: Click on detected face to capture immediately with beep feedback
6. **Manual Save**: Click on color or grayscale preview to save specific version
7. **Auto-Close**: Application closes automatically when configured (grayscale mode + MS Access)

### Automated Workflow (Grayscale Mode)
- Face detection → Auto-capture → Auto-save grayscale → Success message → Auto-close

### Settings
- **Background**: Choose background color for photos
- **Format**: Select JPEG or PNG output format
- **Quality**: Adjust compression level (0-100)
- **Theme**: Toggle between dark and light interface
- **Audio Feedback**: System beep notifications enabled by default

## Advanced Features

### Auto-Save Modes

#### Default Mode (Both Versions)
```bash
python face.py "C:\Photos" "employee.jpg"
```
- Saves both color and grayscale versions
- Files: `employee_color.jpg` and `employee_gray.jpg`
- User can still click previews to save manually
- Application stays open for additional captures

#### Grayscale-Only Mode
```bash
python face.py "C:\Photos" "employee.jpg" grayscale
```
- Saves only grayscale version as `employee.jpg`
- Automatically closes after saving
- Shows success message with file location
- Ideal for MS Access integration

#### Manual Auto-Close
```bash
python face.py "C:\Photos" "employee.jpg" grayscale autoclose
```
- Explicit control over auto-close behavior
- Can be combined with any save mode

### Integration Modes

#### MS Access Integration (from_access=True)
- Forces JPEG format regardless of user selection
- Performs automatic path cleanup
- Returns saved file path for VBA integration
- Handles MS Access-specific filename formatting

#### Standalone Mode (from_access=False)
- Full user control over format (JPEG/PNG)
- Uses filename exactly as provided
- No special path processing
- Interactive GUI mode

### Command Reference

| Command | Behavior | Output Files | Auto-Close |
|---------|----------|--------------|------------|
| `python face.py "path" "file.jpg"` | Save both versions | `file_color.jpg`, `file_gray.jpg` | No |
| `python face.py "path" "file.jpg" grayscale` | Save grayscale only | `file.jpg` | Yes |
| `python face.py "path" "file.jpg" grayscale autoclose` | Save grayscale only | `file.jpg` | Yes |
| Interactive GUI (no params) | Manual save via clicks | User choice | No |

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

# Audio feedback
import winsound  # For Windows beep sounds
winsound.Beep(800, 200)  # Frequency 800Hz, Duration 200ms
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

### VBA Integration
```vba
Private Sub CaptureImage_Click()

Dim BIFolder As String
    Dim fileName As String
    Dim BIOutName As String
    Dim txtSubject As String
    Dim resultPath As String
    
    ' Build the folder structure
    BIFolder = Application.CurrentProject.path & "\Movement Orders\" & _
        Nz(Me.TextCarrigeComp.value, "") & "\" & _
        Nz(Me.TextCompany.value, "") & "\" & _
        Nz(Me.LoadFld.value, "") & " - " & Nz(Me.DecRef.value, "") & "\LivePictures\"
    
    ' Ensure the folder exists
     PathCreator BIFolder
    
    ' Build the filename
    txtSubject = "Dated_" & Format(Me.TextOrderDate.value, "DD-MMMM-YYYY") & "," & CStr(Me.TextBowzer.value) & "," & CStr(Me.LoadFld.value) & _
        "-" & CStr(Me.DecRef.value) & "," & CStr(Me.TextDrv1.value)
    
    fileName = txtSubject & ".jpg"
    BIOutName = BIFolder & fileName

    ' Call webcam capture form and get result
    resultPath = CaptureImageAndReturnPath(BIFolder, fileName)

    If resultPath <> "" And Len(Dir(resultPath)) > 0 Then
       Me.DriverLivePicture.value = resultPath
        Me.DriverImage.Picture = DriverLivePicture
        Me.DriverImage.Requery
        Me.BtnSave.Enabled = True
       
    Else
        MsgBox "Image capture cancelled or failed."
        Me.BtnSave.Enabled = False
    End If
    
End Sub
```

### VBA Code Example
```vba
Public Function CaptureImageAndReturnPath(ByVal folderPath As String, ByVal fileName As String) As String

 On Error GoTo ErrorHandler

    Dim projectPath As String
    Dim pythonPath As String
    Dim scriptPath As String
    Dim photoFolder As String
    Dim photoFileName As String
    Dim commandLine As String
    Dim fullPhotoPath As String
     Dim shellObj As Object

    ' Define values (adjust based on your setup)
    projectPath = CStr(Application.CurrentProject.path) & "\scripts"
    pythonPath = projectPath & "\.venv\Scripts\python.exe"
    scriptPath = projectPath & "\face-uitlity.py"
    photoFolder = IIf(Right(CStr(folderPath), 1) = "\", Left(CStr(folderPath), Len(CStr(folderPath)) - 1), CStr(folderPath))
    photoFileName = CStr(fileName)       ' Or use txtImageName.Value

'    fullPhotoPath = photoFolder & photoFileName
    
    ' Construct command for different modes:
    
    ' Standard mode (saves both color and grayscale)
    commandLine = "cmd /c """ & _
        """" & pythonPath & """" & " " & _
        """" & scriptPath & """" & " " & _
        """" & photoFolder & """" & " " & _
        """" & photoFileName & """" & """"
    
    ' Grayscale-only mode (auto-saves and closes)
    ' commandLine = "cmd /c """ & _
    '     """" & pythonPath & """" & " " & _
    '     """" & scriptPath & """" & " " & _
    '     """" & photoFolder & """" & " " & _
    '     """" & photoFileName & """" & " grayscale""""

      ' Debug Print to check
    Debug.Print commandLine

'      Run without showing the command window
    Set shellObj = CreateObject("WScript.Shell")
    shellObj.Run commandLine, 0, True   ' 0 = hidden window, False = don't wait

    ' Check if file exists
    If Dir(fullPhotoPath) <> "" Then
    DoCmd.Beep
    MsgBox "Image created successfully!", vbInformation
    CaptureImageAndReturnPath = NormalizePath(folderPath & "\" & fileName)
    Else
        MsgBox "Image not found at: " & fullPhotoPath, vbExclamation
    End If

    Exit Function

ErrorHandler:
    MsgBox "Error: " & Err.Description, vbCritical
End Function
```

## License

This project is provided as-is for educational and professional use.

## Support

For issues and questions:
1. Check the log file for error details
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Test with different lighting conditions