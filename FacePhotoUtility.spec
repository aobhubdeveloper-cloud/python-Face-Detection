# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['face-uitlity.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Hussaini Logistics\\AppData\\Roaming\\Python\\Python312\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml', 'cv2/data/haarcascades'), ('C:\\Users\\Hussaini Logistics\\AppData\\Roaming\\Python\\Python312\\site-packages\\cv2\\data\\haarcascade_eye.xml', 'cv2/data/haarcascades')],
    hiddenimports=['cv2', 'numpy', 'PIL', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FacePhotoUtility',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
