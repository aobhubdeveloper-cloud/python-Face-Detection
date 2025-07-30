import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["cv2", "numpy", "PIL", "tkinter", "pyperclip"],
    "include_files": [
        (cv2.data.haarcascades + 'haarcascade_frontalface_default.xml', 'haarcascades/haarcascade_frontalface_default.xml'),
        (cv2.data.haarcascades + 'haarcascade_eye.xml', 'haarcascades/haarcascade_eye.xml')
    ]
}

# Base for GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Face Photo Utility",
    version="1.0",
    description="Face Photo Capture and Processing Utility",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "face-utility.py",
            base=base,
            target_name="FacePhotoUtility.exe",
            icon="app_icon.ico"  # You'll need to create/provide an icon file
        )
    ]
)
