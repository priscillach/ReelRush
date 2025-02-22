from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import all as vfx

class FreezeFrame:
    @staticmethod
    def apply(clip, start_time, duration):
        """Create a freeze frame effect."""
        # v1.0.3 中没有 with_effects，需要直接使用 fx 方法
        return clip.fx(vfx.freeze,
            t=start_time,  # 冻结时间点
            freeze_duration=duration,  # 冻结持续时间
            padding_end=0  # 结尾填充时间
        )