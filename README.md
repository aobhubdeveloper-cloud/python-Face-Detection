# Face Photo Utility - Professional Image Capture System

A comprehensive Python-based face photo capture application with real-time face detection, automatic enhancement, and MS Access integration.

## Features

### 🎯 Core Functionality
- **Real-time Face Detection**: Uses OpenCV Haar Cascades for accurate face and eye detection
- **Auto-Capture Mode**: Automatically captures the best quality photo when face is detected (3-second countdown)
- **Auto-Save & Close**: Automatically saves images after capture and closes app when configured
- **Manual Capture**: Click-to-capture functionality for manual control
- **Dual Output**: Saves both color and grayscale versions simultaneously
- **Grayscale-Only Mode**: Option to save only grayscale images for specific workflows
- **Audio Feedback**: System beep notifications for capture events and alerts
- **Smart Frame Evaluation**: Evaluates frame quality based on centering, eye detection, and brightness

### 📸 Image Processing
- **Background Replacement**: White, Light Gray, Dark Gray, Light Blue options
- **Auto-Enhancement**: Automatic brightness, contrast, and sharpness adjustment during capture
- **Quality Control**: Adjustable JPEG/PNG compression settings (0-100)
- **Smart Cropping**: Intelligent face cropping with proper aspect ratio (200x250 pixels)
- **Auto-Brightness**: Automatic brightness adjustment based on lighting conditions

### 🖥️ User Interface
- **Live Preview**: Real-time webcam feed with face detection overlay (640x480)
- **Dual Preview**: Side-by-side color and grayscale previews (250x300 each)
- **Dark/Light Theme**: Toggle between interface themes
- **Responsive Layout**: Fixed window size (1400x750) optimized for all controls
- **Audio Notifications**: System beep sounds for successful captures
- **Visual Feedback**: Countdown timer and success messages
- **Animated Borders**: Color-changing borders for visual appeal

### 🔗 Integration
- **MS Access Compatible**: Seamless integration with database applications
- **Command Line Support**: Can be launched with parameters
- **Path Management**: Robust file path handling and validation
- **Clipboard Integration**: Automatic path copying to clipboard
- **Directory Auto-Creation**: Automatically creates save directories if they don't exist

## Installation

### Prerequisites
```bash
pip install opencv-python numpy pillow pyperclip
```

### Files Required
- `face.py` - Main application
- Haar cascade XML files (included with OpenCV)
- Python virtual environment (recommended)

## Usage

### Standalone Mode
```bash
python face.py "C:\Photos" "employee.jpg"
```

### Command Line Parameters
```bash
# Basic usage with path and filename (saves both color and grayscale)
python face.py "C:\Photos" "employee.jpg"

# Save only grayscale version (auto-saves and closes)
python face.py "C:\Photos" "employee.jpg" grayscale

# Manual auto-close control
python face.py "C:\Photos" "employee.jpg" grayscale autoclose

# Silent mode (no success messages)
python face.py "C:\Photos" "employee.jpg" grayscale autoclose silent
```

### Parameter Options
1. **save_path**: Directory where images will be saved (required)
2. **filename**: Name for the captured image file (required)
3. **grayscale**: (Optional) Save only grayscale version and auto-close
4. **autoclose**: (Optional) Close application automatically after saving
5. **silent**: (Optional) Suppress success/error messages

### MS Access Integration
```bash
python face.py "C:\Photos" "employee_photo.jpg" grayscale
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
7. **Auto-Close**: Application closes automatically when configured (grayscale mode)

### Automated Workflow (Grayscale Mode)
- Face detection → 3-second countdown → Auto-capture → Auto-save grayscale → Success message (1 second) → Auto-close

### Frame Quality Evaluation
- **Centering Score**: Face position relative to frame center
- **Size Score**: Face size relative to frame (prefers closer faces)
- **Eye Detection**: Bonus points for detecting both eyes
- **Brightness Check**: Rejects frames that are too dark or too bright

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
- Automatically closes after 1-second success message
- Ideal for MS Access integration
- Auto-enables auto_close when from_access=True

#### Silent Mode
```bash
python face.py "C:\Photos" "employee.jpg" grayscale autoclose silent
```
- Suppresses all success/error message boxes
- Fully automated operation
- Ideal for batch processing

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

| Command | Behavior | Output Files | Auto-Close | Messages |
|---------|----------|--------------|------------|----------|
| `python face.py "path" "file.jpg"` | Save both versions | `file_color.jpg`, `file_gray.jpg` | No | Yes |
| `python face.py "path" "file.jpg" grayscale` | Save grayscale only | `file.jpg` | Yes | No |
| `python face.py "path" "file.jpg" grayscale autoclose` | Save grayscale only | `file.jpg` | Yes | No |
| `python face.py "path" "file.jpg" grayscale autoclose silent` | Save grayscale only | `file.jpg` | Yes | No |
| No parameters (error) | Shows usage message | None | Yes | Yes |

## Technical Specifications

### Image Processing
- **Input Resolution**: Webcam native resolution (typically 640x480)
- **Output Size**: 200x250 pixels (standard ID photo size)
- **Supported Formats**: JPEG, PNG
- **Color Modes**: RGB color, Grayscale
- **Enhancement**: Auto brightness/contrast adjustment during capture
- **Compression**: Adjustable quality 0-100 (default: 95)

### Face Detection
- **Algorithm**: OpenCV Haar Cascade Classifiers
- **Detection Models**: Frontal face and eye detection
- **Quality Scoring**: Centering (frame position), size (face area), eye detection
- **Auto-Enhancement**: Pre-capture frame optimization with brightness boost
- **Capture Timing**: 3-second evaluation period for best frame selection

### System Requirements
- **Python**: 3.7 or higher
- **Webcam**: Any USB or built-in camera
- **OS**: Windows (primary), macOS, Linux
- **Memory**: 1GB RAM recommended
- **Storage**: 100MB free space
- **Display**: Minimum 1400x750 resolution

## Configuration

### Error Handling & Logging
Advanced error management system with:
- **Smart Log Management**: Automatically clears log files older than 2 days
- **Error-Only Logging**: Logs only errors and critical issues (no success messages)
- **Detailed Error Context**: Includes filename, line number, and function name for each error
- **Comprehensive Error Handling**: Try-catch blocks around all critical operations
- **Automatic Recovery**: Graceful handling of webcam, file system, and processing errors

Log format: `timestamp - ERROR - filename:line - function() - detailed_message`

Common logged errors:
- Webcam initialization/capture failures
- File system permission issues
- Image processing/saving errors
- Directory creation problems
- Cascade classifier loading failures

### Customization
Key parameters can be modified in the code:
```python
# Window size
self.root.geometry("1400x750")
self.root.minsize(1300, 700)

# Face detection parameters
faces = self.face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
)

# Auto-capture timing
countdown = 3 - int(elapsed)  # 3-second countdown

# Canvas sizes
self.canvas = tk.Canvas(self.left_container, width=640, height=480, bg='black')
self.canvas_color = tk.Canvas(self.preview_color, width=250, height=300, bg='white')

# Audio feedback
self.root.bell()  # System beep sound
```

## Troubleshooting

### Common Issues
- **Camera Not Found**: Check webcam connection and permissions (logged with specific error details)
- **Face Not Detected**: Ensure good lighting and face visibility
- **Save Path Error**: Directory creation failures are automatically logged with full path details
- **Import Errors**: Install required Python packages
- **File Save Failures**: Image write operations include success validation and detailed error logging
- **Cascade Loading Errors**: Haar cascade file loading failures logged with file paths

### Error Logs
Check `face_utility.log` for detailed error information with:
- Exact line numbers and function names where errors occurred
- Full stack traces for debugging
- Automatic log rotation (clears files older than 2 days)
- Error-only logging (no verbose success messages)

### Performance Tips
- Use good lighting for better face detection
- Position face within the guideline box
- Ensure stable internet connection for package updates
- Close other camera applications before running

## MS Access Integration

### VBA Integration with Dynamic File Paths based on Selection of Values
```vba
Private Sub cmdImage_Click()

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

### Complete VBA Function (Production Ready)
```vba
'==============================================================================
' FACE PHOTO UTILITY - MS ACCESS INTEGRATION
'==============================================================================
' This function launches the Python face capture utility and returns the saved image path
' 
' REQUIREMENTS:
' 1. Global Python installation with required packages
' 2. Face capture script at: [Access DB Path]\scripts\face.py
' 3. Webcam connected and accessible
' 4. Required Python packages: opencv-python, numpy, pillow, pyperclip
'
' USAGE MODES:
' Mode 1 - Both Versions: Saves color and grayscale versions, stays open
' Mode 2 - Grayscale Only: Saves single grayscale image, auto-closes
' Mode 3 - Silent Mode: No message boxes, fully automated
'==============================================================================

Public Function CaptureImageAndReturnPath(ByVal folderPath As String, ByVal fileName As String) As String
    On Error GoTo ErrorHandler

    Dim projectPath As String
    Dim scriptPath As String
    Dim photoFolder As String
    Dim photoFileName As String
    Dim commandLine As String
    Dim fullPhotoPath As String
    Dim shellObj As Object

    ' Define paths
    projectPath = CStr(Application.CurrentProject.path) & "\scripts"
    scriptPath = projectPath & "\face.py"
    photoFolder = IIf(Right(CStr(folderPath), 1) = "\", Left(CStr(folderPath), Len(CStr(folderPath)) - 1), CStr(folderPath))
    photoFileName = CStr(fileName)
    fullPhotoPath = photoFolder & "\" & photoFileName
    
    
     ' === VALIDATIONS ===
    If Dir(scriptPath) = "" Then
        MsgBox "Python script not found at: " & scriptPath, vbCritical
        CaptureImageAndReturnPath = ""
        Exit Function
    End If

    If Dir(photoFolder, vbDirectory) = "" Then
        MsgBox "Image folder does not exist: " & photoFolder, vbCritical
        CaptureImageAndReturnPath = ""
        Exit Function
    End If
    
    
    ' Create shell object
    Set shellObj = CreateObject("WScript.Shell")

    ' Validate Python in system PATH
    If shellObj.Run("cmd /c python --version", 0, True) <> 0 Then
        MsgBox "Python is not available in system PATH.", vbCritical
        CaptureImageAndReturnPath = ""
        Exit Function
    End If

    ' Construct command to run the Python script
    commandLine = "cmd /c python """ & scriptPath & """ """ & _
                  photoFolder & """ """ & photoFileName & """ grayscale autoclose silent"
    
    ' Choose your command mode (uncomment one):
    
    ' MODE 1: BOTH COLOR AND GRAYSCALE (Interactive)
    ' Saves both versions: filename_color.jpg and filename_gray.jpg
    ' Application stays open for user interaction
    ' commandLine = "cmd /c python """ & scriptPath & """ """ & _
    '               photoFolder & """ """ & photoFileName & """
    
    ' MODE 2: GRAYSCALE ONLY (Recommended for MS Access)
    ' Saves only grayscale version as specified filename
    ' Automatically closes after capture
    ' commandLine = "cmd /c python """ & scriptPath & """ """ & _
    '               photoFolder & """ """ & photoFileName & """ grayscale"
    
    ' MODE 3: SILENT GRAYSCALE (Fully Automated) - CURRENT ACTIVE MODE
    ' Saves only grayscale version, no message boxes, auto-closes
    ' Best for batch processing and database integration
'     commandLine = "cmd /c python """ & scriptPath & """ """ & _
                  photoFolder & """ """ & photoFileName & """ grayscale autoclose silent"
    
    ' Debug output
    Debug.Print commandLine

    ' Run the command (hidden window, wait for completion)
    shellObj.Run commandLine, 0, True

    ' Check if file was created
    If Dir(fullPhotoPath) <> "" Then
        DoCmd.Beep
        MsgBox "Image created successfully!", vbInformation
        CaptureImageAndReturnPath = NormalizePath(folderPath & "\" & fileName)
    Else
        MsgBox "Image not found at: " & fullPhotoPath, vbExclamation
        CaptureImageAndReturnPath = ""
    End If

    Exit Function

ErrorHandler:
    MsgBox "Error: " & Err.Description, vbCritical
    CaptureImageAndReturnPath = ""
End Function

'==============================================================================
' HELPER FUNCTIONS
'==============================================================================

' Creates directory structure recursively if it doesn't exist
' Usage: PathCreator "C:\Photos\Employee\2024"
Sub PathCreator(strPath As String)
Dim fso As New FileSystemObject
Dim dirs() As String
Dim i As Long
Dim newpath As String

dirs = Split(strPath, "\")

For i = LBound(dirs) To UBound(dirs) - 1
    
    If Len(dirs(i)) > 0 Then
     If i > 0 Then
         newpath = newpath & "\" & dirs(i)
        
        Else
          newpath = dirs(i)
        End If
   Debug.Print newpath
   
        If Not fso.FolderExists(newpath) Then
         'If Dir(newpath, vbDirectory) = "" Then
           fso.CreateFolder newpath
            '' MkDir newpath
        End If
    End If
    
Next i

End Sub


' Test function to verify the face capture system is working
' Usage: Call TestFaceCapture()
Public Sub TestFaceCapture()
    Dim testFolder As String
    Dim testFileName As String
    Dim result As String
    
    ' Setup test parameters
    testFolder = Application.CurrentProject.path & "\TestPhotos"
    testFileName = "test_capture_" & Format(Now, "yyyymmdd_hhnnss") & ".jpg"
    
    ' Create test folder
    PathCreator testFolder
    
    ' Attempt capture
    MsgBox "Test capture starting. Position your face in front of the camera.", vbInformation
    result = CaptureImageAndReturnPath(testFolder, testFileName)
    
    ' Report results
    If result <> "" Then
        MsgBox "Test successful! Image saved at:" & vbCrLf & result, vbInformation
    Else
        MsgBox "Test failed. Check the debug output and error messages.", vbCritical
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