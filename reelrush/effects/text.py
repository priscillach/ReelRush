from moviepy import TextClip, CompositeVideoClip
import numpy as np
import os
from moviepy import *

class DynamicText:
    @staticmethod
    def animated_text(clip, text, start_time, duration, 
                     position='center', fontsize=70, color='white',
                     animation='fade', stroke_color='black', stroke_width=2):
        """Create animated text overlay.
        
        Args:
            clip: Input video clip
            text: Text to display
            start_time: Start time in seconds
            duration: Duration in seconds
            position: Text position ('center' or (x,y))
            fontsize: Font size
            color: Text color
            animation: Animation type ('fade', 'slide', 'scale')
        """
        # 使用系统字体
        if os.name == 'posix':  # macOS 或 Linux
            font = '/System/Library/Fonts/Helvetica.ttc'  # macOS
            if not os.path.exists(font):
                font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Linux
        else:  # Windows
            font = 'C:\\Windows\\Fonts\\arial.ttf'
            
        txt_clip = TextClip(
            text=text,
            font=font,
            font_size=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method='label',
            size=clip.size,            # 设置与视频相同的尺寸
            bg_color=None,             # 透明背景
        )
        # 设置持续时间
        txt_clip = txt_clip.with_duration(duration)
        
        if animation == 'fade':
            txt_clip = txt_clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
        
        # 创建合成视频并设置文本开始时间
        return CompositeVideoClip([clip, txt_clip.with_start(start_time)]) 