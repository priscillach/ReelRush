from moviepy import TextClip, CompositeVideoClip
import numpy as np
import os
from moviepy import *

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
                     animation='fade', stroke_color='black', stroke_width=2,
                     font_style='default', blur_background=None):
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
            stroke_color: Color of text outline
            stroke_width: Width of text outline
            font_style: Font style to use ('default', 'bold', 'elegant', 'modern', 'impact', 'comic')
            blur_background: Type of blur effect for text background (None, 'box_blur', 'gaussian_blur', 'glass', 'motion_blur')
        """
        # 如果需要模糊背景
        if blur_background:
            # 先对原始视频在文字显示的时间段应用模糊效果
            from .filter import FilterEffect
            clip = FilterEffect.apply(clip, blur_background, start_time, duration)
        
        # 获取对应平台的字体路径
        font = DynamicText.get_font_path(font_style)
            
        txt_clip = TextClip(
            text=text,
            font=font,
            font_size=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method='label',
            size=clip.size,
            bg_color=None,
        )
        
        txt_clip = txt_clip.with_duration(duration)
        
        if animation == 'fade':
            txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.5), vfx.CrossFadeOut(0.5)])
        
        return CompositeVideoClip([clip, txt_clip.with_start(start_time)]) 