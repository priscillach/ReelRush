from moviepy.editor import concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx import all as vfx

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
            before = base_clip.subclip(0, start_time)
            
            # 使用 speedx 实现平滑的慢动作
            slow_segment = base_clip.subclip(start_time, end_time)
            slow = slow_segment.fx(vfx.speedx, speed)
            
            after = base_clip.subclip(end_time)
            
            # 合并视频片段
            final_clip = concatenate_videoclips([before, slow, after])
            
            # 重新添加叠加层
            return CompositeVideoClip([final_clip] + overlays)
            
        else:
            # 原始的慢动作处理逻辑
            before = clip.subclip(0, start_time)
            slow_segment = clip.subclip(start_time, end_time)
            slow = slow_segment.fx(vfx.speedx, speed)
            after = clip.subclip(end_time)
            return concatenate_videoclips([before, slow, after]) 