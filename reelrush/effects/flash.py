import cv2
import numpy as np

class FlashEffect:
    @staticmethod
    def apply(clip, timestamp, duration=0.1, intensity=1.0):
        """Add flash effect.
        
        Args:
            clip: Input video clip
            timestamp: Time to add flash
            duration: Duration of flash
            intensity: Flash intensity (0 to 1)
        """
        def flash_transform(frame, t):
            if timestamp <= t <= timestamp + duration:
                progress = 1 - abs(2 * (t - timestamp) / duration - 1)
                flash = np.ones_like(frame) * 255
                return cv2.addWeighted(frame, 1, flash, progress * intensity, 0)
            return frame
        
        return clip.fl(flash_transform) 