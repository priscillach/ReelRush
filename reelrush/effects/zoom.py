import cv2

class DynamicZoom:
    @staticmethod
    def apply(clip, start_time, duration, zoom_factor=1.5):
        """Add dynamic zoom effect.
        
        Args:
            clip: Input video clip
            start_time: Start time of zoom
            duration: Duration of zoom effect
            zoom_factor: Maximum zoom level
        """
        def zoom_transform(get_frame, t):
            # 获取当前帧
            frame = get_frame(t)
            
            if start_time <= t <= start_time + duration:
                progress = (t - start_time) / duration
                current_zoom = 1 + (zoom_factor - 1) * progress
                
                h, w = frame.shape[:2]
                center_x, center_y = w // 2, h // 2
                
                M = cv2.getRotationMatrix2D((center_x, center_y), 0, current_zoom)
                return cv2.warpAffine(frame, M, (w, h))
            return frame
        
        return clip.transform(zoom_transform) 