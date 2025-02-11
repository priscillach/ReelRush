import cv2
import numpy as np

class GlitchEffect:
    @staticmethod
    def apply(clip, timestamp, duration=0.5):
        """Add glitch effect at specified timestamp.
        
        Args:
            clip: Input video clip
            timestamp: Time to add glitch
            duration: Duration of glitch effect
        """
        def glitch_transform(get_frame, t):
            # 获取原始帧
            frame = get_frame(t)
            
            # 只在指定时间段内应用故障效果
            if timestamp <= t <= timestamp + duration:
                height, width = frame.shape[:2]
                slice_h = int(height / 10)
                shifts = np.random.randint(-50, 50, size=(10, 2))
                
                glitched = frame.copy()
                for i, (dx, dy) in enumerate(shifts):
                    h_start = slice_h * i
                    h_end = h_start + slice_h
                    temp = frame[h_start:h_end, :]
                    
                    M = np.float32([[1, 0, dx], [0, 1, dy]])
                    glitched[h_start:h_end, :] = cv2.warpAffine(
                        temp, 
                        M, 
                        (width, slice_h)
                    )
                return glitched
            return frame
            
        return clip.transform(glitch_transform) 