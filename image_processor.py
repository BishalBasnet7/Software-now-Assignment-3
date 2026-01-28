"""
Image Processor Class
Handles all image processing operations using OpenCV
Demonstrates encapsulation and methods
"""

import cv2
import numpy as np


class ImageProcessor:
    """
    Class responsible for all image processing operations.
    Demonstrates encapsulation of image processing logic.
    """
    
    def __init__(self):
        """Constructor: Initialize the image processor."""
        # Encapsulation: Private attributes for default parameters
        self._default_blur_kernel = 5
        self._default_edge_threshold1 = 100
        self._default_edge_threshold2 = 200
        
    def grayscale(self, image):
        """
        Convert image to grayscale.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Grayscale image converted back to BGR for consistency
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Convert back to BGR to maintain 3 channels
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return gray_bgr
    
    def blur(self, image, intensity=5):
        # Ensure kernel size is odd and positive
        kernel_size = max(1, intensity)
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred
    
    def edge_detection(self, image, threshold1=100, threshold2=200):
        """
        Apply Canny edge detection algorithm.
        
        Args:
            image: Input image
            threshold1: First threshold for hysteresis
            threshold2: Second threshold for hysteresis
            
        Returns:
            Edge-detected image
        """
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1, threshold2)
        
        # Convert back to BGR
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edges_bgr
    
    def adjust_brightness(self, image, value):
        """
        Adjust image brightness.
        
        Args:
            image: Input image
            value: Brightness adjustment value (-100 to 100)
            
        Returns:
            Brightness-adjusted image
        """
        # Convert to HSV for better brightness control
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Adjust V channel (brightness)
        if value >= 0:
            # Increase brightness
            v = cv2.add(v, value)
        else:
            # Decrease brightness
            v = cv2.subtract(v, abs(value))
        
        # Merge channels and convert back to BGR
        final_hsv = cv2.merge((h, s, v))
        adjusted = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return adjusted
    
    def adjust_contrast(self, image, value):
        """
        Adjust image contrast.
        
        Args:
            image: Input image
            value: Contrast adjustment value (-100 to 100)
            
        Returns:
            Contrast-adjusted image
        """
        # Calculate alpha (contrast control: 1.0 = no change)
        # Range: 0.5 (low contrast) to 3.0 (high contrast)
        alpha = 1.0 + (value / 100.0)
        alpha = max(0.5, min(3.0, alpha))
        
        # Calculate beta (brightness control)
        beta = 0
        
        # Apply the formula: new_image = alpha * image + beta
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted
    
    def rotate(self, image, angle):
        """
        Rotate image by 90, 180, or 270 degrees.
        
        Args:
            image: Input image
            angle: Rotation angle (90, 180, or 270)
            
        Returns:
            Rotated image
        """
        if angle == 90:
            # Rotate 90 degrees clockwise
            rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            # Rotate 180 degrees
            rotated = cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            # Rotate 270 degrees clockwise (or 90 counter-clockwise)
            rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            raise ValueError("Angle must be 90, 180, or 270 degrees")
            
        return rotated
    
    def flip(self, image, direction):
        """
        Flip image horizontally or vertically.
        
        Args:
            image: Input image
            direction: 'horizontal' or 'vertical'
            
        Returns:
            Flipped image
        """
        if direction == "horizontal":
            # Flip horizontally (around y-axis)
            flipped = cv2.flip(image, 1)
        elif direction == "vertical":
            # Flip vertically (around x-axis)
            flipped = cv2.flip(image, 0)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
            
        return flipped
    
    def resize(self, image, scale_percent):
        """
        Resize image by percentage.
        
        Args:
            image: Input image
            scale_percent: Percentage to scale (e.g., 50 for 50%, 200 for 200%)
            
        Returns:
            Resized image
        """
        if scale_percent <= 0:
            raise ValueError("Scale percentage must be positive")
            
        # Calculate new dimensions
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        
        # Ensure minimum size of 1x1
        width = max(1, width)
        height = max(1, height)
        
        # Resize image
        resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_LANCZOS4)
        return resized
    
    def sharpen(self, image):
        """
        Sharpen the image using a kernel.
        
        Args:
            image: Input image
            
        Returns:
            Sharpened image
        """
        # Sharpening kernel
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened
    
    def get_image_info(self, image):
        """
        Get information about the image.
        
        Args:
            image: Input image
            
        Returns:
            Dictionary with image information
        """
        height, width = image.shape[:2]
        channels = image.shape[2] if len(image.shape) > 2 else 1
        
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'size': image.size,
            'dtype': image.dtype
        }
