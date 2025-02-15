import cv2
import numpy as np

class FilterEffect:
    """Video filter effects"""
    
    FILTERS = {
        'grayscale': lambda frame: cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB),
        'sepia': lambda frame: np.clip(cv2.transform(
            frame, 
            np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
        ), 0, 255).astype(np.uint8),
        'warm': lambda frame: cv2.addWeighted(
            frame, 
            1.0,
            np.full_like(frame, fill_value=(30, 20, 10), dtype=np.uint8),
            0.3,
            0
        ),
        'cool': lambda frame: cv2.addWeighted(
            frame,
            1.0,
            np.full_like(frame, fill_value=(10, 20, 30), dtype=np.uint8),
            0.3,
            0
        ),
        'vintage': lambda frame: cv2.addWeighted(
            cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB),
            0.7,
            cv2.addWeighted(
                frame,
                0.6,
                np.full_like(frame, fill_value=(30, 20, 10), dtype=np.uint8),
                0.3,
                0
            ),
            0.3,
            0
        ),
        'gaussian_blur': lambda frame: cv2.GaussianBlur(frame, (21, 21), 0),
        'box_blur': lambda frame: cv2.blur(frame, (20, 20)),
        'glass': lambda frame: FilterEffect._frosted_glass_effect(frame),
        'motion_blur': lambda frame: cv2.filter2D(frame, -1, FilterEffect._motion_blur_kernel())
    }
    
    @staticmethod
    def _frosted_glass_effect(frame, strength=10):
        """Create frosted glass effect."""
        height, width = frame.shape[:2]
        
        # 创建随机位移映射
        dx = np.random.randint(-strength, strength, (height, width)).astype(np.float32)
        dy = np.random.randint(-strength, strength, (height, width)).astype(np.float32)
        
        # 创建映射网格
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        
        # 添加位移
        map_x = (x + dx).astype(np.float32)
        map_y = (y + dy).astype(np.float32)
        
        # 应用位移映射并添加模糊
        distorted = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)
        blurred = cv2.GaussianBlur(distorted, (7, 7), 0)
        
        return blurred
    
    @staticmethod
    def _motion_blur_kernel(size=15):
        """Create motion blur kernel."""
        kernel = np.zeros((size, size))
        kernel[int((size-1)/2), :] = np.ones(size)
        kernel = kernel / size
        return kernel
    
    @staticmethod
    def apply(clip, filter_name, start_time, duration):
        """Apply filter effect to video clip.
        
        Args:
            clip: Video clip to apply filter to
            filter_name (str): Name of filter to apply
            start_time (float): Start time of filter effect
            duration (float): Duration of filter effect
        """
        if filter_name not in FilterEffect.FILTERS:
            raise ValueError(f"Unknown filter: {filter_name}. Available filters: {list(FilterEffect.FILTERS.keys())}")
            
        filter_func = FilterEffect.FILTERS[filter_name]
        
        def filter_transform(get_frame, t):
            frame = get_frame(t)
            
            # 只在指定时间段内应用滤镜
            if start_time <= t <= start_time + duration:
                return filter_func(frame)
            return frame
            
        return clip.transform(filter_transform)

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