import cv2
import numpy as np

class VideoFilter:
    @staticmethod
    def grayscale(frame):
        """Convert frame to grayscale."""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    @staticmethod
    def sepia(frame):
        """Apply sepia filter."""
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        sepia_image = cv2.transform(frame, sepia_matrix)
        sepia_image[np.where(sepia_image > 255)] = 255
        return sepia_image.astype(np.uint8)
    
    @staticmethod
    def vignette(frame, intensity=0.5):
        """Apply vignette effect."""
        height, width = frame.shape[:2]
        
        # Create radial gradient
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        X, Y = np.meshgrid(x, y)
        mask = np.sqrt(X**2 + Y**2)
        mask = 1 - np.clip(mask * intensity, 0, 1)
        
        # Apply mask to image
        mask = np.dstack([mask] * 3)
        return (frame * mask).astype(np.uint8)
    
    @staticmethod
    def rgb_shift(frame, offset=10):
        """Apply RGB channel shift effect."""
        height, width = frame.shape[:2]
        
        # Split channels
        b, g, r = cv2.split(frame)
        
        # Shift red and blue channels
        M = np.float32([[1, 0, offset], [0, 1, 0]])
        r = cv2.warpAffine(r, M, (width, height))
        M = np.float32([[1, 0, -offset], [0, 1, 0]])
        b = cv2.warpAffine(b, M, (width, height))
        
        return cv2.merge([b, g, r]) 