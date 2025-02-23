from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx
import cv2
import numpy as np

class SoulEffect:
    @staticmethod
    def apply(clip, start_time, duration, intensity=0.5):
        """Apply soul-leaving effect to video.
        
        Args:
            clip: Input video clip
            start_time: Start time of effect
            duration: Duration of effect
            intensity: Effect intensity (0 to 1)
        """
        def soul_transform(get_frame, t):
            frame = get_frame(t)
            
            if t < start_time or t > start_time + duration:
                return frame
            
            # 确保 frame 是 uint8 类型的 numpy 数组
            frame = frame.astype('uint8')
            
            # 计算效果进度 (0 到 1)
            progress = (t - start_time) / duration
            
            # 计算当前放大比例和透明度
            scale = 1 + (intensity * 0.3 * progress)  # 最大放大到 1.3 倍
            alpha = max(0, 0.7 - (progress * 0.7))   # 透明度从 0.7 降到 0
            
            # 放大图像
            h, w = frame.shape[:2]
            scaled_size = (int(w * scale), int(h * scale))
            scaled = cv2.resize(frame, scaled_size, interpolation=cv2.INTER_LINEAR)
            
            # 计算裁剪范围以保持中心对齐
            y_start = max(0, (scaled_size[1] - h) // 2)
            y_end = min(scaled_size[1], y_start + h)
            x_start = max(0, (scaled_size[0] - w) // 2)
            x_end = min(scaled_size[0], x_start + w)
            scaled = scaled[y_start:y_end, x_start:x_end]
            
            # 确保 scaled 和原始帧大小一致
            if scaled.shape != frame.shape:
                scaled = cv2.resize(scaled, (w, h), interpolation=cv2.INTER_LINEAR)
            
            # 混合原始帧和放大帧
            result = cv2.addWeighted(frame, 1, scaled, alpha, 0)
            
            return result.astype('uint8')
            
        return clip.fl(soul_transform)