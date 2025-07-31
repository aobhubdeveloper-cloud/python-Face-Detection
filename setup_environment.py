#!/usr/bin/env python3
"""
Environment Setup Script for Face Photo Utility
Checks Python installation, installs required packages, and validates environment
"""

import sys
import subprocess
import os
import importlib
from pathlib import Path

# Required packages for the face photo utility
REQUIRED_PACKAGES = [
    'opencv-python',
    'numpy', 
    'pillow',
    'pyperclip'
]

def check_python_installation():
    """Check if Python is properly installed and accessible"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
            return True
        else:
            print(f"✗ Python version {version.major}.{version.minor} is too old. Requires 3.7+")
            return False
    except Exception as e:
        print(f"✗ Python check failed: {e}")
        return False

def install_package(package_name):
    """Install a Python package using pip"""
    try:
        print(f"Installing {package_name}...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', package_name
        ], capture_output=True, text=True, check=True)
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package_name}: {e.stderr}")
        return False

def check_package_installed(package_name):
    """Check if a package is already installed"""
    try:
        if package_name == 'opencv-python':
            importlib.import_module('cv2')
        elif package_name == 'pillow':
            importlib.import_module('PIL')
        else:
            importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def setup_environment():
    """Main setup function"""
    print("=== Face Photo Utility Environment Setup ===\n")
    
    # Check Python installation
    if not check_python_installation():
        print("\nPlease install Python 3.7+ from https://python.org")
        return False
    
    # Check and install required packages
    print("\nChecking required packages...")
    all_installed = True
    
    for package in REQUIRED_PACKAGES:
        if check_package_installed(package):
            print(f"✓ {package} already installed")
        else:
            print(f"✗ {package} not found")
            if not install_package(package):
                all_installed = False
    
    if all_installed:
        print("\n✓ All packages installed successfully!")
        print("Environment is ready for Face Photo Utility")
        return True
    else:
        print("\n✗ Some packages failed to install")
        return False

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)