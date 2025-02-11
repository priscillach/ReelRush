from moviepy import concatenate_videoclips
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy import *

class SlowMotion:
    @staticmethod
    def apply(clip, start_time, end_time, speed=0.5, abruptness= 0, soonness=1):
        """Apply slow motion effect to video segment.
        
        Args:
            clip: Input video clip
            start_time: Start time in seconds
            end_time: End time in seconds
            speed: Playback speed (0.1 to 1.0)
        """
        # 如果是 CompositeVideoClip，获取原始视频
        if isinstance(clip, CompositeVideoClip):
            base_clip = clip.clips[0]  # 获取基础视频
            overlays = clip.clips[1:]  # 获取所有叠加层
            
            # 对基础视频应用慢动作
            before = base_clip.subclipped(0, start_time)
            
            # 使用 AccelDecel 实现平滑的慢动作
            slow_segment = base_clip.subclipped(start_time, end_time)
            slow = slow_segment.with_effects([vfx.AccelDecel(
                new_duration=(end_time - start_time) / speed,
                abruptness=abruptness,  # 正值表示先减速，后加速，再减速
                soonness=soonness     # 控制变速的时机
            )])
            
            after = base_clip.subclipped(end_time)
            
            # 合并视频片段
            final_clip = concatenate_videoclips([before, slow, after])
            
            # 重新添加叠加层
            return CompositeVideoClip([final_clip] + overlays)
            
        else:
            # 原始的慢动作处理逻辑
            before = clip.subclipped(0, start_time)
            slow_segment = clip.subclipped(start_time, end_time)
            slow = slow_segment.with_effects([vfx.AccelDecel(
                new_duration=(end_time - start_time) / speed,
                abruptness=0.5,
                soonness=1.0
            )])
            after = clip.subclipped(end_time)
            return concatenate_videoclips([before, slow, after]) 