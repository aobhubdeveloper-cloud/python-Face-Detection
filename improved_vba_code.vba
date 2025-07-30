Private Sub Command398_Click()
    On Error GoTo ErrorHandler

    Dim projectPath As String
    Dim pythonPath As String
    Dim scriptPath As String
    Dim photoFolder As String
    Dim photoFileName As String
    Dim commandLine As String
    Dim fullPhotoPath As String
    Dim wsh As Object
    Dim waitOnReturn As Boolean
    Dim windowStyle As Integer
    Dim errorCode As Integer

    ' Define values (adjust based on your setup)
    projectPath = CStr(Application.CurrentProject.Path) & "\scripts"
    pythonPath = projectPath & "\.venv\Scripts\python.exe"
    scriptPath = projectPath & "\working.py"
    photoFolder = CStr(txtImagePath.Value)
    photoFileName = CStr(txtImageName.Value)

    ' Remove trailing backslash from photoFolder if present
    If Right(photoFolder, 1) = "\" Then
        photoFolder = Left(photoFolder, Len(photoFolder) - 1)
    End If

    ' Construct full photo path for checking later
    fullPhotoPath = photoFolder & "\" & photoFileName

    ' Construct command line
    commandLine = "cmd /c """ & _
        """" & pythonPath & """" & " " & _
        """" & scriptPath & """" & " " & _
        """" & photoFolder & """" & " " & _
        """" & photoFileName & """" & """"

    ' Debug Print to check
    Debug.Print "Command: " & commandLine
    Debug.Print "Expected file: " & fullPhotoPath

    ' Create Windows Script Host object for better process control
    Set wsh = CreateObject("WScript.Shell")
    
    ' Execute the command and wait for it to complete
    ' vbNormalFocus = 1, waitOnReturn = True
    waitOnReturn = True
    windowStyle = 1 ' vbNormalFocus
    
    ' Show progress message
    DoEvents
    Application.Echo False
    Me.Painting = False
    
    ' Display a temporary message
    Dim tempMsg As String
    tempMsg = "Launching camera application... Please capture your photo and save it."
    
    ' You might want to show this in a label or status bar instead
    Debug.Print tempMsg
    
    ' Execute and wait for completion
    errorCode = wsh.Run(commandLine, windowStyle, waitOnReturn)
    
    ' Restore form painting
    Me.Painting = True
    Application.Echo True
    
    ' Check the error code
    If errorCode <> 0 Then
        MsgBox "Python script returned error code: " & errorCode, vbExclamation, "Script Error"
        GoTo Cleanup
    End If
    
    ' Give a moment for file system to update
    Sleep 500
    DoEvents
    
    ' Check if file was created
    If Dir(fullPhotoPath) <> "" Then
        ' File exists, try to display it
        On Error Resume Next
        
        ' If you have an image control named imgFacePhoto, uncomment the next line:
        ' Me.imgFacePhoto.Picture = fullPhotoPath
        
        ' Alternative: Set the picture using LoadPicture
        ' Me.imgFacePhoto.Picture = LoadPicture(fullPhotoPath)
        
        If Err.Number <> 0 Then
            MsgBox "Image created successfully at: " & fullPhotoPath & vbCrLf & _
                   "However, there was an error displaying it: " & Err.Description, _
                   vbInformation, "Image Created"
            Err.Clear
        Else
            MsgBox "Image created and displayed successfully!", vbInformation, "Success"
        End If
        
        On Error GoTo ErrorHandler
        
        ' Refresh the form to ensure the image is displayed
        Me.Refresh
        DoEvents
        
    Else
        MsgBox "Image was not found at: " & fullPhotoPath & vbCrLf & _
               "Please check if the Python script completed successfully.", _
               vbExclamation, "Image Not Found"
    End If

Cleanup:
    ' Clean up objects
    Set wsh = Nothing
    Exit Sub

ErrorHandler:
    Application.Echo True
    Me.Painting = True
    MsgBox "Error: " & Err.Description & " (Error " & Err.Number & ")", vbCritical, "Error"
    GoTo Cleanup

End Sub

' Windows API Sleep function declaration (add this at the top of your module)
' If you don't have this already, add it to the top of your VBA module:
#If VBA7 Then
    Private Declare PtrSafe Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
#Else
    Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
#End If

' Alternative method using Shell and process monitoring
Private Sub Command398_Click_Alternative()
    On Error GoTo ErrorHandler

    Dim projectPath As String
    Dim pythonPath As String
    Dim scriptPath As String
    Dim photoFolder As String
    Dim photoFileName As String
    Dim commandLine As String
    Dim fullPhotoPath As String
    Dim taskID As Double
    Dim startTime As Double
    Dim timeoutSeconds As Double

    ' Define values
    projectPath = CStr(Application.CurrentProject.Path) & "\scripts"
    pythonPath = projectPath & "\.venv\Scripts\python.exe"
    scriptPath = projectPath & "\working.py"
    photoFolder = CStr(txtImagePath.Value)
    photoFileName = CStr(txtImageName.Value)

    ' Remove trailing backslash
    If Right(photoFolder, 1) = "\" Then
        photoFolder = Left(photoFolder, Len(photoFolder) - 1)
    End If

    fullPhotoPath = photoFolder & "\" & photoFileName

    ' Construct command
    commandLine = "cmd /c """ & _
        """" & pythonPath & """" & " " & _
        """" & scriptPath & """" & " " & _
        """" & photoFolder & """" & " " & _
        """" & photoFileName & """" & """"

    Debug.Print "Command: " & commandLine

    ' Launch the process
    taskID = Shell(commandLine, vbNormalFocus)
    
    ' Set timeout (5 minutes)
    timeoutSeconds = 300
    startTime = Timer
    
    ' Wait for the process to complete or timeout
    Do While Timer - startTime < timeoutSeconds
        DoEvents
        Sleep 1000 ' Wait 1 second
        
        ' Check if file exists (indicating completion)
        If Dir(fullPhotoPath) <> "" Then
            Exit Do
        End If
    Loop
    
    ' Check results
    If Dir(fullPhotoPath) <> "" Then
        ' Success - display image
        On Error Resume Next
        ' Me.imgFacePhoto.Picture = fullPhotoPath
        If Err.Number = 0 Then
            MsgBox "Image captured and displayed successfully!", vbInformation
        Else
            MsgBox "Image captured at: " & fullPhotoPath, vbInformation
        End If
        On Error GoTo ErrorHandler
        Me.Refresh
    Else
        If Timer - startTime >= timeoutSeconds Then
            MsgBox "Operation timed out. Please try again.", vbExclamation
        Else
            MsgBox "Image not found. Please check the application.", vbExclamation
        End If
    End If

    Exit Sub

ErrorHandler:
    MsgBox "Error: " & Err.Description, vbCritical
End Sub