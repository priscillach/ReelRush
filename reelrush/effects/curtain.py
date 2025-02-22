from moviepy.editor import VideoFileClip
import cv2
import numpy as np

class CurtainEffect:
    @staticmethod
    def apply(clip, start_time, duration, effect_type='darken'):
        """Apply curtain effect to video.
        
        Args:
            clip: Input video clip
            start_time: Start time of effect
            duration: Duration of effect
            effect_type: Type of curtain effect ('darken' or 'blur')
        """
        def curtain_transform(get_frame, t):
            frame = get_frame(t)
            
            if t < start_time or t > start_time + duration:
                return frame
                
            # 计算效果进度 (0 到 1)
            progress = (t - start_time) / duration
            
            if effect_type == 'darken':
                # 逐渐变暗：从原始亮度到全黑
                darkened = frame * (1 - progress)
                return darkened.astype('uint8')
            else:  # blur
                # 逐渐模糊：从清晰到最大模糊
                max_blur = 30  # 最大模糊半径
                blur_radius = int(progress * max_blur) * 2 + 1  # 确保是奇数
                blurred = cv2.GaussianBlur(frame, (blur_radius, blur_radius), 0)
                return blurred
                
        return clip.fl(curtain_transform) 