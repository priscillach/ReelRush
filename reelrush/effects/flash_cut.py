from moviepy import VideoFileClip, concatenate_videoclips
import numpy as np
import cv2

class FlashCut:
    @staticmethod
    def create(clips, cut_duration=0.1, flash_intensity=1.0):
        """Create rapid cuts between video clips with flash transition.
        
        Args:
            clips (list): List of video clips to join with flash transitions
            cut_duration (float): Duration of flash transition effect
            flash_intensity (float): Intensity of flash effect (0 to 1)
        """
        final_clips = []
        
        for i, clip in enumerate(clips):
            if i < len(clips) - 1:
                def flash_transform(get_frame, t):
                    frame = get_frame(t)
                    
                    # 只在片段的最后 cut_duration 时间添加闪光效果
                    if t >= clip.duration - cut_duration:
                        # 计算闪光进度（0到1）
                        progress = (t - (clip.duration - cut_duration)) / cut_duration
                        # 创建白色帧
                        flash = np.ones_like(frame) * 255
                        # 混合原始帧和白色帧
                        return cv2.addWeighted(
                            frame, 
                            1.0 - (progress * flash_intensity), 
                            flash, 
                            progress * flash_intensity, 
                            0
                        )
                    return frame
                
                # 只对片段的最后部分应用闪光效果
                transformed_clip = clip.transform(flash_transform)
                final_clips.append(transformed_clip)
            else:
                # 最后一个片段不需要闪光效果
                final_clips.append(clip)
        
        # 连接所有片段
        final_clip = concatenate_videoclips(final_clips)
        return final_clip 