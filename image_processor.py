"""
Image Processor Class
Handles all image processing operations using OpenCV, demonstrating encapsulation.
"""

import cv2
import numpy as np


class ImageProcessor:
    """Class responsible for all image processing operations."""

    def __init__(self):
        """Constructor: Initialize the image processor with default parameters."""
        self._default_blur_kernel = 5  # Default blur kernel size
        self._default_edge_threshold1 = 100  # Default Canny edge detection threshold 1
        self._default_edge_threshold2 = 200  # Default Canny edge detection threshold 2

    def grayscale(self, image):
        """
        Convert image to grayscale.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Grayscale image (BGR format)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, image, intensity=5):
        """Apply Gaussian blur to the image."""
        kernel_size = max(1, intensity)
        if kernel_size % 2 == 0:
            kernel_size += 1  # Ensure kernel size is odd
            
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def edge_detection(self, image, threshold1=None, threshold2=None):
        """
        Apply Canny edge detection.
        
        Args:
            image: Input image
            threshold1: First threshold for hysteresis
            threshold2: Second threshold for hysteresis
            
        Returns:
            Edge-detected image (BGR format)
        """
        threshold1 = threshold1 if threshold1 is not None else self._default_edge_threshold1
        threshold2 = threshold2 if threshold2 is not None else self._default_edge_threshold2
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def adjust_brightness(self, image, value):
        """
        Adjust image brightness.
        
        Args:
            image: Input image
            value: Brightness adjustment value (-100 to 100)
            
        Returns:
            Brightness-adjusted image
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        v = cv2.add(v, value) if value >= 0 else cv2.subtract(v, abs(value))
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    def adjust_contrast(self, image, value):
        """
        Adjust image contrast.
        
        Args:
            image: Input image
            value: Contrast adjustment value (-100 to 100)
            
        Returns:
            Contrast-adjusted image
        """
        alpha = 1.0 + (value / 100.0)
        alpha = max(0.5, min(3.0, alpha))
        return cv2.convertScaleAbs(image, alpha=alpha)

    def rotate(self, image, angle):
        """
        Rotate image by a specified angle.
        
        Args:
            image: Input image
            angle: Rotation angle (90, 180, or 270)
            
        Returns:
            Rotated image
        """
        if angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            raise ValueError("Angle must be 90, 180, or 270 degrees")

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
            return cv2.flip(image, 1)
        elif direction == "vertical":
            return cv2.flip(image, 0)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")

    def resize(self, image, scale_percent):
        """
        Resize image by percentage.
        
        Args:
            image: Input image
            scale_percent: Percentage to scale (50 for 50%, 200 for 200%)
            
        Returns:
            Resized image
        """
        if scale_percent <= 0:
            raise ValueError("Scale percentage must be positive")
        
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        width = max(1, width)
        height = max(1, height)
        
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_LANCZOS4)

    def sharpen(self, image):
        """
        Sharpen the image using a kernel.
        
        Args:
            image: Input image
            
        Returns:
            Sharpened image
        """
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)

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