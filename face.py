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
import logging  # For error tracking
import traceback  # For detailed error information
from datetime import datetime, timedelta

# Set up logging with error-only configuration
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face_utility.log')

# Clear log file if older than 2 days
if os.path.exists(log_path):
    try:
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(log_path))
        if datetime.now() - file_mod_time > timedelta(days=2):
            open(log_path, 'w').close()  # Clear the file
    except Exception:
        pass

# Configure logging for errors only with detailed format
logging.basicConfig(
    filename=log_path,
    level=logging.ERROR,  # Only log errors and critical issues
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
    filemode='a'  # Append mode
)

def log_error(message, exc_info=None):
    """Log error with function and line information"""
    try:
        frame = traceback.extract_stack()[-2]  # Get caller frame
        logging.error(f"{frame.filename}:{frame.lineno} - {frame.name}() - {message}", exc_info=exc_info)
    except Exception:
        logging.error(message, exc_info=exc_info)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler"""
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_text = ''.join(tb_lines)
    logging.error(f"Uncaught exception: {str(exc_value)}\n{tb_text}")
    try:
        messagebox.showerror("Error", f"An error occurred: {str(exc_value)}\nCheck face_utility.log for details")
    except Exception:
        pass

class ImageUtilityApp:
    """
    A comprehensive GUI application for capturing, processing, and saving face photos.
    Provides real-time face detection, image enhancement, and multiple output formats.
    """
    def __init__(self, root, save_path, filename, from_access=False, grayscale_only=False, auto_close=False, show_messages=True):
        """
        Initialize the Image Utility Application
        
        Args:
            root: Tkinter root window
            save_path: Directory path where images will be saved
            filename: Name for the saved image file
            from_access: Boolean indicating if app is launched from Access database
            grayscale_only: Boolean indicating if only grayscale should be saved automatically
            auto_close: Boolean indicating if app should close automatically after saving
            show_messages: Boolean indicating if success/error messages should be displayed
        """
        # Initialize main window properties
        self.root = root
        self.save_path = save_path
        self.filename = filename
        self.from_access = from_access
        self.grayscale_only = grayscale_only
        self.auto_close = auto_close
        self.show_messages = show_messages
        self.root.title("Image Utility App")
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        
        # Auto brightness adjustment settings
        self.last_brightness_check = 0  # Timestamp of last brightness check
        self.auto_brightness_enabled = True  # Enable automatic brightness adjustment

        # Default filter values
        self.noise_value = 0
        self.saturation_value = 1.0
        self.brightness_value = 0
        self.contrast_value = 1.0
        self.sharpness_value = 1.0
        self.gamma_value = 1.0

        # Initialize webcam capture with DirectShow on Windows for fastest startup
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                log_error("Cannot open webcam - camera not available or in use")
                messagebox.showerror("Error", "Cannot open webcam. Ensure camera is plugged in and not in use by another app.")
                self.close_app()
                return
        except Exception as e:
            log_error(f"Failed to initialize webcam: {str(e)}", exc_info=True)
            messagebox.showerror("Error", "Cannot open webcam")
            self.close_app()
            return

        # Load Haar Cascade Classifiers for face and eye detection
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
            face_cascade_path = os.path.join(application_path, 'haarcascades', 'haarcascade_frontalface_default.xml')
            eye_cascade_path = os.path.join(application_path, 'haarcascades', 'haarcascade_eye.xml')
        else:
            face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
            
        try:
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
            if self.face_cascade.empty() or self.eye_cascade.empty():
                log_error(f"Failed to load cascade classifiers - face: {face_cascade_path}, eye: {eye_cascade_path}")
                messagebox.showerror("Error", "Failed to load detection models")
                self.close_app()
                return
        except Exception as e:
            log_error(f"Error loading cascade classifiers: {str(e)}", exc_info=True)
            messagebox.showerror("Error", "Failed to load detection models")
            self.close_app()
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
        self.capture_success_time = None # Timestamp when capture was successful

        # ==================== GUI Elements (Classic Original Layout) ====================
        # Row 1: File Path & Filename
        self.input_frame = tk.Frame(root)
        tk.Label(self.input_frame, text="File Path:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.path_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 10))
        self.path_entry.insert(0, save_path)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        self.browse_button = tk.Button(self.input_frame, text="Browse", font=("Arial", 10, "bold"), command=self.browse_path)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        tk.Label(self.input_frame, text="Filename:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.filename_entry = tk.Entry(self.input_frame, width=30, font=("Arial", 10))
        self.filename_entry.insert(0, filename)
        self.filename_entry.pack(side=tk.LEFT, padx=5)

        # Row 2: Saved Image Path & Theme Toggle
        self.saved_frame = tk.Frame(root)
        self.saved_frame.pack(fill=tk.X, padx=5, pady=(2, 0))
        
        self.theme_var = tk.BooleanVar(value=True)  # True for dark theme
        self.theme_button = tk.Checkbutton(
            self.saved_frame, 
            text="Dark Theme", 
            variable=self.theme_var, 
            font=("Arial", 10, "bold"),
            command=self.toggle_theme
        )
        self.theme_button.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(self.saved_frame, text="Saved Image:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.saved_path_entry = tk.Entry(self.saved_frame, width=50, font=("Arial", 10))
        self.saved_path_entry.config(state='readonly')
        self.saved_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.saved_path_entry.bind("<Double-Button-1>", self.view_saved_image)

        # Row 3: Controls (RETAKE, Auto-Capture, Background, Format, Quality)
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(fill=tk.X, padx=5, pady=3)
        self.button_row = tk.Frame(self.control_frame)
        self.button_row.pack(fill=tk.X, pady=2)
        
        self.retake_button = tk.Button(self.button_row, text="RETAKE", font=("Arial", 10, "bold"), command=self.reset_capture)
        self.retake_button.pack(side=tk.LEFT, padx=5)
        
        self.auto_capture_var = tk.BooleanVar(value=False)
        self.auto_capture_check = tk.Checkbutton(
            self.button_row, 
            text="Auto-Capture", 
            font=("Arial", 10, "bold"), 
            variable=self.auto_capture_var, 
            command=self.toggle_auto_capture
        )
        self.auto_capture_check.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.button_row, text="Background:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.background_var = tk.StringVar(value="White")
        self.background_menu = ttk.Combobox(
            self.button_row, 
            textvariable=self.background_var, 
            values=["White", "Light Gray", "Dark Gray", "Light Blue"], 
            width=12, 
            font=("Arial", 9),
            state="readonly"
        )
        self.background_menu.pack(side=tk.LEFT, padx=2)
        self.background_menu.bind("<<ComboboxSelected>>", self.apply_filters)
        
        tk.Label(self.button_row, text="Format:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.format_var = tk.StringVar(value="JPEG")
        self.format_menu = ttk.Combobox(
            self.button_row, 
            textvariable=self.format_var, 
            values=["JPEG", "PNG"], 
            width=8, 
            font=("Arial", 9),
            state="readonly"
        )
        self.format_menu.pack(side=tk.LEFT, padx=2)
        
        tk.Label(self.button_row, text="Quality:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.compression_scale = tk.Scale(self.button_row, from_=0, to=100, orient=tk.HORIZONTAL, length=120, font=("Arial", 9))
        self.compression_scale.set(95)
        self.compression_scale.pack(side=tk.LEFT, padx=2)

        # Keyboard shortcuts
        self.root.bind("<space>", lambda e: self.on_space_key())
        self.root.bind("<Return>", lambda e: self.on_return_key())
        self.root.bind("<Escape>", lambda e: self.reset_capture())

        # Main content area: Live Preview (Left) & Previews (Right)
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left side: Live feed
        self.left_container = tk.Frame(self.main_frame)
        self.left_container.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        self.live_preview_label = tk.Label(
            self.left_container, 
            text="Live Preview", 
            font=('Arial', 14, 'bold'),
            fg='#4CAF50'
        )
        self.live_preview_label.pack(anchor='nw', pady=(0, 5))

        self.canvas = tk.Canvas(self.left_container, width=640, height=480, bg='black', cursor="crosshair")
        self.canvas.pack()
        self.border_colors = ['#4CAF50', '#2196F3', '#9C27B0', '#F44336']  # Green, Blue, Purple, Red
        self.current_border_color = 0
        self.update_border_color()

        # Right side: Previews (Color & Grayscale side-by-side)
        self.preview_frame = tk.Frame(self.main_frame)
        self.preview_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.click_to_save_label = tk.Label(self.preview_frame, text="Click to Save:", font=('Arial', 12, 'bold'))
        self.click_to_save_label.pack(pady=(0, 10))

        # Side-by-side preview panels
        self.previews_row = tk.Frame(self.preview_frame)
        self.previews_row.pack()

        # Color preview (left)
        self.preview_color = tk.Frame(self.previews_row)
        self.preview_color.pack(side=tk.LEFT, padx=(0, 10))
        self.canvas_color = tk.Canvas(self.preview_color, width=250, height=300, bg='white', cursor="hand2")
        self.canvas_color.pack()
        self.canvas_color.configure(highlightthickness=2, highlightbackground='#4CAF50')  # Green border
        self.color_text_label = tk.Label(self.preview_color, text="Color", font=('Arial', 10, 'bold'))
        self.color_text_label.pack(pady=(5, 0))

        # Grayscale preview (right)
        self.preview_gray = tk.Frame(self.previews_row)
        self.preview_gray.pack(side=tk.LEFT)
        self.canvas_gray = tk.Canvas(self.preview_gray, width=250, height=300, bg='white', cursor="hand2")
        self.canvas_gray.pack()
        self.canvas_gray.configure(highlightthickness=2, highlightbackground='#607D8B')  # Blue-gray border
        self.gray_text_label = tk.Label(self.preview_gray, text="Grayscale", font=('Arial', 10, 'bold'))
        self.gray_text_label.pack(pady=(5, 0))

        # Bind clicks to save
        self.canvas_color.bind("<Button-1>", lambda e: self.save_image("color"))
        self.canvas_gray.bind("<Button-1>", lambda e: self.save_image("gray"))

        # Bind mouse events for live feed
        self.canvas.bind("<Button-1>", self.select_face)
        self.manual_crop = False
        self.crop_start = None
        self.crop_end = None
        self.canvas.bind("<ButtonPress-3>", self.start_manual_crop)
        self.canvas.bind("<B3-Motion>", self.update_manual_crop)
        self.canvas.bind("<ButtonRelease-3>", self.end_manual_crop)

        # Set window size to match classic UI (1400x750)
        self.root.geometry("1400x750")
        self.root.minsize(1300, 700)

        # Apply initial theme
        self.toggle_theme()

        # Start live video feed loop
        self.update_feed()

    def update_feed(self):
        """
        Main method for updating the video feed and processing each frame.
        Handles:
        - Webcam capture
        - Auto brightness adjustment
        - Face detection
        - Guide box drawing
        - Countdown and auto-capture
        - Display updates
        """
        # Capture frame from webcam with retry during warmup
        try:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                for _ in range(10):
                    time.sleep(0.1)
                    ret, frame = self.cap.read()
                    if ret and frame is not None:
                        break
            if not ret or frame is None:
                log_error("Failed to capture webcam feed - camera disconnected or unavailable")
                messagebox.showerror("Error", "Failed to capture webcam feed. Please check webcam connection.")
                self.close_app()
                return
        except Exception as e:
            log_error(f"Error reading from webcam: {str(e)}", exc_info=True)
            messagebox.showerror("Error", "Failed to capture webcam feed")
            self.close_app()
            return
        
        # Automatic brightness adjustment system (checks every 0.5s)
        if self.auto_brightness_enabled and time.time() - self.last_brightness_check > 0.5:
            gray_check = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray_check)
            if avg_brightness < 80:  # Low light
                frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=25)
            elif avg_brightness > 180:  # High light
                frame = cv2.convertScaleAbs(frame, alpha=0.8, beta=-15)
            self.last_brightness_check = time.time()

        # Apply live filters to feed
        img = frame.copy()
        if self.noise_value > 0:
            img = cv2.GaussianBlur(img, (2 * self.noise_value + 1, 2 * self.noise_value + 1), 0)
        if self.saturation_value != 1.0:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * self.saturation_value, 0, 255).astype(np.uint8)
            img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        img = cv2.convertScaleAbs(img, alpha=1.3, beta=30)
        kernel = np.array([[-1, -1, -1], [-1, 9 * self.sharpness_value, -1], [-1, -1, -1]])
        img = cv2.filter2D(img, -1, kernel)
        if self.gamma_value != 1.0:
            inv_gamma = 1.0 / self.gamma_value
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
            img = cv2.LUT(img, table)
        if self.background_var.get() != "None":
            img = self.apply_background(img, self.background_var.get())

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        self.faces = faces

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

        # Track face detection timing for countdown
        if len(faces) > 0 and self.cropped_face is None:
            if self.face_detected_time is None:  # Face appeared
                self.face_detected_time = time.time()
            elapsed = time.time() - self.face_detected_time
            if elapsed <= 3:  # Show countdown for 3 seconds
                countdown = 3 - int(elapsed)
                text = f"Capturing in: {countdown}"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
                text_x = (img.shape[1] - text_size[0]) // 2
                text_y = img.shape[0] // 2 - 50
                cv2.rectangle(img, (text_x - 10, text_y - 40), (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)
                cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            elif not self.auto_capture:  # After 3 seconds, trigger auto-capture
                self.auto_capture = True
                self.auto_capture_var.set(True)
                self.auto_capture_start = time.time()
        else:
            self.face_detected_time = None
        
        self.last_face_count = len(faces)

        # Draw detected face boxes and eyes
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

        # Show capture success message on video feed
        if self.capture_success_time is not None:
            elapsed = time.time() - self.capture_success_time
            if elapsed <= 1:  # Show for 1 second
                text = "Face Captured Successfully"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
                text_x = (img.shape[1] - text_size[0]) // 2
                text_y = img.shape[0] // 2
                cv2.rectangle(img, (text_x - 15, text_y - 35), (text_x + text_size[0] + 15, text_y + 10), (0, 0, 0), -1)
                cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            else:
                # Close app automatically after 1 second if auto_close is enabled
                if self.auto_close:
                    self.close_app()
                    return
                self.capture_success_time = None

        # Display frame on canvas
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_tk = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img_tk)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

        if self.cropped_face is not None:
            self.update_previews()

        # Handle Auto-capture execution
        if self.auto_capture:
            if self.auto_capture_start is None:
                self.auto_capture_start = time.time()
                frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
                
            elapsed = time.time() - self.auto_capture_start
            if elapsed < 3:
                score = self.evaluate_frame(frame, faces)
                if score > 2.0:  # Immediate high-quality capture
                    self.best_frame = frame.copy()
                    self.best_score = score
                    elapsed = 3
                elif score > self.best_score:
                    self.best_score = score
                    self.best_frame = frame.copy()
            else:
                if self.best_frame is not None and len(faces) > 0:
                    self.best_frame = cv2.convertScaleAbs(self.best_frame, alpha=1.2, beta=15)
                    self.auto_capture_face()
                elif len(faces) > 0:
                    self.best_frame = frame.copy()
                    self.auto_capture_face()
                self.auto_capture = False
                self.auto_capture_var.set(False)
                self.auto_capture_start = None
                self.best_frame = None
                self.best_score = -1
                self.face_detected_time = None

        self.root.after(15, self.update_feed)

    def evaluate_frame(self, frame, faces):
        """
        Evaluate frame quality for auto-capture.
        Considers centering, size, eye detection, brightness.
        """
        if len(faces) != 1:
            return -1
            
        (x, y, w, h) = faces[0]
        frame_center_x = frame.shape[1] // 2
        face_center_x = x + w // 2
        centering_score = 1 - abs(frame_center_x - face_center_x) / frame.shape[1]
        size_score = min(w * h / (frame.shape[0] * frame.shape[1]) * 4, 1.0)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_roi = gray[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
        eye_score = 1 if len(eyes) >= 2 else 0
        
        avg_brightness = np.mean(face_roi)
        if avg_brightness < 50 or avg_brightness > 200:
            return -1
            
        return centering_score + eye_score + size_score

    def auto_capture_face(self):
        """Perform automatic capture on the best evaluated frame"""
        if self.best_frame is None:
            return
        gray = cv2.cvtColor(self.best_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            self.capture_face(self.best_frame, x, y, w, h)

    def select_face(self, event):
        """Manual click on face to capture immediately"""
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
        """
        frame_aspect = frame.shape[1] / frame.shape[0]
        
        # Add padding around face (100% horizontal, 120% vertical)
        padding_x = int(w * 1.0)
        padding_y = int(h * 1.2)
        
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
        
        # Auto-save after capture
        self.auto_save_after_capture()
        
        # Set capture success time for confirmation message overlay
        self.capture_success_time = time.time()
        
        # Play beep sound on capture
        try:
            self.root.bell()
        except Exception:
            pass

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
        if (x2 - x1) > 20 and (y2 - y1) > 20:
            self.cropped_face = frame[y1:y2, x1:x2]
            self.cropped_face = cv2.resize(self.cropped_face, (200, 250))
            self.apply_filters()
            self.auto_save_after_capture()
            self.capture_success_time = time.time()
            try:
                self.root.bell()
            except Exception:
                pass
        self.crop_start = None
        self.crop_end = None

    def auto_save_after_capture(self):
        """
        Automatically save images after capture based on configuration.
        Saves grayscale only if grayscale_only is True, otherwise saves both color and grayscale.
        """
        if self.cropped_face is None:
            return
            
        # Ensure save directory exists
        try:
            os.makedirs(self.save_path, exist_ok=True)
        except Exception as e:
            log_error(f"Failed to create save directory {self.save_path}: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Cannot create save directory: {self.save_path}")
            return
        
        # Get current values from entries
        current_path = self.path_entry.get().strip()
        current_filename = self.filename_entry.get().strip()
        
        # Handle filename formatting
        filename = current_filename
        if self.from_access and not filename.lower().endswith('.jpg'):
            filename = os.path.splitext(filename)[0] + '.jpg'
            
        img_format = 'jpeg' if self.from_access else self.format_var.get().lower()
        compression = self.compression_scale.get() if hasattr(self, 'compression_scale') and hasattr(self.compression_scale, 'get') else 95
        params = [cv2.IMWRITE_JPEG_QUALITY, compression] if img_format == "jpeg" else [cv2.IMWRITE_PNG_COMPRESSION, int((100 - compression) / 10)]
        
        try:
            if self.grayscale_only:
                # Save only grayscale version
                self.saved_image_path = os.path.join(current_path, filename)
                success = cv2.imwrite(self.saved_image_path, self.gray_img, params)
                if not success:
                    log_error(f"Failed to save grayscale image to {self.saved_image_path}")
                    return
            else:
                # Save both color and grayscale versions
                color_filename = os.path.splitext(filename)[0] + '_color' + os.path.splitext(filename)[1]
                color_path = os.path.join(current_path, color_filename)
                success1 = cv2.imwrite(color_path, self.color_img, params)
                
                gray_filename = os.path.splitext(filename)[0] + '_gray' + os.path.splitext(filename)[1]
                gray_path = os.path.join(current_path, gray_filename)
                success2 = cv2.imwrite(gray_path, self.gray_img, params)
                
                if not success1 or not success2:
                    log_error(f"Failed to save images - color: {success1}, gray: {success2}")
                    return
                
                self.saved_image_path = color_path
        except Exception as e:
            log_error(f"Error saving images: {str(e)}", exc_info=True)
            messagebox.showerror("Error", "Failed to save image")
            return
        
        # Update the saved path entry
        try:
            self.saved_path_entry.config(state='normal')
            self.saved_path_entry.delete(0, tk.END)
            self.saved_path_entry.insert(0, self.saved_image_path)
            self.saved_path_entry.config(state='readonly')
            pyperclip.copy(self.saved_image_path)
        except Exception:
            pass
        
        # Show success message if configured
        if self.auto_close and self.show_messages:
            messagebox.showinfo("Success", f"Image saved to {self.saved_image_path}\nPath copied to clipboard")
            self.close_app()

    def auto_enhance(self):
        if self.cropped_face is None:
            messagebox.showwarning("Warning", "No face selected to enhance")
            return
        self.brightness_value = 20
        self.contrast_value = 1.3
        self.sharpness_value = 1.5
        self.noise_value = 1
        self.saturation_value = 1.2
        self.gamma_value = 1.0
        self.apply_filters()

    def apply_filters(self, _=None):
        """Apply basic image processing to the cropped face image."""
        if self.cropped_face is None:
            return
            
        img = self.cropped_face.copy()
        if self.background_var.get() != "None":
            img = self.apply_background(img, self.background_var.get())
            
        self.color_img = img
        self.gray_img = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2GRAY)
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
            except Exception as e:
                log_error(f"Error opening image {self.saved_image_path}: {str(e)}", exc_info=True)

    def update_previews(self):
        if self.color_img is not None and hasattr(self, 'canvas_color'):
            color_rgb = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2RGB)
            color_img = Image.fromarray(color_rgb)
            color_img = ImageTk.PhotoImage(color_img)
            self.canvas_color.create_image(0, 0, anchor=tk.NW, image=color_img)
            self.canvas_color.image = color_img
        if self.gray_img is not None and hasattr(self, 'canvas_gray'):
            gray_img = Image.fromarray(self.gray_img)
            gray_img = ImageTk.PhotoImage(gray_img)
            self.canvas_gray.create_image(0, 0, anchor=tk.NW, image=gray_img)
            self.canvas_gray.image = gray_img

    def save_image(self, img_type):
        """Save the selected image format manually (when user clicks preview) and close."""
        if self.cropped_face is None:
            messagebox.showwarning("Warning", "No face selected to save")
            return
            
        try:
            os.makedirs(self.save_path, exist_ok=True)
        except Exception as e:
            log_error(f"Cannot create save directory {self.save_path}: {str(e)}")
            messagebox.showerror("Error", f"Cannot create save directory: {self.save_path}")
            return
            
        current_path = self.path_entry.get().strip()
        current_filename = self.filename_entry.get().strip()
        
        filename = current_filename
        if self.from_access and not filename.lower().endswith('.jpg'):
            filename = os.path.splitext(filename)[0] + '.jpg'
        self.saved_image_path = os.path.join(current_path, filename)
        img_format = 'jpeg' if self.from_access else self.format_var.get().lower()
        compression = self.compression_scale.get() if hasattr(self, 'compression_scale') and hasattr(self.compression_scale, 'get') else 95
        params = [cv2.IMWRITE_JPEG_QUALITY, compression] if img_format == "jpeg" else [cv2.IMWRITE_PNG_COMPRESSION, int((100 - compression) / 10)]
        
        try:
            if img_type == "color":
                success = cv2.imwrite(self.saved_image_path, self.color_img, params)
            else:
                success = cv2.imwrite(self.saved_image_path, self.gray_img, params)
            
            if not success:
                log_error(f"Failed to save {img_type} image to {self.saved_image_path}")
                messagebox.showerror("Error", "Failed to save image")
                return
        except Exception as e:
            log_error(f"Error saving {img_type} image: {str(e)}", exc_info=True)
            messagebox.showerror("Error", "Failed to save image")
            return
            
        try:
            self.saved_path_entry.config(state='normal')
            self.saved_path_entry.delete(0, tk.END)
            self.saved_path_entry.insert(0, self.saved_image_path)
            self.saved_path_entry.config(state='readonly')
            pyperclip.copy(self.saved_image_path)
        except Exception:
            pass
            
        if self.show_messages:
            messagebox.showinfo("Success", f"Image saved to {self.saved_image_path}\nPath copied to clipboard")
            
        self.close_app()

    def reset_capture(self):
        """Reset capture state and resume live camera feed"""
        self.cropped_face = None
        self.color_img = None
        self.gray_img = None
        self.capture_success_time = None
        self.auto_capture = False
        self.auto_capture_start = None
        self.face_detected_time = None
        if hasattr(self, 'canvas_color'):
            self.canvas_color.delete("all")
        if hasattr(self, 'canvas_gray'):
            self.canvas_gray.delete("all")
        self.background_var.set("White")
        self.format_var.set("JPEG")
        if hasattr(self, 'compression_scale'):
            self.compression_scale.set(95)
        if hasattr(self, 'saved_path_entry'):
            self.saved_path_entry.config(state='normal')
            self.saved_path_entry.delete(0, tk.END)
            self.saved_path_entry.config(state='readonly')
        self.saved_image_path = ""

    def on_space_key(self):
        """Space key triggers capture or reset"""
        if self.cropped_face is None and hasattr(self, 'faces') and len(self.faces) > 0:
            ret, frame = self.cap.read()
            if ret and frame is not None:
                (x, y, w, h) = self.faces[0]
                self.capture_face(frame, x, y, w, h)
        else:
            self.reset_capture()

    def on_return_key(self):
        """Enter key confirms and saves image"""
        if self.cropped_face is not None:
            save_type = "gray" if self.grayscale_only else "color"
            self.save_image(save_type)

    def browse_path(self):
        """Open directory selection dialog and update save path"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            initialdir=self.path_entry.get(),
            title="Select Directory for Saving Images"
        )
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)
            self.save_path = directory

    def toggle_auto_capture(self):
        self.auto_capture = self.auto_capture_var.get()
        if self.auto_capture:
            self.auto_capture_start = None
            self.best_frame = None
            self.best_score = -1
            self.face_detected_time = None

    def update_border_color(self):
        """Update the live preview border color for animated cycle effect"""
        try:
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                self.canvas.configure(
                    highlightthickness=2,
                    highlightbackground=self.border_colors[self.current_border_color]
                )
                self.current_border_color = (self.current_border_color + 1) % len(self.border_colors)
                self.root.after(1000, self.update_border_color)
        except Exception:
            pass

    def toggle_theme(self):
        """Toggle between light and dark theme safely across widgets"""
        is_dark = self.theme_var.get()
        bg_color = '#2C2C2C' if is_dark else '#F0F0F0'
        fg_color = '#FFFFFF' if is_dark else '#000000'
        input_bg = '#3C3C3C' if is_dark else '#FFFFFF'
        
        self.root.configure(bg=bg_color)
        
        for frame_attr in ['input_frame', 'saved_frame', 'control_frame', 'button_row', 
                           'main_frame', 'left_container', 'preview_frame', 'previews_row', 
                           'preview_color', 'preview_gray']:
            if hasattr(self, frame_attr):
                try:
                    getattr(self, frame_attr).configure(bg=bg_color)
                except Exception:
                    pass

        for entry_attr in ['path_entry', 'filename_entry', 'saved_path_entry']:
            if hasattr(self, entry_attr):
                try:
                    getattr(self, entry_attr).configure(bg=input_bg, fg=fg_color, insertbackground=fg_color)
                except Exception:
                    pass

        for btn_attr in ['browse_button', 'retake_button']:
            if hasattr(self, btn_attr):
                try:
                    getattr(self, btn_attr).configure(bg=input_bg, fg=fg_color)
                except Exception:
                    pass

        for label_attr in ['live_preview_label', 'click_to_save_label', 'color_text_label', 'gray_text_label']:
            if hasattr(self, label_attr):
                try:
                    widget = getattr(self, label_attr)
                    if label_attr == 'live_preview_label':
                        widget.configure(bg=bg_color, fg='#4CAF50')
                    else:
                        widget.configure(bg=bg_color, fg=fg_color)
                except Exception:
                    pass

        if hasattr(self, 'theme_button'):
            try:
                self.theme_button.configure(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color)
            except Exception:
                pass
        if hasattr(self, 'auto_capture_check'):
            try:
                self.auto_capture_check.configure(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color)
            except Exception:
                pass

    def close_app(self):
        """Release camera and destroy window cleanly."""
        try:
            if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass
        try:
            self.root.quit()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def __del__(self):
        try:
            if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass

def run_image_utility(save_path, filename, from_access=False, grayscale_only=False, auto_close=False, show_messages=True):
    """Run the Image Utility App with given save path and filename."""
    try:
        if from_access:
            save_path = save_path.rstrip('\\/')
            if filename in save_path:
                save_path = save_path.replace(filename, '').rstrip('\\/" ')
            
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path, exist_ok=True)
                except Exception as e:
                    log_error(f"Failed to create directory {save_path}: {str(e)}", exc_info=True)
                    messagebox.showerror("Error", f"Cannot create directory: {save_path}")
                    return ""
        
        root = tk.Tk()
        app = ImageUtilityApp(root, save_path, filename, from_access, grayscale_only, auto_close, show_messages)
        root.mainloop()
        try:
            app.close_app()
        except Exception:
            pass
        
        if app.saved_image_path and os.path.exists(app.saved_image_path):
            return app.saved_image_path
        return ""
    except Exception as e:
        log_error(f"Error in run_image_utility: {str(e)}", exc_info=True)
        messagebox.showerror("Error", f"Failed to run application: {str(e)}")
        return ""

if __name__ == "__main__":
    try:
        sys.excepthook = handle_exception
        
        # Auto-recover if Windows quote escaping (e.g. \" from trailing backslash) merged arguments
        if len(sys.argv) == 2 and '"' in sys.argv[1]:
            parts = [p.strip() for p in sys.argv[1].split('"') if p.strip()]
            sys.argv = [sys.argv[0]] + parts

        if len(sys.argv) >= 3:
            save_path = sys.argv[1].strip('"')  # Remove any surrounding quotes
            filename = sys.argv[2].strip('"')   # Remove any surrounding quotes
            grayscale_only = len(sys.argv) > 3 and sys.argv[3].lower() == 'grayscale'
            auto_close = len(sys.argv) > 4 and sys.argv[4].lower() == 'autoclose'
            show_messages = not (len(sys.argv) > 5 and sys.argv[5].lower() == 'silent')
            from_access = True  # Set to True when running from command line
            
            # Auto-enable auto_close when grayscale_only and from_access are both true
            if grayscale_only and from_access:
                auto_close = True
            # Auto-disable messages for fully automated mode
            if grayscale_only and auto_close:
                show_messages = False
            
            # Remove trailing backslashes from save_path
            save_path = save_path.rstrip('\\/')
            
            # Clean up the save_path by removing any file name that might have been appended
            if filename in save_path:
                save_path = save_path.replace(filename, '').rstrip('\\/" ')
            
            # Verify paths and create directory if needed
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path, exist_ok=True)
                except Exception as e:
                    log_error(f"Failed to create directory {save_path}: {str(e)}", exc_info=True)
                    messagebox.showerror("Error", f"Failed to create save directory: {save_path}")
                    sys.exit(1)
            
            run_image_utility(save_path, filename, from_access=from_access, grayscale_only=grayscale_only, auto_close=auto_close, show_messages=show_messages)
        else:
            log_error(f"Invalid number of arguments provided: {len(sys.argv)} - Expected at least 3. Received: {sys.argv}")
            print(f"Usage: python face.py <save_path> <filename> [grayscale] [autoclose] [silent]\nReceived: {sys.argv}")
            sys.exit(1)
            
    except Exception as e:
        log_error(f"Fatal application error: {str(e)}", exc_info=True)
        messagebox.showerror("Critical Error", f"Application failed to start: {str(e)}\nCheck face_utility.log for details")
        sys.exit(1)