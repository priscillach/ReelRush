from moviepy import *
import numpy as np

class CameraShake:
    @staticmethod
    def apply(clip, start_time, duration, intensity=0.5):
        """Apply camera shake effect to video.
        
        Args:
            clip: Input video clip
            start_time: Start time in seconds
            duration: Duration in seconds
            intensity: Shake intensity (0.0 to 1.0)
        """
        def shake_transform(get_frame, t):
            # 只在指定时间段内应用抖动
            if t < start_time or t > start_time + duration:
                return get_frame(t)
            
            # 生成随机偏移
            dx = intensity * np.random.uniform(-30, 30)
            dy = intensity * np.random.uniform(-30, 30)
            
            # 获取原始帧
            frame = get_frame(t)
            
            # 创建平移矩阵
            h, w = frame.shape[:2]
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            
            # 应用平移变换
            import cv2
            return cv2.warpAffine(frame, M, (w, h))
            
        # 使用 transform 替代 fl
        return clip.transform(shake_transform) 