from moviepy import VideoFileClip
import numpy as np
import cv2

class FlashCut:
    @staticmethod
    def create(clip, timestamps, cut_duration=0.1, flash_intensity=1.0):
        """Create flash transitions at specified timestamps.
        
        Args:
            clip: The video clip to add transitions to
            timestamps: List of timestamps where to add flash effects
            cut_duration: Duration of flash transition effect
            flash_intensity: Intensity of flash effect (0 to 1)
        """
        def flash_transform(get_frame, t):
            frame = get_frame(t)
            
            # 检查当前时间是否接近任何一个时间戳
            for timestamp in timestamps:
                if timestamp - cut_duration/2 <= t <= timestamp + cut_duration/2:
                    # 计算闪光进度（0到1）
                    if t <= timestamp:
                        # 淡入白光
                        progress = (t - (timestamp - cut_duration/2)) / (cut_duration/2)
                    else:
                        # 淡出白光
                        progress = 1 - (t - timestamp) / (cut_duration/2)
                    
                    flash = np.ones_like(frame) * 255
                    alpha = min(progress * flash_intensity, 1.0)  # 限制最大透明度
                    return cv2.addWeighted(frame, 1.0 - alpha, flash, alpha, 0)
            
            return frame
        
        # 应用闪光效果
        final_clip = clip.transform(flash_transform)
        return final_clip