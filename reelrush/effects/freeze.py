from moviepy import VideoFileClip, concatenate_videoclips
from moviepy import *

class FreezeFrame:
    @staticmethod
    def apply(clip, timestamp, duration):
        """Create a freeze frame effect.
        
        Args:
            clip: Input video clip
            timestamp: Time to freeze frame
            duration: Duration of freeze
        """
        # 使用 vfx.Freeze 实现冻结帧效果
        return clip.with_effects([vfx.Freeze(
            t=timestamp,  # 冻结时间点
            freeze_duration=duration,  # 冻结持续时间
            padding_end=0  # 结尾填充时间
        )]) 