from moviepy import VideoFileClip, CompositeVideoClip
import numpy as np
import cv2

class SlideTransition:
    @staticmethod
    def apply(clip, timestamp, duration=1.0, direction='left'):
        """Apply slide transition effect at specified timestamp.
        
        Args:
            clip: Input video clip
            timestamp (float): Time to trigger transition
            duration (float): Duration of transition effect
            direction (str): Direction of slide ('left', 'right', 'up', 'down')
        """
        def slide_transform(get_frame, t):
            frame = get_frame(t)
            
            if timestamp <= t <= timestamp + duration:
                # 计算过渡进度 (0 到 1)
                progress = (t - timestamp) / duration
                
                h, w = frame.shape[:2]
                
                # 创建变换矩阵
                if direction == 'left':
                    offset = int(w * progress)
                    M = np.float32([[1, 0, -offset], [0, 1, 0]])
                elif direction == 'right':
                    offset = int(w * (1 - progress))
                    M = np.float32([[1, 0, offset], [0, 1, 0]])
                elif direction == 'up':
                    offset = int(h * progress)
                    M = np.float32([[1, 0, 0], [0, 1, -offset]])
                else:  # down
                    offset = int(h * (1 - progress))
                    M = np.float32([[1, 0, 0], [0, 1, offset]])
                
                # 应用变换
                frame = cv2.warpAffine(frame, M, (w, h))
                
            return frame
        
        return clip.transform(slide_transform) 