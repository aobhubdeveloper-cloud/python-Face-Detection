# External library imports for image processing and GUI
import cv2  # OpenCV for image processing and webcam capture
import numpy as np  # NumPy for numerical operations on images
from PIL import Image, ImageTk  # Pillow for image handling and Tkinter compatibility
import tkinter as tk  # Main GUI framework
from tkinter import messagebox, ttk  # Additional GUI components
import sys  # System-specific parameters and functions
import os  # Operating system interface
import time  # Time access and conversions
import pyperclip  # Cross-platform clipboard operations
import subprocess  # Subprocess management

class ImageUtilityApp:
    """
    A comprehensive GUI application for capturing, processing, and saving face photos.
    Provides real-time face detection, image enhancement, and multiple output formats.
    """
    def __init__(self, root, save_path, filename, from_access=False):
        """
        Initialize the Image Utility Application
        
        Args:
            root: Tkinter root window
            save_path: Directory path where images will be saved
            filename: Name for the saved image file
            from_access: Boolean indicating if app is launched from Access database
        """
        # Initialize main window properties
        self.root = root
        self.save_path = save_path
        self.filename = filename
        self.from_access = from_access
        self.root.title("Image Utility App")
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.geometry("1400x900")  # Set default window size
        self.root.minsize(1200, 700)   # Set minimum window size
        
        # Auto brightness adjustment settings
        self.last_brightness_check = 0  # Timestamp of last brightness check
        self.auto_brightness_enabled = True  # Enable automatic brightness adjustment

        # Initialize webcam capture
        self.cap = cv2.VideoCapture(0)  # Open default camera (index 0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot open webcam")
            self.root.quit()
            return

        # Load Haar Cascade Classifiers for face and eye detection
        # These XML files contain pre-trained models for detecting faces and eyes
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        if self.face_cascade.empty() or self.eye_cascade.empty():
            messagebox.showerror("Error", "Failed to load detection models")
            self.root.quit()
            return

        # Image storage and processing variables
        self.cropped_face = None        # Stores the cropped face region
        self.color_img = None           # Processed color image
        self.gray_img = None            # Processed grayscale image
        self.bw_img = None              # Processed black and white image
        self.faces = []                 # List of detected face coordinates
        self.face_detected_time = None  # Timestamp when a face was first detected
        self.last_face_count = 0        # Number of faces in previous frame
        
        # Auto-capture related variables
        self.auto_capture = False       # Flag for auto-capture mode
        self.auto_capture_start = None  # Timestamp when auto-capture started
        self.best_frame = None          # Best frame captured during auto-capture
        self.best_score = -1            # Quality score of the best frame
        self.saved_image_path = ""      # Path of the last saved image

        # GUI Elements
        # Input frame for textboxes
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=3, pady=3)

        tk.Label(self.input_frame, text="Save Path:", font=("Arial", 8)).pack(side=tk.LEFT)
        self.path_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 8))
        self.path_entry.insert(0, save_path)
        self.path_entry.pack(side=tk.LEFT, padx=2)
        
        self.browse_button = tk.Button(self.input_frame, text="Browse", font=("Arial", 8), command=self.browse_path)
        self.browse_button.pack(side=tk.LEFT, padx=2)

        tk.Label(self.input_frame, text="Filename:", font=("Arial", 8)).pack(side=tk.LEFT)
        self.filename_entry = tk.Entry(self.input_frame, width=30, font=("Arial", 8))
        self.filename_entry.insert(0, filename)
        self.filename_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(self.input_frame, text="Saved Image:", font=("Arial", 8)).pack(side=tk.LEFT)
        self.saved_path_entry = tk.Entry(self.input_frame, width=25, font=("Arial", 8))
        self.saved_path_entry.config(state='readonly')
        self.saved_path_entry.pack(side=tk.LEFT, padx=2)
        self.saved_path_entry.bind("<Double-Button-1>", self.view_saved_image)

        # Main frame for live feed and previews
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Left side - Live feed
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.left_frame, width=800, height=600, bg='black')
        self.canvas.pack(padx=50, pady=0)
        
        # Right side - Saved images
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        tk.Label(self.right_frame, text="Saved Images (Click to Save)", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.canvas_color = tk.Canvas(self.right_frame, width=200, height=250, bg='white')
        self.canvas_color.pack(pady=2)
        tk.Label(self.right_frame, text="Color", font=('Arial', 8)).pack()
        
        self.canvas_gray = tk.Canvas(self.right_frame, width=200, height=250, bg='white')
        self.canvas_gray.pack(pady=2)
        tk.Label(self.right_frame, text="Grayscale", font=('Arial', 8)).pack()

        self.canvas_color.bind("<Button-1>", lambda e: self.save_image("color"))
        self.canvas_gray.bind("<Button-1>", lambda e: self.save_image("gray"))

        # Control frame (below live feed) - Responsive layout
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(fill=tk.X, padx=3, pady=3)
        
        # Row 1 - Buttons
        self.button_row = tk.Frame(self.control_frame)
        self.button_row.pack(fill=tk.X, pady=2)
        
        self.retake_button = tk.Button(self.button_row, text="Retake", font=("Arial", 8), command=self.reset_capture)
        self.retake_button.pack(side=tk.LEFT, padx=2)
        
        self.auto_capture_var = tk.BooleanVar()
        self.auto_capture_check = tk.Checkbutton(self.button_row, text="Auto-Capture", font=("Arial", 8), variable=self.auto_capture_var, command=self.toggle_auto_capture)
        self.auto_capture_check.pack(side=tk.LEFT, padx=2)
        
        self.auto_enhance_button = tk.Button(self.button_row, text="Auto-Enhance", font=("Arial", 8), command=self.auto_enhance)
        self.auto_enhance_button.pack(side=tk.LEFT, padx=2)
        
        # Row 2 - Sliders
        self.slider_row1 = tk.Frame(self.control_frame)
        self.slider_row1.pack(fill=tk.X, pady=2)
        
        tk.Label(self.slider_row1, text="Brightness", font=("Arial", 8)).pack(side=tk.LEFT)
        self.brightness_scale = tk.Scale(self.slider_row1, from_=-100, to=100, orient=tk.HORIZONTAL, length=120, font=("Arial", 7), command=self.apply_filters)
        self.brightness_scale.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.slider_row1, text="Contrast", font=("Arial", 8)).pack(side=tk.LEFT)
        self.contrast_scale = tk.Scale(self.slider_row1, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=120, font=("Arial", 7), command=self.apply_filters)
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.slider_row1, text="Sharpness", font=("Arial", 8)).pack(side=tk.LEFT)
        self.sharpness_scale = tk.Scale(self.slider_row1, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=120, font=("Arial", 7), command=self.apply_filters)
        self.sharpness_scale.set(1.0)
        self.sharpness_scale.pack(side=tk.LEFT, padx=2)
        
        # Row 3 - More sliders
        self.slider_row2 = tk.Frame(self.control_frame)
        self.slider_row2.pack(fill=tk.X, pady=2)
        
        tk.Label(self.slider_row2, text="Noise Reduction", font=("Arial", 8)).pack(side=tk.LEFT)
        self.noise_scale = tk.Scale(self.slider_row2, from_=0, to=5, orient=tk.HORIZONTAL, length=120, font=("Arial", 7), command=self.apply_filters)
        self.noise_scale.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.slider_row2, text="Saturation", font=("Arial", 8)).pack(side=tk.LEFT)
        self.saturation_scale = tk.Scale(self.slider_row2, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=120, font=("Arial", 7), command=self.apply_filters)
        self.saturation_scale.set(1.0)
        self.saturation_scale.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.slider_row2, text="Gamma", font=("Arial", 8)).pack(side=tk.LEFT)
        self.gamma_scale = tk.Scale(self.slider_row2, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=120, font=("Arial", 7), command=self.apply_filters)
        self.gamma_scale.set(1.0)
        self.gamma_scale.pack(side=tk.LEFT, padx=2)
        
        # Row 4 - Checkboxes and dropdowns
        self.option_row = tk.Frame(self.control_frame)
        self.option_row.pack(fill=tk.X, pady=2)
        
        self.equalize_var = tk.BooleanVar()
        self.equalize_check = tk.Checkbutton(self.option_row, text="Hist. Equal.", font=("Arial", 8), variable=self.equalize_var, command=self.apply_filters)
        self.equalize_check.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.option_row, text="Background", font=("Arial", 8)).pack(side=tk.LEFT)
        self.background_var = tk.StringVar(value="White")
        self.background_menu = ttk.Combobox(self.option_row, textvariable=self.background_var, values=["White", "Light Gray", "Dark Gray", "Light Blue"], width=12, font=("Arial", 8))
        self.background_menu.pack(side=tk.LEFT, padx=2)
        self.background_menu.bind("<<ComboboxSelected>>", self.apply_filters)
        
        tk.Label(self.option_row, text="Format", font=("Arial", 8)).pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="JPEG")
        self.format_menu = ttk.Combobox(self.option_row, textvariable=self.format_var, values=["JPEG", "PNG"], width=8, font=("Arial", 8))
        self.format_menu.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.option_row, text="Compression", font=("Arial", 8)).pack(side=tk.LEFT)
        self.compression_scale = tk.Scale(self.option_row, from_=0, to=100, orient=tk.HORIZONTAL, length=120, font=("Arial", 7))
        self.compression_scale.set(95)
        self.compression_scale.pack(side=tk.LEFT, padx=2)

        # Bind mouse events for live feed
        self.canvas.bind("<Button-1>", self.select_face)
        self.manual_crop = False
        self.crop_start = None
        self.crop_end = None
        self.canvas.bind("<ButtonPress-3>", self.start_manual_crop)
        self.canvas.bind("<B3-Motion>", self.update_manual_crop)
        self.canvas.bind("<ButtonRelease-3>", self.end_manual_crop)

        self.guidelines_enabled = True
        self.update_feed()

    def update_feed(self):
        """
        Main method for updating the video feed and processing each frame.
        Handles:
        - Webcam capture
        - Auto brightness adjustment
        - Face detection
        - Guide box drawing
        - Live filter application
        - Display updates
        """
        # Capture frame from webcam
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture webcam feed")
            self.root.quit()
            return
        
        # Automatic brightness adjustment system
        # Checks every 0.5 seconds to avoid constant adjustments
        if self.auto_brightness_enabled and time.time() - self.last_brightness_check > 0.5:
            gray_check = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray_check)
            if avg_brightness < 80:  # Boost brightness in low light conditions
                frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=25)
            elif avg_brightness > 180:  # Reduce brightness in high light conditions
                frame = cv2.convertScaleAbs(frame, alpha=0.8, beta=-15)
            self.last_brightness_check = time.time()

        # Apply live filters to feed
        img = frame.copy()
        noise = self.noise_scale.get()
        if noise > 0:
            img = cv2.GaussianBlur(img, (2 * noise + 1, 2 * noise + 1), 0)
        saturation = self.saturation_scale.get()
        if saturation != 1.0:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255).astype(np.uint8)
            img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        brightness = self.brightness_scale.get()
        contrast = self.contrast_scale.get()
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        sharpness = self.sharpness_scale.get()
        kernel = np.array([[-1, -1, -1], [-1, 9 * sharpness, -1], [-1, -1, -1]])
        img = cv2.filter2D(img, -1, kernel)
        gamma = self.gamma_scale.get()
        if gamma != 1.0:
            inv_gamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
            img = cv2.LUT(img, table)
        if self.background_var.get() != "None":
            img = self.apply_background(img, self.background_var.get())

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        self.faces = faces

        # Track face detection timing
        if len(faces) > 0:
            if self.last_face_count == 0:  # Face just appeared
                self.face_detected_time = time.time()
            if self.face_detected_time is not None:
                elapsed = time.time() - self.face_detected_time
                if elapsed <= 3:  # Show countdown for 3 seconds
                    countdown = 3 - int(elapsed)
                    cv2.putText(img, f"Capturing in: {countdown}", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                elif not self.auto_capture:  # After 3 seconds, trigger auto-capture
                    self.auto_capture = True
                    self.auto_capture_var.set(True)
                    self.auto_capture_start = time.time()
        else:
            self.face_detected_time = None
        
        self.last_face_count = len(faces)

        # Draw guideline box
        h, w = img.shape[:2]
        head_width = int(w * 0.8)
        head_height = int(h * 0.8)
        guide_x1 = (w - head_width) // 2
        guide_y1 = (h - head_height) // 2
        guide_x2 = guide_x1 + head_width
        guide_y2 = guide_y1 + head_height
        cv2.rectangle(img, (guide_x1, guide_y1), (guide_x2, guide_y2), (255, 255, 0), 1)
        cv2.putText(img, "Place face here", (guide_x1, guide_y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        for (x, y, w, h) in faces:
            center_x = x + w // 2
            center_y = y + h // 2
            face_width = head_width
            face_height = head_height
            face_x1 = center_x - face_width // 2
            face_y1 = center_y - face_height // 2
            face_x2 = face_x1 + face_width
            face_y2 = face_y1 + face_height
            cv2.rectangle(img, (face_x1, face_y1), (face_x2, face_y2), (0, 255, 0), 2)
            face_roi = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(img, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 0, 0), 1)

        if self.manual_crop and self.crop_start and self.crop_end:
            cv2.rectangle(img, self.crop_start, self.crop_end, (0, 0, 255), 2)

        # Resize frame to fit canvas
        frame_resized = cv2.resize(img, (800, 600))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img_tk = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img_tk)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

        if self.cropped_face is not None:
            self.update_previews()

        if self.auto_capture:
            if self.auto_capture_start is None:
                self.auto_capture_start = time.time()
                # Pre-enhance frame for better capture
                frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)  # Slightly brighten
                
            elapsed = time.time() - self.auto_capture_start
            if elapsed < 3:  # Reduced to 3 seconds for faster capture
                score = self.evaluate_frame(frame, faces)
                if score > 2.0:  # If we find a very good frame, capture immediately
                    self.best_frame = frame.copy()
                    self.best_score = score
                    elapsed = 3  # Force immediate capture
                elif score > self.best_score:
                    self.best_score = score
                    self.best_frame = frame.copy()
            else:
                if self.best_frame is not None and len(faces) > 0:
                    # Apply quick enhancement before capture
                    self.best_frame = cv2.convertScaleAbs(
                        self.best_frame, 
                        alpha=1.2,  # Increase contrast
                        beta=15     # Increase brightness
                    )
                    self.auto_capture_face()
                self.auto_capture = False
                self.auto_capture_var.set(False)
                self.auto_capture_start = None
                self.best_frame = None
                self.best_score = -1
                self.face_detected_time = None  # Reset face detection timer

        self.root.after(10, self.update_feed)

    def evaluate_frame(self, frame, faces):
        """
        Evaluate the quality of a frame for auto-capture.
        Considers:
        - Face centering
        - Eye detection
        - Brightness and contrast
        - Face size relative to frame
        Returns score from -1 (worst) to 3 (best)
        """
        if len(faces) != 1:
            return -1
            
        (x, y, w, h) = faces[0]
        
        # Check face centering
        frame_center_x = frame.shape[1] // 2
        face_center_x = x + w // 2
        centering_score = 1 - abs(frame_center_x - face_center_x) / frame.shape[1]
        
        # Check face size (prefer closer faces)
        size_score = min(w * h / (frame.shape[0] * frame.shape[1]) * 4, 1.0)
        
        # Check eyes and facial features
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_roi = gray[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
        eye_score = 1 if len(eyes) >= 2 else 0
        
        # Check brightness and contrast in face region
        avg_brightness = np.mean(face_roi)
        if avg_brightness < 50 or avg_brightness > 200:  # Too dark or too bright
            return -1
            
        return centering_score + eye_score + size_score

    def auto_capture_face(self):
        if self.best_frame is None:
            return
        gray = cv2.cvtColor(self.best_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            self.capture_face(self.best_frame, x, y, w, h)

    def select_face(self, event):
        if self.auto_capture:
            return
        x, y = event.x, event.y
        for (fx, fy, fw, fh) in self.faces:
            if fx <= x <= fx + fw and fy <= y <= fy + fh:
                ret, frame = self.cap.read()
                if not ret:
                    return
                self.capture_face(frame, fx, fy, fw, fh)
                break

    def capture_face(self, frame, x, y, w, h):
        """
        Crop and process a detected face from the frame.
        
        Args:
            frame: The source video frame
            x, y: Top-left coordinates of the detected face
            w, h: Width and height of the detected face
        
        The method:
        1. Calculates frame aspect ratio
        2. Adds padding around the face
        3. Ensures the crop area stays within frame bounds
        4. Maintains aspect ratio of the final crop
        5. Resizes to standard dimensions
        """
        # Calculate frame aspect ratio for consistent output
        frame_aspect = frame.shape[1] / frame.shape[0]
        
        # Add padding around the face (100% horizontal, 120% vertical)
        padding_x = int(w * 1.0)
        padding_y = int(h * 1.2)
        
        # Calculate initial crop coordinates with padding
        x1 = max(x - padding_x, 0)
        y1 = max(y - padding_y, 0)
        x2 = min(x + w + padding_x, frame.shape[1])
        y2 = min(y + h + padding_y, frame.shape[0])
        crop_width = x2 - x1
        crop_height = y2 - y1
        crop_aspect = crop_width / crop_height
        if crop_aspect > frame_aspect:
            new_width = int(crop_height * frame_aspect)
            x1 = x + w//2 - new_width//2
            x2 = x1 + new_width
        else:
            new_height = int(crop_width / frame_aspect)
            y1 = y + h//2 - new_height//2
            y2 = y1 + new_height
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)
        self.cropped_face = frame[y1:y2, x1:x2]
        self.cropped_face = cv2.resize(self.cropped_face, (200, 250))
        self.apply_filters()

    def start_manual_crop(self, event):
        self.manual_crop = True
        self.crop_start = (event.x, event.y)
        self.crop_end = None

    def update_manual_crop(self, event):
        self.crop_end = (event.x, event.y)

    def end_manual_crop(self, event):
        self.crop_end = (event.x, event.y)
        self.manual_crop = False
        ret, frame = self.cap.read()
        if not ret:
            return
        x1, y1 = self.crop_start
        x2, y2 = self.crop_end
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        self.cropped_face = frame[y1:y2, x1:x2]
        self.cropped_face = cv2.resize(self.cropped_face, (200, 250))
        self.apply_filters()
        self.crop_start = None
        self.crop_end = None

    def auto_enhance(self):
        if self.cropped_face is None:
            messagebox.showwarning("Warning", "No face selected to enhance")
            return
        # Use default enhancement values
        self.brightness_value = 20
        self.contrast_value = 1.3
        self.sharpness_value = 1.5
        self.noise_value = 1
        self.saturation_value = 1.2
        self.gamma_value = 1.0
        self.equalize_enabled = True
        self.apply_filters()

    def apply_filters(self, _=None):
        """
        Apply image processing filters to the cropped face image using fixed enhancement values.
        Args:
            _: Optional parameter for Tkinter callback compatibility (not used)
        """
        if self.cropped_face is None:
            return
            
        # Start with a fresh copy of the original image
        img = self.cropped_face.copy()
        
        # Apply noise reduction
        if hasattr(self, 'noise_value'):
            noise = self.noise_value
            if noise > 0:
                img = cv2.GaussianBlur(img, (2 * noise + 1, 2 * noise + 1), 0)
        
        # Adjust image saturation
        if hasattr(self, 'saturation_value'):
            saturation = self.saturation_value
            if saturation != 1.0:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255).astype(np.uint8)
                img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Apply brightness and contrast
        if hasattr(self, 'brightness_value') and hasattr(self, 'contrast_value'):
            img = cv2.convertScaleAbs(img, alpha=self.contrast_value, beta=self.brightness_value)
        
        # Apply sharpening
        if hasattr(self, 'sharpness_value'):
            kernel = np.array([[-1, -1, -1], [-1, 9 * self.sharpness_value, -1], [-1, -1, -1]])
            img = cv2.filter2D(img, -1, kernel)
        
        # Apply gamma correction
        if hasattr(self, 'gamma_value'):
            gamma = self.gamma_value
            if gamma != 1.0:
                inv_gamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
                img = cv2.LUT(img, table)
        
        # Apply background
        if self.background_var.get() != "None":
            img = self.apply_background(img, self.background_var.get())
        self.color_img = img
        self.color_img = img
        # Apply CLAHE enhancement to grayscale
        self.gray_img = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2GRAY)
        if hasattr(self, 'equalize_enabled') and self.equalize_enabled:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            self.gray_img = clahe.apply(self.gray_img)
        self.update_previews()

    def apply_background(self, img, background_type):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [largest_contour], -1, 255, -1)
        mask_inv = cv2.bitwise_not(mask)
        fg = cv2.bitwise_and(img, img, mask=mask)
        if background_type == "Light Gray":
            bg_color = (200, 200, 200)
        elif background_type == "Dark Gray":
            bg_color = (128, 128, 128)
        elif background_type == "Light Blue":
            bg_color = (200, 200, 255)
        else:
            bg_color = (255, 255, 255)
        bg = np.full_like(img, bg_color)
        bg = cv2.bitwise_and(bg, bg, mask=mask_inv)
        return cv2.add(fg, bg)


    def view_saved_image(self, event):
        if self.saved_image_path and os.path.exists(self.saved_image_path):
            try:
                subprocess.run(['start', '', self.saved_image_path], shell=True, check=True)
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to open image")

    def update_previews(self):
        if self.color_img is not None:
            color_rgb = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2RGB)
            color_img = Image.fromarray(color_rgb)
            color_img = ImageTk.PhotoImage(color_img)
            self.canvas_color.create_image(0, 0, anchor=tk.NW, image=color_img)
            self.canvas_color.image = color_img
        if self.gray_img is not None:
            gray_img = Image.fromarray(self.gray_img)
            gray_img = ImageTk.PhotoImage(gray_img)
            self.canvas_gray.create_image(0, 0, anchor=tk.NW, image=gray_img)
            self.canvas_gray.image = gray_img

    def save_image(self, img_type):
        """
        Save the processed image in the specified format.
        
        Args:
            img_type: String indicating the type of image to save ('color' or 'gray')
        
        Features:
        - Creates save directory if it doesn't exist
        - Handles different file formats (JPEG/PNG)
        - Applies compression settings
        - Copies file path to clipboard
        - Shows success message
        """
        if self.cropped_face is None:
            messagebox.showwarning("Warning", "No face selected to save")
            return
            
        # Ensure save directory exists
        os.makedirs(self.save_path, exist_ok=True)
        
        # Get current values from entries
        current_path = self.path_entry.get()
        current_filename = self.filename_entry.get()
        
        # Handle filename formatting
        filename = current_filename if self.from_access else current_filename
        if self.from_access and not filename.lower().endswith('.jpg'):
            filename = os.path.splitext(filename)[0] + '.jpg'
        self.saved_image_path = os.path.join(current_path, filename)
        img_format = 'jpeg' if self.from_access else self.format_var.get().lower()
        compression = self.compression_scale_value if hasattr(self, 'compression_scale_value') else 95
        if img_type == "color":
            params = [cv2.IMWRITE_JPEG_QUALITY, compression] if img_format == "jpeg" else [cv2.IMWRITE_PNG_COMPRESSION, int((100 - compression) / 10)]
            cv2.imwrite(self.saved_image_path, self.color_img, params)
        elif img_type == "gray":
            params = [cv2.IMWRITE_JPEG_QUALITY, compression] if img_format == "jpeg" else [cv2.IMWRITE_PNG_COMPRESSION, int((100 - compression) / 10)]
            cv2.imwrite(self.saved_image_path, self.gray_img, params)
        self.saved_path_entry.config(state='normal')
        self.saved_path_entry.delete(0, tk.END)
        self.saved_path_entry.insert(0, self.saved_image_path)
        self.saved_path_entry.config(state='readonly')
        pyperclip.copy(self.saved_image_path)
        messagebox.showinfo("Success", f"Image saved to {self.saved_image_path}\nPath copied to clipboard")
        self.root.quit()

    def reset_capture(self):
        self.cropped_face = None
        self.color_img = None
        self.gray_img = None
        self.canvas_color.delete("all")
        self.canvas_gray.delete("all")
        self.brightness_scale.set(0)
        self.contrast_scale.set(1.0)
        self.sharpness_scale.set(1.0)
        self.noise_scale.set(0)
        self.saturation_scale.set(1.0)
        self.gamma_scale.set(1.0)
        self.equalize_var.set(False)
        self.background_var.set("White")
        self.format_var.set("JPEG")
        self.compression_scale.set(95)
        self.saved_path_entry.config(state='normal')
        self.saved_path_entry.delete(0, tk.END)
        self.saved_path_entry.config(state='readonly')
        self.saved_image_path = ""

    def browse_path(self):
        """Open directory selection dialog and update save path"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            initialdir=self.path_entry.get(),
            title="Select Directory for Saving Images"
        )
        if directory:  # If a directory was selected
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)
            self.save_path = directory

    def toggle_auto_capture(self):
        self.auto_capture = self.auto_capture_var.get()
        if self.auto_capture:
            self.auto_capture_start = None
            self.best_frame = None
            self.best_score = -1

    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()

def run_image_utility(save_path, filename, from_access=False):
    """Run the Image Utility App with given save path and filename."""
    root = tk.Tk()
    app = ImageUtilityApp(root, save_path, filename, from_access)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        save_path = sys.argv[1]
        filename = sys.argv[2]
        run_image_utility(save_path, filename, from_access=True)
    else:
        print("Usage: python script.py <save_path> <filename>")
        sys.exit(1)