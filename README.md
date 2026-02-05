# HIT137 Assignment 3 - Image Processing Application

## Group Members
- **[Nishan Hamal]**
- **[Bishal Basnet]** - 
- **[aryan Thaoa]** 
 **[Bhuwan Giri]** 
---


Desktop image processing application built with Python Tkinter and OpenCV, following Week 8 tutorial programming style.

---

## Installation

### Step 1: Install Python Packages
```bash
pip3 install opencv-python numpy Pillow
```

### Step 2: Run the Application
```bash
python3 main.py
```

---

## Features

### Image Processing (8 Required Features)
1. **Grayscale Conversion** - Convert to black and white
2. **Blur Effect** - Adjustable Gaussian blur (slider 1-50)
3. **Edge Detection** - Canny edge detection
4. **Brightness** - Adjust brightness (-100 to +100)
5. **Contrast** - Adjust contrast (-100 to +100)
6. **Rotation** - Rotate 90°, 180°, 270°
7. **Flip** - Horizontal or vertical flip
8. **Resize** - Scale by percentage

### GUI Elements
- **Menu Bar** - File (Open, Save, Save As, Exit) and Edit (Undo, Redo, Reset)
- **Toolbar** - Quick access buttons
- **Control Panel** - Organized filters, adjustments, transformations
- **Canvas** - Image display area
- **Status Bar** - Shows current operation
- **Sliders** - For blur, brightness, contrast
- **File Dialogs** - Open and save images
- **Message Boxes** - Errors and confirmations

---

## OOP Requirements (All Met)

### 3 Classes

**1. ImageProcessingApp** (main.py)
- Main GUI application class
- 30+ methods

**2. ImageProcessor** (image_processor.py)  
- All image processing operations
- 10+ methods

**3. HistoryManager** (history_manager.py)
- Undo/redo functionality
- 10+ methods

### OOP Concepts Demonstrated

**Encapsulation** ✓
```python
self._current_image = None  # Private attribute
self._filename = None        # Private attribute
```

**Constructor** ✓
```python
def __init__(self, master):
    """Initializes the application"""
    self.processor = ImageProcessor()
    self.history = HistoryManager()
```

**Methods** ✓
```python
def applyGrayscale(self):
    """Apply grayscale filter"""
    processed = self.processor.grayscale(self._current_image)
```

**Class Interaction** ✓
```python
# Main class uses other classes
self.processor = ImageProcessor()  # For processing
self.history = HistoryManager()    # For undo/redo
```

---

## How to Use

### 1. Open Image
- Click **"Open"** button
- Or use **File > Open**
- Select JPG, PNG, or BMP file

### 2. Apply Filters
- Click **"Grayscale"** button
- Click **"Edge Detection"** button  
- Move **"Blur Intensity"** slider

### 3. Adjust Image
- Move **"Brightness"** slider
- Move **"Contrast"** slider
- Click **"Reset Adjustments"** to reset

### 4. Transform Image
- Click **"Rotate 90°/180°/270°"**
- Click **"Flip Horizontal/Vertical"**
- Enter percentage, click **"Apply"** to resize

### 5. Undo/Redo
- Click **"Undo"** (or Edit > Undo)
- Click **"Redo"** (or Edit > Redo)

### 6. Save Image
- Click **"Save"** to overwrite
- Use **File > Save As** for new file

---

## File Structure
```
project/
├── main.py                # Main application
├── image_processor.py     # Image processing
├── history_manager.py     # Undo/redo management
├── requirements.txt       # Dependencies
├── README.md             # This file
├── github_link.txt       # GitHub link
└── sample_test_image.jpg # Test image
```

---

## Code Structure (Week 8 Style)

### Main Program
```python
root = Tk()
app = ImageProcessingApp(root)
root.mainloop()
```

### Menu Creation (PDF Style)
```python
menu = Menu(self.master)
self.master.config(menu=menu)
fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=self.openImage)
```

### Toolbar (PDF Style)
```python
toolbar = Frame(self.master, bg="lightgray")
Button(toolbar, text="Open", command=self.openImage).pack(side=LEFT)
toolbar.pack(side=TOP, fill=X)
```

### Status Bar (PDF Style)
```python
self.statusBar = Label(self.master, text="Ready", 
                      bd=1, relief=SUNKEN, anchor=W)
self.statusBar.pack(side=BOTTOM, fill=X)
```

### Message Boxes (PDF Style)
```python
messagebox.showinfo("Success", "Image saved!")
messagebox.showerror("Error", "Failed to load")
messagebox.askyesno("Reset", "Reset image?")
```

---

## Testing

### Basic Tests
1. Run application - window opens
2. Open sample_test_image.jpg
3. Click each filter button
4. Move each slider
5. Test all transformations
6. Try undo/redo
7. Save image

### Format Tests  
- ✓ JPG files
- ✓ PNG files
- ✓ BMP files

### Error Tests
- Try filters without image (shows warning)
- Try invalid resize value (shows error)
- Try save without image (shows warning)

---

## Troubleshooting

**Problem:** ModuleNotFoundError
```bash
pip3 install opencv-python numpy Pillow
```

**Problem:** Application won't start
- Check Python 3.7+ installed
- Check all files in same folder

**Problem:** Image won't load  
- Use JPG, PNG, or BMP format only
- Check file is not corrupted

---

## Requirements Checklist

### OOP (All Met) ✓
- [x] 3 Classes
- [x] Encapsulation (private attributes)
- [x] Constructors (__init__ methods)
- [x] Methods (30+ total)
- [x] Class Interaction

### Image Processing (All Met) ✓
- [x] Grayscale
- [x] Blur with adjustable intensity
- [x] Edge detection  
- [x] Brightness adjustment
- [x] Contrast adjustment
- [x] Rotation (90°, 180°, 270°)
- [x] Flip (horizontal, vertical)
- [x] Resize/scale

### GUI (All Met) ✓
- [x] Main window
- [x] Menu bar (File, Edit)
- [x] Image display area (Canvas)
- [x] Control panel
- [x] Status bar
- [x] File dialogs
- [x] At least one slider (has 3!)
- [x] Message boxes
- [x] Support JPG, PNG, BMP

---

## Submission Steps

1. **Create GitHub Repository**
   - Make it PUBLIC
   - Name: hit137-assignment3-image-processor

2. **Add Group Members**
   - Go to Settings > Collaborators
   - Add all group members

3. **Upload Files**
   - main.py
   - image_processor.py
   - history_manager.py
   - requirements.txt
   - README.md
   - github_link.txt
   - sample_test_image.jpg

4. **Update github_link.txt**
   - Add your actual repository URL

5. **Create Zip File**
   - Zip all files together

6. **Submit to Learnline**
   - Upload zip file
   - Include github_link.txt

---

## Notes

This application follows Week 8 tutorial style:
- Simple, clear code structure
- Basic Tkinter widgets
- Frame-based layout
- PDF example patterns
- Easy to understand

All assignment requirements are met!

---

**Last Updated:** January 2026  
**Version:** 1.0
