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

![Python Application Interface](./Python%20UI.png)
*Python application interface showing live webcam feed and dual preview panels*

### 🔗 Integration
- **MS Access Compatible**: Seamless integration with database applications
- **Command Line Support**: Can be launched with parameters
- **Path Management**: Robust file path handling and validation
- **Clipboard Integration**: Automatic path copying to clipboard
- **Directory Auto-Creation**: Automatically creates save directories if they don't exist

### 🗃️ MS Access Database Form Features
- **Auto-Installation Validation**: Checks Python, libraries, and ActiveX controls before form load
- **AccessImagine Integration**: Uses AccessImagine ActiveX control for seamless image display
- **Dynamic File Path Generation**: Automatically builds folder structure based on form field values
- **Live Image Display**: Real-time preview of captured photos in Access forms
- **Database Field Integration**: Direct binding to image fields in Access tables
- **Automated Database Storage**: Automatically stores file path and filename in database fields
- **Preview Last Saved Images**: View recently captured images with metadata
- **Automated Workflow**: One-click capture, save, and database update
- **Path Validation**: Ensures directory structure exists before capture
- **Error Handling**: Comprehensive VBA error management with user feedback
- **Batch Processing**: Support for multiple image captures in sequence
- **Field-Based Naming**: Intelligent filename generation from form data
- **Pre-Flight Checks**: Validates all dependencies before allowing image capture
- **Transaction Management**: Ensures database consistency during image capture and storage
- **Cross-Form Integration**: Reference forms can pass file paths and names between forms

![Sample MS Access Form](./Sample%20Form.png)
*Sample MS Access form showing integrated face capture functionality*

### 💾 MS Access Database Sample File
The system includes a complete MS Access database sample (`Live Webcam Feed.accdb`) demonstrating full integration:

#### Main Form
- **Purpose**: Central navigation and system overview
- **Features**: Access to all capture and preview functions
- **Validation**: Pre-flight system checks before opening sub-forms
- **Navigation**: Quick access to capture and preview forms

#### Live Face Capture Form
- **Purpose**: Direct integration with Python face capture utility
- **Features**: Real-time image capture with database storage
- **Integration**: Calls Python script with dynamic file paths
- **Display**: AccessImagine control for immediate image preview
- **Storage**: Automatic database field population

#### Reference Form
- **Purpose**: Pass file paths and names between forms
- **Features**: Cross-form data sharing and validation
- **Integration**: Seamless data transfer for batch operations
- **Validation**: Path and filename verification before processing

#### Stored Files Preview Form
- **Purpose**: View and manage previously captured images
- **Features**: 
  - **ID Display**: Unique identifier for each captured image
  - **File Name**: Original filename with metadata
  - **File Path**: Complete path to stored image file
  - **Timestamp**: Capture date and time information
  - **Image Preview**: Thumbnail display of stored images
  - **File Management**: Options to view, delete, or export images
  - **Search & Filter**: Find images by date, name, or path
  - **Batch Operations**: Select multiple images for bulk actions

## Installation

### Auto-Installation Scripts
The system includes automated installation scripts for easy setup:

#### Python Environment Setup
```bash
# Run the automated Python setup
setup_environment.py

# Or use the batch file
install_python.bat
```

#### AccessImagine ActiveX Control
```bash
# Install AccessImagine ActiveX control for MS Access
install_accessimagine.bat
```

### Manual Prerequisites
```bash
pip install opencv-python numpy pillow pyperclip
```

### Files Required
- `face.py` - Main application
- `Live Webcam Feed.accdb` - MS Access database sample with integrated forms
- `setup_environment.py` - Auto-installer for Python dependencies
- `install_python.bat` - Batch installer for Python environment
- `install_accessimagine.bat` - AccessImagine ActiveX installer
- Haar cascade XML files (included with OpenCV)
- Python virtual environment (recommended)

### MS Access Setup Requirements

#### AccessImagine ActiveX Control
Required for displaying images in MS Access forms:
- **Component**: AccessImagine ActiveX Control
- **Purpose**: Real-time image display and database integration
- **Installation**: Run `install_accessimagine.bat` as Administrator
- **Registration**: Automatically registers the control in Windows Registry
- **Validation**: Form validates control availability before opening

#### Form Validation Process
Before opening any form with image capture functionality:
1. **Python Installation Check**: Validates Python is installed and accessible
2. **Required Libraries Check**: Verifies opencv-python, numpy, pillow, pyperclip
3. **AccessImagine Control Check**: Confirms ActiveX control is registered
4. **Webcam Availability Check**: Tests camera access permissions
5. **Script Path Validation**: Ensures face.py exists in scripts folder
6. **Error Reporting**: Displays specific missing components with installation guidance

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

### Pre-Form Validation Process
Before any form with image capture opens, the system performs comprehensive validation:

```vba
' Form Load Event - Validation Example
Private Sub Form_Load()
    If Not ValidateSystemRequirements() Then
        MsgBox "System requirements not met. Please run setup scripts.", vbCritical
        DoCmd.Close acForm, Me.Name
        Exit Sub
    End If
End Sub

Private Function ValidateSystemRequirements() As Boolean
    ' Check Python installation
    If Not IsPythonInstalled() Then
        MsgBox "Python not found. Run install_python.bat", vbCritical
        Return False
    End If
    
    ' Check required Python libraries
    If Not ArePythonLibrariesInstalled() Then
        MsgBox "Python libraries missing. Run setup_environment.py", vbCritical
        Return False
    End If
    
    ' Check AccessImagine ActiveX control
    If Not IsAccessImagineInstalled() Then
        MsgBox "AccessImagine control missing. Run install_accessimagine.bat as Administrator", vbCritical
        Return False
    End If
    
    ' Check webcam availability
    If Not IsWebcamAvailable() Then
        MsgBox "Webcam not accessible. Check permissions and connections.", vbExclamation
        Return False
    End If
    
    Return True
End Function
```

### AccessImagine ActiveX Control Setup
The AccessImagine control enables seamless image display in MS Access:

```vba
' Initialize AccessImagine control on form
Private Sub Form_Open(Cancel As Integer)
    ' Set AccessImagine properties
    Me.ImageControl.BorderStyle = 1
    Me.ImageControl.SizeMode = 3  ' Zoom to fit
    Me.ImageControl.BackColor = RGB(255, 255, 255)
End Sub

' Update image display after capture
Private Sub UpdateImageDisplay(imagePath As String)
    If Dir(imagePath) <> "" Then
        Me.ImageControl.Picture = imagePath
        Me.ImageControl.Requery
    End If
End Sub
```

### Database Storage Integration
The system automatically stores captured image information in database fields:

```vba
' Database field mapping for image storage
Private Sub StoreImageToDatabase(imagePath As String, fileName As String)
    On Error GoTo ErrorHandler
    
    ' Store full file path in database field
    Me.ImageFilePath.Value = imagePath
    
    ' Store just the filename in separate field
    Me.ImageFileName.Value = fileName
    
    ' Store capture timestamp
    Me.ImageCaptureDate.Value = Now()
    
    ' Store file size for reference
    Me.ImageFileSize.Value = FileLen(imagePath)
    
    ' Update the record
    Me.Dirty = False
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Error storing image to database: " & Err.Description, vbCritical
End Sub
```

### VBA Integration with Dynamic File Paths and Database Storage
```vba
Private Sub cmdImage_Click()
    On Error GoTo ErrorHandler
    
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
        ' Update image display
        Me.DriverLivePicture.value = resultPath
        Me.DriverImage.Picture = DriverLivePicture
        Me.DriverImage.Requery
        
        ' Store image information to database
        Call StoreImageToDatabase(resultPath, fileName)
        
        ' Enable save button
        Me.BtnSave.Enabled = True
        
        MsgBox "Image captured and stored successfully!", vbInformation
    Else
        MsgBox "Image capture cancelled or failed.", vbExclamation
        Me.BtnSave.Enabled = False
    End If
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Error in image capture process: " & Err.Description, vbCritical
End Sub
```

### Database Field Requirements
Ensure your Access table includes these fields for image storage:

```sql
-- Required database fields for image storage
ImageFilePath     TEXT(255)    -- Full path to image file
ImageFileName     TEXT(100)    -- Just the filename
ImageCaptureDate  DATETIME     -- When image was captured
ImageFileSize     LONG         -- File size in bytes (optional)
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
    Dim pythonExe As String
    Dim localAppData As String

    ' Define paths
    projectPath = CStr(Application.CurrentProject.path) & "\scripts"
    scriptPath = projectPath & "\face.py"
    
    ' Clean folder path: trim and remove any trailing backslashes to avoid quote escaping (\")
    photoFolder = Trim(CStr(folderPath))
    Do While Right(photoFolder, 1) = "\" Or Right(photoFolder, 1) = "/"
        photoFolder = Left(photoFolder, Len(photoFolder) - 1)
    Loop
    
    photoFileName = Trim(CStr(fileName))
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

    ' Dynamic Python detection (Direct executable path - avoids cmd /c quote-stripping issues)
    localAppData = Environ("LOCALAPPDATA")
    If Len(localAppData) > 0 And Dir(localAppData & "\Programs\Python\Python314\python.exe") <> "" Then
        pythonExe = localAppData & "\Programs\Python\Python314\python.exe"
    ElseIf Len(localAppData) > 0 And Dir(localAppData & "\Programs\Python\Python313\python.exe") <> "" Then
        pythonExe = localAppData & "\Programs\Python\Python313\python.exe"
    ElseIf Dir("C:\Windows\py.exe") <> "" Then
        pythonExe = "C:\Windows\py.exe"
    Else
        pythonExe = "python"
    End If

    ' Construct command line directly with executable (no cmd /c)
    commandLine = """" & pythonExe & """ """ & scriptPath & """ """ & _
                  photoFolder & """ """ & photoFileName & """ grayscale autoclose"
    
    ' Debug output
    Debug.Print "Executing: " & commandLine

    ' Run the command (0 = hidden background window so no black cmd window appears, True = wait for capture and auto-close)
    shellObj.Run commandLine, 0, True

    ' Check if file was created
    If Dir(fullPhotoPath) <> "" Then
        DoCmd.Beep
        CaptureImageAndReturnPath = fullPhotoPath
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