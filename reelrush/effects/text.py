from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.fx import all as vfx
from moviepy.video.compositing.transitions import crossfadein, crossfadeout, slide_in, slide_out

import numpy as np
import os
from moviepy.config import change_settings

# 设置 ImageMagick 二进制文件路径
if os.path.exists('/usr/local/bin/convert'):
    change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/convert"})
elif os.path.exists('/opt/homebrew/bin/convert'):
    change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

class DynamicText:
    # 预设字体配置
    FONT_PRESETS = {
        'default': {
            'windows': 'C:\\Windows\\Fonts\\arial.ttf',
            'darwin': '/System/Library/Fonts/Helvetica.ttc',  # macOS
            'linux': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        },
        'bold': {
            'windows': 'C:\\Windows\\Fonts\\arialbd.ttf',
            'darwin': '/System/Library/Fonts/HelveticaBold.ttc',
            'linux': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        },
        'elegant': {
            'windows': 'C:\\Windows\\Fonts\\times.ttf',
            'darwin': '/System/Library/Fonts/Times.ttc',
            'linux': '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
        },
        'modern': {
            'windows': 'C:\\Windows\\Fonts\\segoeui.ttf',
            'darwin': '/System/Library/Fonts/SFNSDisplay.ttf',
            'linux': '/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf'
        },
        'impact': {
            'windows': 'C:\\Windows\\Fonts\\impact.ttf',
            'darwin': '/Library/Fonts/Impact.ttf',
            'linux': '/usr/share/fonts/truetype/msttcorefonts/Impact.ttf'
        },
        'comic': {
            'windows': 'C:\\Windows\\Fonts\\comic.ttf',
            'darwin': '/Library/Fonts/Comic Sans MS.ttf',
            'linux': '/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf'
        }
    }

    @staticmethod
    def get_font_path(font_style='default'):
        """Get appropriate font path for current platform."""
        if font_style not in DynamicText.FONT_PRESETS:
            raise ValueError(f"Unknown font style: {font_style}. Available styles: {list(DynamicText.FONT_PRESETS.keys())}")
        
        platform = 'darwin' if os.name == 'posix' and 'darwin' in os.uname().sysname.lower() else \
                  'linux' if os.name == 'posix' else 'windows'
        
        font_path = DynamicText.FONT_PRESETS[font_style][platform]
        
        # 如果指定的字体不存在，回退到默认字体
        if not os.path.exists(font_path):
            return DynamicText.FONT_PRESETS['default'][platform]
            
        return font_path

    @staticmethod
    def animated_text(clip, text, start_time, duration, 
                     position='center', fontsize=70, color='white',
                     animation='fade', fade_in_duration=0.5, fade_out_duration=0.5,
                     stroke_color='black', stroke_width=2,
                     font_style='default', blur_background=None):
        """Create animated text overlay."""
        # 如果需要模糊背景
        if blur_background:
            from .filter import FilterEffect
            clip = FilterEffect.apply(clip, blur_background, start_time, duration)
        
        # 获取对应平台的字体路径
        font = DynamicText.get_font_path(font_style)
            
        txt_clip = TextClip(
            txt=text,
            font=font,
            fontsize=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method='label',
            size=clip.size,
            bg_color='transparent',
            transparent=True
        )
        
        txt_clip = txt_clip.set_duration(duration)
        
        if animation == 'fade':
            txt_clip = txt_clip.fx(crossfadein, duration=fade_in_duration)
            txt_clip = txt_clip.fx(crossfadeout, duration=fade_out_duration)
        elif animation == 'slide':
            w, h = clip.size
            
            def make_slide_frame(t):
                if t < fade_in_duration:  # 入场阶段：从左边滑到中间
                    progress = t / fade_in_duration
                    return (int(w * (progress - 1)), 'center')  # 从 -w 到 0
                elif t < fade_in_duration + duration:  # 中间展示阶段
                    return ('center', 'center')  # 保持在中间
                else:  # 退场阶段：从中间滑到右边
                    progress = (t - (fade_in_duration + duration)) / fade_out_duration
                    return (int(w * progress), 'center')  # 从 0 到 w
            
            # 设置总时长为三个阶段的总和
            total_duration = fade_in_duration + duration + fade_out_duration
            txt_clip = txt_clip.set_duration(total_duration)
            txt_clip = txt_clip.set_position(make_slide_frame)
        
        if position == 'center' and animation != 'slide':
            txt_clip = txt_clip.set_position('center')
        elif animation != 'slide':
            txt_clip = txt_clip.set_position(position)
        
        return CompositeVideoClip([clip, txt_clip.set_start(start_time)]) 