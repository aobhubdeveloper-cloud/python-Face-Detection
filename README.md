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

### Logging
Logs are automatically saved to `face_utility.log` with:
- Application startup/shutdown events
- Error tracking and debugging info
- System information and version details

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
    Dim txtSubject As String
    Dim resultPath As String
    
    ' Build the folder structure
    BIFolder = Application.CurrentProject.path & "\Movement Orders\" & _
        Nz(Me.TextCarriageComp.value, "") & "\" & _
        Nz(Me.TextCompany.value, "") & "\" & _
        Nz(Me.LoadFld.value, "") & " - " & Nz(Me.DecRef.value, "") & "\LivePictures\"
    
    ' Ensure the folder exists
    PathCreator BIFolder
    
    ' Build the filename
    txtSubject = "Dated_" & Format(Me.TextOrderDate.value, "DD-MMMM-YYYY") & "," & _
        CStr(Me.TextBowzer.value) & "," & CStr(Me.LoadFld.value) & _
        "-" & CStr(Me.DecRef.value) & "," & CStr(Me.TextDrv1.value)
    
    fileName = txtSubject & ".jpg"

    ' Call webcam capture and get result
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
' 1. Python virtual environment at: [Access DB Path]\scripts\.venv\
' 2. Face capture script at: [Access DB Path]\scripts\face.py
' 3. Webcam connected and accessible
' 4. Required Python packages: opencv-python, numpy, pillow, pyperclip
'
' USAGE MODES:
' Mode 1 - Grayscale Only (Recommended for Access): Saves single grayscale image, auto-closes
' Mode 2 - Both Versions: Saves color and grayscale versions, stays open
' Mode 3 - Silent Mode: No message boxes, fully automated
'==============================================================================

Public Function CaptureImageAndReturnPath(ByVal folderPath As String, ByVal fileName As String) As String
    On Error GoTo ErrorHandler

    ' Variable declarations
    Dim projectPath As String      ' Path to scripts folder
    Dim pythonPath As String       ' Path to Python executable in virtual environment
    Dim scriptPath As String       ' Path to face.py script
    Dim photoFolder As String      ' Cleaned folder path for saving
    Dim photoFileName As String    ' Image filename
    Dim commandLine As String      ' Complete command to execute
    Dim fullPhotoPath As String    ' Full path to expected saved image
    Dim shellObj As Object         ' Shell object for running commands
    Dim startTime As Date          ' For timeout handling
    
    ' STEP 1: Setup paths (adjust these paths based on your installation)
    projectPath = CStr(Application.CurrentProject.path) & "\scripts"
    pythonPath = projectPath & "\.venv\Scripts\python.exe"  ' Virtual environment Python
    scriptPath = projectPath & "\face.py"                    ' Main face capture script
    
    ' STEP 2: Clean and validate input paths
    photoFolder = IIf(Right(CStr(folderPath), 1) = "\", Left(CStr(folderPath), Len(CStr(folderPath)) - 1), CStr(folderPath))
    photoFileName = CStr(fileName)
    fullPhotoPath = photoFolder & "\" & photoFileName
    
    ' STEP 3: Verify required files exist
    If Dir(pythonPath) = "" Then
        MsgBox "Python executable not found at: " & pythonPath & vbCrLf & _
               "Please ensure virtual environment is set up correctly.", vbCritical
        CaptureImageAndReturnPath = ""
        Exit Function
    End If
    
    If Dir(scriptPath) = "" Then
        MsgBox "Face capture script not found at: " & scriptPath, vbCritical
        CaptureImageAndReturnPath = ""
        Exit Function
    End If
    
    ' STEP 4: Ensure target directory exists
    PathCreator photoFolder
    
    ' STEP 5: Choose command mode based on requirements
    
    ' MODE 1: GRAYSCALE ONLY (Recommended for MS Access)
    ' - Saves only grayscale version as specified filename
    ' - Automatically closes after capture
    ' - No success message boxes
    ' - Ideal for database integration
    commandLine = "cmd /c """ & _
        """" & pythonPath & """" & " " & _
        """" & scriptPath & """" & " " & _
        """" & photoFolder & """" & " " & _
        """" & photoFileName & """" & " grayscale"""
    
    ' MODE 2: BOTH COLOR AND GRAYSCALE (Interactive)
    ' - Saves both color and grayscale versions
    ' - Files saved as: filename_color.jpg and filename_gray.jpg
    ' - Application stays open for user interaction
    ' - User can click previews to save manually
    ' Uncomment below to use this mode:
    ' commandLine = "cmd /c """ & _
    '     """" & pythonPath & """" & " " & _
    '     """" & scriptPath & """" & " " & _
    '     """" & photoFolder & """" & " " & _
    '     """" & photoFileName & """"
    
    ' MODE 3: SILENT GRAYSCALE (Fully Automated)
    ' - Saves only grayscale version
    ' - No message boxes at all
    ' - Automatically closes
    ' - Best for batch processing
    ' Uncomment below to use this mode:
    ' commandLine = "cmd /c """ & _
    '     """" & pythonPath & """" & " " & _
    '     """" & scriptPath & """" & " " & _
    '     """" & photoFolder & """" & " " & _
    '     """" & photoFileName & """" & " grayscale autoclose silent"""
    
    ' STEP 6: Debug output (remove in production if not needed)
    Debug.Print "=== FACE CAPTURE DEBUG INFO ==="
    Debug.Print "Project Path: " & projectPath
    Debug.Print "Python Path: " & pythonPath
    Debug.Print "Script Path: " & scriptPath
    Debug.Print "Photo Folder: " & photoFolder
    Debug.Print "Photo Filename: " & photoFileName
    Debug.Print "Full Photo Path: " & fullPhotoPath
    Debug.Print "Command: " & commandLine
    Debug.Print "================================"
    
    ' STEP 7: Execute the Python script
    Set shellObj = CreateObject("WScript.Shell")
    
    ' Run parameters explanation:
    ' - commandLine: The complete command to execute
    ' - 0: Hide the command window (use 1 to show for debugging)
    ' - True: Wait for completion before continuing
    shellObj.Run commandLine, 0, True
    
    ' STEP 8: Wait for file system to update (important for network drives)
    Application.Wait (Now + TimeValue("0:00:02"))  ' Wait 2 seconds
    
    ' STEP 9: Verify the image was created and return result
    If Dir(fullPhotoPath) <> "" Then
        ' Success: Image file exists
        DoCmd.Beep  ' Audio confirmation
        CaptureImageAndReturnPath = fullPhotoPath
        Debug.Print "SUCCESS: Image saved at " & fullPhotoPath
    Else
        ' Failure: Image file not found
        MsgBox "Image capture failed or was cancelled." & vbCrLf & _
               "Expected file: " & fullPhotoPath & vbCrLf & vbCrLf & _
               "Possible causes:" & vbCrLf & _
               "- User cancelled the capture" & vbCrLf & _
               "- Webcam not available" & vbCrLf & _
               "- Insufficient lighting for face detection" & vbCrLf & _
               "- Python script error (check face_utility.log)", vbExclamation
        CaptureImageAndReturnPath = ""
        Debug.Print "FAILURE: Image not found at " & fullPhotoPath
    End If
    
    Exit Function

ErrorHandler:
    ' Handle any VBA errors that occur
    MsgBox "VBA Error in CaptureImageAndReturnPath:" & vbCrLf & _
           "Error Number: " & Err.Number & vbCrLf & _
           "Description: " & Err.Description & vbCrLf & vbCrLf & _
           "Command attempted: " & commandLine, vbCritical
    Debug.Print "VBA ERROR: " & Err.Number & " - " & Err.Description
    CaptureImageAndReturnPath = ""
End Function

'==============================================================================
' HELPER FUNCTIONS
'==============================================================================

' Creates directory structure recursively if it doesn't exist
' Usage: PathCreator "C:\Photos\Employee\2024"
Public Sub PathCreator(ByVal strPath As String)
    On Error Resume Next
    
    Dim pathParts() As String
    Dim currentPath As String
    Dim i As Integer
    
    ' Handle UNC paths and drive letters
    If Left(strPath, 2) = "\\" Then
        ' UNC path
        pathParts = Split(strPath, "\")
        currentPath = "\\" & pathParts(2) & "\" & pathParts(3)  ' \\server\share
        i = 4
    Else
        ' Regular path
        pathParts = Split(strPath, "\")
        currentPath = pathParts(0)  ' Drive letter (C:)
        i = 1
    End If
    
    ' Create each directory level
    For i = i To UBound(pathParts)
        If pathParts(i) <> "" Then
            currentPath = currentPath & "\" & pathParts(i)
            If Dir(currentPath, vbDirectory) = "" Then
                MkDir currentPath
            End If
        End If
    Next i
    
    On Error GoTo 0
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