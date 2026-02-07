"""
Image Processing Application
A user-friendly image editor built with Tkinter and OpenCV
Author: Software Engineering Student
Date: February 2026
"""

from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import ImageProcessor
from history_manager import HistoryManager


class ImageProcessingApp:
    """
    Main application class for the Image Processing tool.
    This creates a GUI where users can edit images with various filters and adjustments.
    """
    
    def __init__(self, master):
        """
        Initialize the application and set up the GUI.
        
        Args:
            master: The main Tkinter window
        """
        # Set up the main window
        self.master = master
        self.master.title("Image Processing Application using OpenCV")
        self.master.geometry("1000x700")
        
        # Store the images we're working with
        # These are kept private (using _ prefix) to protect them from accidental changes
        self._current_image = None      # The image as it is right now
        self._original_image = None     # A backup of the current state
        self._display_image = None      # The image shown on screen (Tkinter format)
        self._filename = None           # Where the image is saved
        
        # Create helper objects to process images and track history
        self.processor = ImageProcessor()  # Handles all the image editing
        self.history = HistoryManager()    # Keeps track of undo/redo
        
        # Build the GUI piece by piece
        self.createMenus()
        self.createToolbar()
        self.createWidgets()
        self.createStatusBar()
        
    def createMenus(self):
        """Create the menu bar at the top with File and Edit menus."""
        # Main menu bar
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        # File menu - for opening, saving, and exiting
        fileMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.openImage)
        fileMenu.add_command(label="Save", command=self.saveImage)
        fileMenu.add_command(label="Save As...", command=self.saveImageAs)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exitApp)
        
        # Edit menu - for undoing changes and resetting
        editMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Undo", command=self.undo)
        editMenu.add_command(label="Redo", command=self.redo)
        editMenu.add_separator()
        editMenu.add_command(label="Reset to Original", command=self.resetImage)
        
    def createToolbar(self):
        """Create the toolbar with quick-access buttons."""
        toolbar = Frame(self.master, bg="lightgray", bd=1, relief=RAISED)
        
        # Add buttons to the toolbar (they appear left to right)
        Button(toolbar, text="Open", command=self.openImage).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Save", command=self.saveImage).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Undo", command=self.undo).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Redo", command=self.redo).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Reset", command=self.resetImage).pack(side=LEFT, padx=2, pady=2)
        
        # Put the toolbar at the top of the window
        toolbar.pack(side=TOP, fill=X)
        
    def createWidgets(self):
        """Create the main content area with controls and image display."""
        # Main container that holds everything
        mainFrame = Frame(self.master)
        mainFrame.pack(fill=BOTH, expand=True)
        
        # Left side: control panel with all the editing tools
        self.createControlPanel(mainFrame)
        
        # Right side: where the image is displayed
        self.createImagePanel(mainFrame)
        
    def createControlPanel(self, parent):
        """
        Create the left panel with all image editing controls.
        
        Args:
            parent: The frame that will contain this panel
        """
        # Create a fixed-width panel on the left
        controlFrame = Frame(parent, width=280, bg="#e0e0e0", relief=RIDGE, bd=2)
        controlFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        controlFrame.pack_propagate(False)  # Don't let it shrink
        
        # Title for the control panel
        Label(controlFrame, text="Image Processing Controls", 
              font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=10)
        
        # === FILTERS SECTION ===
        # This section has grayscale, edge detection, and blur controls
        filterFrame = LabelFrame(controlFrame, text="Filters", 
                                font=("Arial", 10, "bold"), bg="#e0e0e0")
        filterFrame.pack(fill=X, padx=10, pady=5)
        
        # Grayscale button - makes the image black and white
        Button(filterFrame, text="Grayscale", width=22, 
               command=self.applyGrayscale).pack(pady=3)
        
        # Edge detection button - finds edges in the image
        Button(filterFrame, text="Edge Detection", width=22, 
               command=self.applyEdgeDetection).pack(pady=3)
        
        # Blur slider - lets you blur the image smoothly
        Label(filterFrame, text="Blur Intensity:", bg="#e0e0e0").pack(pady=(5, 0))
        self.blurScale = Scale(filterFrame, from_=1, to=50, orient=HORIZONTAL, 
                              length=220, command=self.applyBlur)
        self.blurScale.set(1)  # Start with no blur (1 = no blur)
        self.blurScale.pack(pady=3)
        
        # === ADJUSTMENTS SECTION ===
        # This section has brightness and contrast sliders
        adjustFrame = LabelFrame(controlFrame, text="Adjustments", 
                                font=("Arial", 10, "bold"), bg="#e0e0e0")
        adjustFrame.pack(fill=X, padx=10, pady=5)
        
        # Brightness slider - makes image lighter or darker
        Label(adjustFrame, text="Brightness:", bg="#e0e0e0").pack(pady=(5, 0))
        self.brightnessScale = Scale(adjustFrame, from_=-100, to=100, 
                                    orient=HORIZONTAL, length=220, 
                                    command=self.adjustBrightness)
        self.brightnessScale.set(0)  # Start at 0 (no change)
        self.brightnessScale.pack(pady=3)
        
        # Contrast slider - adjusts the difference between light and dark
        Label(adjustFrame, text="Contrast:", bg="#e0e0e0").pack(pady=(5, 0))
        self.contrastScale = Scale(adjustFrame, from_=-100, to=100, 
                                  orient=HORIZONTAL, length=220, 
                                  command=self.adjustContrast)
        self.contrastScale.set(0)  # Start at 0 (no change)
        self.contrastScale.pack(pady=3)
        
        # Reset button - sets brightness and contrast back to 0
        Button(adjustFrame, text="Reset Adjustments", width=22, 
               command=self.resetAdjustments).pack(pady=5)
        
        # === TRANSFORMATIONS SECTION ===
        # This section has rotation, flip, and resize controls
        transformFrame = LabelFrame(controlFrame, text="Transformations", 
                                   font=("Arial", 10, "bold"), bg="#e0e0e0")
        transformFrame.pack(fill=X, padx=10, pady=5)
        
        # Rotation buttons
        Label(transformFrame, text="Rotation:", bg="#e0e0e0", 
              font=("Arial", 9, "bold")).pack(pady=(5, 2))
        Button(transformFrame, text="Rotate 90°", width=22, 
               command=lambda: self.rotateImage(90)).pack(pady=2)
        Button(transformFrame, text="Rotate 180°", width=22, 
               command=lambda: self.rotateImage(180)).pack(pady=2)
        Button(transformFrame, text="Rotate 270°", width=22, 
               command=lambda: self.rotateImage(270)).pack(pady=2)
        
        # Flip buttons
        Label(transformFrame, text="Flip:", bg="#e0e0e0", 
              font=("Arial", 9, "bold")).pack(pady=(10, 2))
        Button(transformFrame, text="Flip Horizontal", width=22, 
               command=lambda: self.flipImage("horizontal")).pack(pady=2)
        Button(transformFrame, text="Flip Vertical", width=22, 
               command=lambda: self.flipImage("vertical")).pack(pady=2)
        
        # Resize control
        Label(transformFrame, text="Resize (%):", bg="#e0e0e0", 
              font=("Arial", 9, "bold")).pack(pady=(10, 2))
        resizeFrame = Frame(transformFrame, bg="#e0e0e0")
        resizeFrame.pack(pady=3)
        self.resizeEntry = Entry(resizeFrame, width=10)
        self.resizeEntry.insert(0, "100")  # 100% = original size
        self.resizeEntry.pack(side=LEFT, padx=2)
        Button(resizeFrame, text="Apply", command=self.resizeImage).pack(side=LEFT, padx=2)
        
    def createImagePanel(self, parent):
        """
        Create the image display area on the right side.
        
        Args:
            parent: The frame that will contain this panel
        """
        # Create a white area for showing the image
        imageFrame = Frame(parent, bg="white", relief=SUNKEN, bd=2)
        imageFrame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        
        # Canvas is like a drawing board where we put the image
        self.canvas = Canvas(imageFrame, bg="#d0d0d0", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)
        
        # Show helpful text when no image is loaded
        self.placeholderText = self.canvas.create_text(
            400, 250, 
            text="No image loaded\n\nClick 'Open' or use File > Open to load an image",
            font=("Arial", 14), fill="gray40", justify=CENTER
        )
        
    def createStatusBar(self):
        """Create the status bar at the bottom that shows messages."""
        self.statusBar = Label(self.master, text="Ready", bd=1, 
                              relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)
        
    def updateStatus(self, message):
        """
        Update the status bar with a new message.
        
        Args:
            message: The text to display in the status bar
        """
        self.statusBar.config(text=message)
        self.master.update_idletasks()  # Make sure it shows up right away
        
    def openImage(self):
        """Let the user choose and open an image file."""
        # Show a file picker dialog
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        # If user selected a file (didn't cancel)
        if filename:
            try:
                # Load the image using OpenCV
                image = cv2.imread(filename)
                if image is None:
                    raise ValueError("Failed to load image")
                    
                # Store the image in our variables
                self._current_image = image.copy()
                self._original_image = image.copy()
                self._filename = filename
                
                # Start fresh with the history
                self.history.clear()
                self.history.add_state(image.copy())
                
                # Show the image on screen
                self.displayImage(image)
                
                # Reset all the sliders to their default positions
                self.resetAdjustments()
                self.blurScale.set(1)
                
                # Tell the user what we loaded
                self.updateStatus(f"Loaded: {filename}")
                
            except Exception as e:
                # If something went wrong, show an error message
                messagebox.showerror("Error", f"Failed to open image:\n{str(e)}")
                
    def saveImage(self):
        """Save the current image to its original file."""
        # Make sure there's an image to save
        if self._current_image is None:
            messagebox.showwarning("No Image", "No image to save!")
            return
            
        # If we know the filename, save there
        if self._filename:
            try:
                cv2.imwrite(self._filename, self._current_image)
                self.updateStatus(f"Saved: {self._filename}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
        else:
            # If we don't have a filename yet, ask for one
            self.saveImageAs()
            
    def saveImageAs(self):
        """Save the current image with a new filename."""
        # Make sure there's an image to save
        if self._current_image is None:
            messagebox.showwarning("No Image", "No image to save!")
            return
            
        # Ask the user where to save and what to name it
        filename = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        
        # If user chose a location (didn't cancel)
        if filename:
            try:
                cv2.imwrite(filename, self._current_image)
                self._filename = filename
                self.updateStatus(f"Saved as: {filename}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
                
    def exitApp(self):
        """Close the application."""
        # Ask for confirmation before closing
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.quit()
            
    def displayImage(self, image):
        """
        Show an image on the canvas.
        
        Args:
            image: The image to display (in OpenCV BGR format)
        """
        if image is None:
            return
            
        # Convert from OpenCV's BGR format to RGB (what PIL expects)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image so Tkinter can use it
        pil_image = Image.fromarray(image_rgb)
        
        # Find out how big the canvas is
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas hasn't been drawn yet, use default size
        if canvas_width <= 1:
            canvas_width = 700
            canvas_height = 600
            
        # Figure out how much to shrink the image to fit the canvas
        img_width, img_height = pil_image.size
        scale_w = canvas_width / img_width
        scale_h = canvas_height / img_height
        scale = min(scale_w, scale_h, 1.0)  # Don't make it bigger, only smaller
        
        # Resize the image if needed
        if scale < 1.0:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        # Convert to PhotoImage (Tkinter's image format)
        self._display_image = ImageTk.PhotoImage(pil_image)
        
        # Clear the canvas and put the image in the center
        self.canvas.delete("all")
        x = canvas_width // 2 if canvas_width > 1 else 200
        y = canvas_height // 2 if canvas_height > 1 else 200
        self.canvas.create_image(x, y, image=self._display_image)
        
    def applyGrayscale(self):
        """Convert the image to black and white."""
        # Make sure we have an image first
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            # Apply the grayscale filter
            processed = self.processor.grayscale(self._current_image)
            self.updateImage(processed, "Grayscale filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply grayscale:\n{str(e)}")
            
    def applyBlur(self, value=None):
        """
        Apply blur to the image based on the slider position.
        
        FIXED VERSION: This now works from the original image so you can
        increase or decrease blur freely without it getting stuck.
        
        Args:
            value: The slider value (Tkinter passes this automatically)
        """
        # Don't do anything if no image is loaded
        if self._current_image is None:
            return
            
        try:
            # Get the blur intensity from the slider
            intensity = int(self.blurScale.get())
            
            # IMPORTANT: Start from the ORIGINAL image, not the current one
            # This is what fixes the bug - we can now reduce blur properly
            base_image = self.history.get_first_state()
            if base_image is None:
                return
                
            # If intensity is 1, show the original (no blur)
            if intensity <= 1:
                processed = base_image.copy()
            else:
                # Make sure the blur kernel size is an odd number (required by OpenCV)
                if intensity % 2 == 0:
                    intensity += 1
                processed = self.processor.blur(base_image, intensity)
            
            # Now apply brightness and contrast if the user has them set
            # This lets all three sliders work together
            brightness = int(self.brightnessScale.get())
            contrast = int(self.contrastScale.get())
            
            if brightness != 0:
                processed = self.processor.adjust_brightness(processed, brightness)
            if contrast != 0:
                processed = self.processor.adjust_contrast(processed, contrast)
                
            # Update the display (but don't add to history - it's just a slider)
            self._current_image = processed
            self.displayImage(processed)
            self.updateStatus(f"Blur: {intensity}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply blur:\n{str(e)}")
            
    def applyEdgeDetection(self):
        """Find and highlight the edges in the image."""
        # Make sure we have an image first
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            # Apply edge detection
            processed = self.processor.edge_detection(self._current_image)
            self.updateImage(processed, "Edge detection applied")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply edge detection:\n{str(e)}")
            
    def adjustBrightness(self, value=None):
        """
        Make the image lighter or darker based on the slider.
        
        Args:
            value: The slider value (Tkinter passes this automatically)
        """
        # Don't do anything if no image is loaded
        if self._current_image is None:
            return
            
        try:
            # Get the brightness adjustment from the slider
            brightness = int(self.brightnessScale.get())
            
            # Start from the original image to avoid cumulative effects
            base_image = self.history.get_first_state()
            
            # Apply blur first if it's set
            blur_intensity = int(self.blurScale.get())
            if blur_intensity > 1:
                if blur_intensity % 2 == 0:
                    blur_intensity += 1
                base_image = self.processor.blur(base_image, blur_intensity)
            
            # Now apply brightness
            processed = self.processor.adjust_brightness(base_image, brightness)
            
            # Also apply contrast if it's set
            contrast = int(self.contrastScale.get())
            if contrast != 0:
                processed = self.processor.adjust_contrast(processed, contrast)
                
            # Update the display
            self._current_image = processed
            self.displayImage(processed)
            self.updateStatus(f"Brightness: {brightness}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to adjust brightness:\n{str(e)}")
            
    def adjustContrast(self, value=None):
        """
        Adjust the difference between light and dark areas.
        
        Args:
            value: The slider value (Tkinter passes this automatically)
        """
        # Don't do anything if no image is loaded
        if self._current_image is None:
            return
            
        try:
            # Get the contrast adjustment from the slider
            contrast = int(self.contrastScale.get())
            
            # Start from the original image to avoid cumulative effects
            base_image = self.history.get_first_state()
            
            # Apply blur first if it's set
            blur_intensity = int(self.blurScale.get())
            if blur_intensity > 1:
                if blur_intensity % 2 == 0:
                    blur_intensity += 1
                base_image = self.processor.blur(base_image, blur_intensity)
            
            # Now apply contrast
            processed = self.processor.adjust_contrast(base_image, contrast)
            
            # Also apply brightness if it's set
            brightness = int(self.brightnessScale.get())
            if brightness != 0:
                processed = self.processor.adjust_brightness(processed, brightness)
                
            # Update the display
            self._current_image = processed
            self.displayImage(processed)
            self.updateStatus(f"Contrast: {contrast}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to adjust contrast:\n{str(e)}")
            
    def resetAdjustments(self):
        """Reset the brightness and contrast sliders back to zero."""
        self.brightnessScale.set(0)
        self.contrastScale.set(0)
        
    def rotateImage(self, angle):
        """
        Rotate the image by 90, 180, or 270 degrees.
        
        Args:
            angle: How many degrees to rotate (90, 180, or 270)
        """
        # Make sure we have an image first
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            # Rotate the image
            processed = self.processor.rotate(self._current_image, angle)
            self.updateImage(processed, f"Image rotated {angle}°")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rotate image:\n{str(e)}")
            
    def flipImage(self, direction):
        """
        Flip the image like a mirror.
        
        Args:
            direction: Either 'horizontal' (left-right) or 'vertical' (top-bottom)
        """
        # Make sure we have an image first
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            # Flip the image
            processed = self.processor.flip(self._current_image, direction)
            self.updateImage(processed, f"Image flipped {direction}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to flip image:\n{str(e)}")
            
    def resizeImage(self):
        """Resize the image based on the percentage entered."""
        # Make sure we have an image first
        if self._current_image is None:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        try:
            # Get the percentage from the entry box
            scale = float(self.resizeEntry.get())
            if scale <= 0:
                raise ValueError("Scale percentage must be positive")
                
            # Resize the image
            processed = self.processor.resize(self._current_image, scale)
            self.updateImage(processed, f"Image resized to {scale}%")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", 
                               f"Please enter a valid percentage:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resize image:\n{str(e)}")
            
    def undo(self):
        """Go back to the previous version of the image."""
        # Try to get the previous state from history
        previous = self.history.undo()
        
        if previous is not None:
            # We found a previous state, restore it
            self._current_image = previous
            self._original_image = previous.copy()
            self.displayImage(previous)
            
            # Reset all the sliders
            self.resetAdjustments()
            self.blurScale.set(1)
            
            self.updateStatus("Undo - previous state restored")
        else:
            # Nothing to undo
            self.updateStatus("Nothing to undo")
            
    def redo(self):
        """Go forward to the next version of the image (if you undid something)."""
        # Try to get the next state from history
        next_state = self.history.redo()
        
        if next_state is not None:
            # We found a next state, restore it
            self._current_image = next_state
            self._original_image = next_state.copy()
            self.displayImage(next_state)
            
            # Reset all the sliders
            self.resetAdjustments()
            self.blurScale.set(1)
            
            self.updateStatus("Redo - next state restored")
        else:
            # Nothing to redo
            self.updateStatus("Nothing to redo")
            
    def resetImage(self):
        """Go all the way back to the original image (before any edits)."""
        # Make sure we have an image loaded
        if self.history.get_first_state() is None:
            messagebox.showwarning("No Image", "No image loaded!")
            return
            
        # Ask the user if they're sure
        answer = messagebox.askyesno("Reset Image", 
                                    "Reset image to original state?")
        if answer:
            # Get the very first version of the image
            original = self.history.get_first_state()
            self._current_image = original.copy()
            self._original_image = original.copy()
            
            # Show it and reset all sliders
            self.displayImage(self._current_image)
            self.resetAdjustments()
            self.blurScale.set(1)
            
            self.updateStatus("Image reset to original state")
            
    def updateImage(self, processed_image, status_message):
        """
        Update the image and add it to history.
        This is used for permanent changes (buttons), not slider movements.
        
        Args:
            processed_image: The new version of the image
            status_message: What to show in the status bar
        """
        # Save the new image
        self._current_image = processed_image
        self._original_image = processed_image.copy()
        
        # Add it to history so we can undo if needed
        self.history.add_state(processed_image.copy())
        
        # Show it on screen
        self.displayImage(processed_image)
        
        # Reset the sliders since this is a new base state
        self.resetAdjustments()
        self.blurScale.set(1)
        
        # Update the status bar
        self.updateStatus(status_message)


# This is where the program starts
if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()