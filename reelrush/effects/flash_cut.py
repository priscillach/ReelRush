from moviepy.editor import VideoFileClip
import numpy as np
import cv2

class FlashCut:
    @staticmethod
    def apply(clip, timestamps, cut_duration=0.1, flash_intensity=1.0):
        """Add flash cut effect at specified timestamps."""
        def flash_transform(get_frame, t):
            frame = get_frame(t)
            
            # 检查是否在任何闪光时间点附近
            for timestamp in timestamps:
                if timestamp <= t <= timestamp + cut_duration:
                    # 计算闪光强度
                    progress = (t - timestamp) / cut_duration
                    intensity = flash_intensity * (1 - progress)
                    
                    # 添加白色闪光
                    flash = np.full_like(frame, 255, dtype=np.uint8)
                    return cv2.addWeighted(frame, 1-intensity, flash, intensity, 0)
            
            return frame
            
        return clip.fl(flash_transform)  # v1.0.3 使用 fl