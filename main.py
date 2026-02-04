
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import ImageProcessor
from history_manager import HistoryManager


class ImageProcessingApp:
    "Testing"
    def __init__(self, master):
        """Constructor - initializes the application"""
        self.master = master
        self.master.title(" OPENCV Application - HIT137 Assignment 3")
        self.master.geometry("1000x700")
        
        # Private attributes (Encapsulation)
        self._current_image = None
        self._original_image = None
        self._display_image = None
        self._filename = None
        
        # Class Interaction - using other classes
        self.processor = ImageProcessor()
        self.history = HistoryManager()
        
        # Create GUI components
        self.createMenus()
        self.createToolbar()
        self.createWidgets()
        self.createStatusBar()
        
    def createMenus(self):
         # Main menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        # File menu
        fileMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.openImage)
        fileMenu.add_command(label="Save", command=self.saveImage)
        fileMenu.add_command(label="Save As...", command=self.saveImageAs)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exitApp)
        
        # Edit menu
        editMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Undo", command=self.undo)
        editMenu.add_command(label="Redo", command=self.redo)
        editMenu.add_separator()
        editMenu.add_command(label="Reset to Original", command=self.resetImage)
        
    def createToolbar(self):
        toolbar = Frame(self.master, bg="lightgray", bd=1, relief=RAISED)
        
        
        Button(toolbar, text="Open", command=self.openImage).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Save", command=self.saveImage).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Undo", command=self.undo).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Redo", command=self.redo).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Reset", command=self.resetImage).pack(side=LEFT, padx=2, pady=2)
        
        toolbar.pack(side=TOP, fill=X)
        
    def createWidgets(self):
         # Main container
        mainFrame = Frame(self.master)
        mainFrame.pack(fill=BOTH, expand=True)
        
        # Left panel for controls
        self.createControlPanel(mainFrame)
        
        # Right panel for image display
        self.createImagePanel(mainFrame)
        
    def createControlPanel(self, parent):
        controlFrame = Frame(parent, width=280, bg="#e0e0e0", relief=RIDGE, bd=2)
        controlFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        controlFrame.pack_propagate(False)
        
        # Title
        Label(controlFrame, text="Image Processing Controls", 
              font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=10)
        
        # === FILTERS SECTION ===
        filterFrame = LabelFrame(controlFrame, text="Filters", 
                                font=("Arial", 10, "bold"), bg="#e0e0e0")
        filterFrame.pack(fill=X, padx=10, pady=5)
        
        Button(filterFrame, text="Grayscale", width=22, 
               command=self.applyGrayscale).pack(pady=3)
        Button(filterFrame, text="Edge Detection", width=22, 
               command=self.applyEdgeDetection).pack(pady=3)
        
        # Blur with slider
        Label(filterFrame, text="Blur Intensity:", bg="#e0e0e0").pack(pady=(5, 0))
        self.blurScale = Scale(filterFrame, from_=1, to=50, orient=HORIZONTAL, 
                              length=220, command=self.applyBlur)
        self.blurScale.set(5)
        self.blurScale.pack(pady=3)
        
        # === ADJUSTMENTS SECTION ===
        adjustFrame = LabelFrame(controlFrame, text="Adjustments", 
                                font=("Arial", 10, "bold"), bg="#e0e0e0")
        adjustFrame.pack(fill=X, padx=10, pady=5)
        
        # Brightness
        Label(adjustFrame, text="Brightness:", bg="#e0e0e0").pack(pady=(5, 0))
        self.brightnessScale = Scale(adjustFrame, from_=-100, to=100, 
                                    orient=HORIZONTAL, length=220, 
                                    command=self.adjustBrightness)
        self.brightnessScale.set(0)
        self.brightnessScale.pack(pady=3)
        
        # Contrast
        Label(adjustFrame, text="Contrast:", bg="#e0e0e0").pack(pady=(5, 0))
        self.contrastScale = Scale(adjustFrame, from_=-100, to=100, 
                                  orient=HORIZONTAL, length=220, 
                                  command=self.adjustContrast)
        self.contrastScale.set(0)
        self.contrastScale.pack(pady=3)
        
        Button(adjustFrame, text="Reset Adjustments", width=22, 
               command=self.resetAdjustments).pack(pady=5)
        
        # === TRANSFORMATIONS SECTION ===
        transformFrame = LabelFrame(controlFrame, text="Transformations", 
                                   font=("Arial", 10, "bold"), bg="#e0e0e0")
        transformFrame.pack(fill=X, padx=10, pady=5)
        
        # Rotation
        Label(transformFrame, text="Rotation:", bg="#e0e0e0", 
              font=("Arial", 9, "bold")).pack(pady=(5, 2))
        Button(transformFrame, text="Rotate 90°", width=22, 
               command=lambda: self.rotateImage(90)).pack(pady=2)
        Button(transformFrame, text="Rotate 180°", width=22, 
               command=lambda: self.rotateImage(180)).pack(pady=2)
        Button(transformFrame, text="Rotate 270°", width=22, 
               command=lambda: self.rotateImage(270)).pack(pady=2)
        
        # Flip
        Label(transformFrame, text="Flip:", bg="#e0e0e0", 
              font=("Arial", 9, "bold")).pack(pady=(10, 2))
        Button(transformFrame, text="Flip Horizontal", width=22, 
               command=lambda: self.flipImage("horizontal")).pack(pady=2)
        Button(transformFrame, text="Flip Vertical", width=22, 
               command=lambda: self.flipImage("vertical")).pack(pady=2)
        
        # Resize
        Label(transformFrame, text="Resize (%):", bg="#e0e0e0", 
              font=("Arial", 9, "bold")).pack(pady=(10, 2))
        resizeFrame = Frame(transformFrame, bg="#e0e0e0")
        resizeFrame.pack(pady=3)
        self.resizeEntry = Entry(resizeFrame, width=10)
        self.resizeEntry.insert(0, "100")
        self.resizeEntry.pack(side=LEFT, padx=2)
        Button(resizeFrame, text="Apply", command=self.resizeImage).pack(side=LEFT, padx=2)
        
    def createImagePanel(self, parent):
        """Create image display area"""
        imageFrame = Frame(parent, bg="white", relief=SUNKEN, bd=2)
        imageFrame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for displaying image
        self.canvas = Canvas(imageFrame, bg="#d0d0d0", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)
        
        # Placeholder text
        self.placeholderText = self.canvas.create_text(
            400, 250, 
            text="No image loaded\n\nClick 'Open' or use File > Open to load an image",
            font=("Arial", 14), fill="gray40", justify=CENTER
        )
        
    def createStatusBar(self):
        self.statusBar = Label(self.master, text="Ready", bd=1, 
                              relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)
        
    def updateStatus(self, message):
        """Update status bar message"""
        self.statusBar.config(text=message)
        self.master.update_idletasks()
        
    def openImage(self):
        filename = filedialog.askopenfilename(
            title="Open Image File",
            filetypes=[
                ("All Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp"),
                ("All Files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Load image using OpenCV
                image = cv2.imread(filename)
                if image is None:
                    raise ValueError("Unable to load image file")
                
                # Store image and reset state
                self._current_image = image
                self._original_image = image.copy()
                self._filename = filename
                
                # Initialize history
                self.history.clear()
                self.history.add_state(image.copy())
                
                # Reset adjustments
                self.resetAdjustments()
                
                # Display the image
                self.displayImage(image)
                
                # Update status with image info
                height, width = image.shape[:2]
                import os
                filename_only = os.path.basename(filename)
                self.updateStatus(f"Loaded: {filename_only} | Size: {width}x{height} pixels")
                
            except Exception as e:
                messagebox.showerror("Error Opening File", 
                                   f"Failed to open image:\n{str(e)}")
                
    def saveImage(self):
        """Save the current image"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "No image to save!")
            return
            
        if self._filename is None:
            self.saveImageAs()
            return
            
        try:
            cv2.imwrite(self._filename, self._current_image)
            import os
            filename_only = os.path.basename(self._filename)
            self.updateStatus(f"Saved: {filename_only}")
            messagebox.showinfo("Success", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error Saving", f"Failed to save image:\n{str(e)}")
            
    def saveImageAs(self):
        """Save image with a new filename"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "No image to save!")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG Files", "*.jpg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp")
            ]
        )
        
        if filename:
            try:
                cv2.imwrite(filename, self._current_image)
                self._filename = filename
                import os
                filename_only = os.path.basename(filename)
                self.updateStatus(f"Saved as: {filename_only}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error Saving", f"Failed to save image:\n{str(e)}")
                
    def exitApp(self):
        """Exit the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.master.quit()
            
    def displayImage(self, image):
        """Display image on canvas"""
        if image is None:
            return
            
        # Convert BGR to RGB for display
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        
        # Get canvas size
        self.master.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Resize image to fit canvas while maintaining aspect ratio
        if canvas_width > 1 and canvas_height > 1:
            pil_image.thumbnail((canvas_width - 20, canvas_height - 20), Image.LANCZOS)
        
        # Convert to PhotoImage
        self._display_image = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        x = canvas_width // 2 if canvas_width > 1 else 200
        y = canvas_height // 2 if canvas_height > 1 else 200
        self.canvas.create_image(x, y, image=self._display_image)
        
    def applyGrayscale(self):
        """Apply grayscale filter"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            processed = self.processor.grayscale(self._current_image)
            self.updateImage(processed, "Grayscale filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply grayscale:\n{str(e)}")
            
    def applyBlur(self, value=None):
        """Apply Gaussian blur filter"""
        if self._current_image is None:
            return
            
        try:
            intensity = int(self.blurScale.get())
            # Ensure odd number for kernel size
            if intensity % 2 == 0:
                intensity += 1
                
            processed = self.processor.blur(self._current_image, intensity)
            self.updateImage(processed, f"Blur applied (intensity: {intensity})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply blur:\n{str(e)}")
            
    def applyEdgeDetection(self):
        """Apply Canny edge detection"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            processed = self.processor.edge_detection(self._current_image)
            self.updateImage(processed, "Edge detection applied")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply edge detection:\n{str(e)}")
            
    def adjustBrightness(self, value=None):
        """Adjust image brightness"""
        if self._current_image is None:
            return
            
        try:
            brightness = int(self.brightnessScale.get())
            # Work from original image to avoid cumulative effects
            base_image = self.history.get_first_state()
            processed = self.processor.adjust_brightness(base_image, brightness)
            
            # Also apply contrast if set
            contrast = int(self.contrastScale.get())
            if contrast != 0:
                processed = self.processor.adjust_contrast(processed, contrast)
                
            self._current_image = processed
            self.displayImage(processed)
            self.updateStatus(f"Brightness: {brightness}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to adjust brightness:\n{str(e)}")
            
    def adjustContrast(self, value=None):
        """Adjust image contrast"""
        if self._current_image is None:
            return
            
        try:
            contrast = int(self.contrastScale.get())
            # Work from original image to avoid cumulative effects
            base_image = self.history.get_first_state()
            processed = self.processor.adjust_contrast(base_image, contrast)
            
            # Also apply brightness if set
            brightness = int(self.brightnessScale.get())
            if brightness != 0:
                processed = self.processor.adjust_brightness(processed, brightness)
                
            self._current_image = processed
            self.displayImage(processed)
            self.updateStatus(f"Contrast: {contrast}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to adjust contrast:\n{str(e)}")
            
    def resetAdjustments(self):
        """Reset brightness and contrast sliders"""
        self.brightnessScale.set(0)
        self.contrastScale.set(0)
        
    def rotateImage(self, angle):
        """Rotate image by specified angle"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            processed = self.processor.rotate(self._current_image, angle)
            self.updateImage(processed, f"Image rotated {angle}°")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rotate image:\n{str(e)}")
            
    def flipImage(self, direction):
        """Flip image horizontally or vertically"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            processed = self.processor.flip(self._current_image, direction)
            self.updateImage(processed, f"Image flipped {direction}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to flip image:\n{str(e)}")
            
    def resizeImage(self):
        """Resize image by percentage"""
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            scale = float(self.resizeEntry.get())
            if scale <= 0:
                raise ValueError("Scale percentage must be positive")
                
            processed = self.processor.resize(self._current_image, scale)
            self.updateImage(processed, f"Image resized to {scale}%")
        except ValueError as e:
            messagebox.showerror("Invalid Input", 
                               f"Please enter a valid percentage:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resize image:\n{str(e)}")
            
    def undo(self):
        """Undo last operation"""
        previous = self.history.undo()
        if previous is not None:
            self._current_image = previous
            self._original_image = previous.copy()
            self.displayImage(previous)
            self.resetAdjustments()
            self.updateStatus("Undo - previous state restored")
        else:
            self.updateStatus("Nothing to undo")
            
    def redo(self):
        """Redo last undone operation"""
        next_state = self.history.redo()
        if next_state is not None:
            self._current_image = next_state
            self._original_image = next_state.copy()
            self.displayImage(next_state)
            self.resetAdjustments()
            self.updateStatus("Redo - next state restored")
        else:
            self.updateStatus("Nothing to redo")
            
    def resetImage(self):
        """Reset image to original state"""
        if self.history.get_first_state() is None:
            messagebox.showwarning("No Image", "No image loaded!")
            return
            
        # Ask for confirmation
        answer = messagebox.askyesno("Reset Image", 
                                    "Reset image to original state?")
        if answer:
            original = self.history.get_first_state()
            self._current_image = original.copy()
            self._original_image = original.copy()
            self.displayImage(self._current_image)
            self.resetAdjustments()
            self.updateStatus("Image reset to original state")
            
    def updateImage(self, processed_image, status_message):
        """Update current image and add to history"""
        self._current_image = processed_image
        self._original_image = processed_image.copy()
        self.history.add_state(processed_image.copy())
        self.displayImage(processed_image)
        self.resetAdjustments()
        self.updateStatus(status_message)


# Main program - following Week 8 PDF style
if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
