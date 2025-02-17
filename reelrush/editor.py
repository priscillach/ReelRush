from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import cv2
import numpy as np
from reelrush.effects.filter import FilterEffect
from reelrush.effects.text import DynamicText
from reelrush.effects.particle import ParticleEffect
from reelrush.effects.flash_cut import FlashCut
from reelrush.effects.shake import CameraShake
from reelrush.effects.glitch import GlitchEffect
from reelrush.effects.motion import SlowMotion
from reelrush.effects.flash import FlashEffect
from reelrush.effects.zoom import DynamicZoom
from reelrush.effects.freeze import FreezeFrame
from reelrush.effects.slide import SlideTransition
import os
import json


class VideoEditor:
    def __init__(self, video_path, vide_file_clip=None):
        """Initialize the video editor with a video file.
        
        Args:
            video_path (str): Path to the input video file
            video: VideoFileClip object
        """
        if video_path:
            self.video_path = video_path
            self.base_clip = VideoFileClip(video_path)
        elif vide_file_clip:
            self.base_clip = vide_file_clip
        else:
            raise ValueError("video_path or vide_file_clip must be provided")
        self.clip = self.base_clip  # 保持 self.clip 引用，用于存储当前编辑状态
        self.effects = []  # 存储所有特效及其时间信息
        self.duration = self.base_clip.duration  # 跟踪视频总时长
    
    def _update_duration(self, start_time, end_time, new_duration):
        """更新视频总时长"""
        original_duration = end_time - start_time
        duration_change = new_duration - original_duration
        self.duration += duration_change
        
        # 更新后续特效的时间点
        for effect in self.effects:
            if effect['time'] > end_time:
                effect['time'] += duration_change
    
    def _get_adjusted_time(self, timestamp):
        """根据之前的效果调整时间点"""
        adjusted_time = timestamp
        for effect in self.effects:
            if effect['type'] == 'slow_motion' and effect['time'] < timestamp:
                # 计算慢动作效果对时间点的影响
                effect_end = effect['time'] + effect['duration']
                if timestamp > effect_end:
                    time_change = effect['duration'] - (effect_end - effect['time'])
                    adjusted_time += time_change
        return adjusted_time
    
    def add_freeze_frame(self, start_time, duration=2):
        """Add a freeze frame effect at the specified timestamp.
        
        Args:
            timestamp (float): Time in seconds where to freeze
            duration (float): Duration of freeze in seconds
        """
        self.clip = FreezeFrame.apply(self.clip, start_time, duration)
        
        
    def add_camera_shake(self, start_time, duration, intensity=0.5):
        """Add camera shake effect.
        
        Args:
            start_time (float): Start time in seconds
            duration (float): Duration of effect in seconds
            intensity (float): Shake intensity from 0 to 1
        """
        self.clip = CameraShake.apply(
            self.clip, 
            start_time, 
            duration, 
            intensity
        )
    
    def add_glitch(self, start_time, duration=0.5):
        """Add glitch effect at specified timestamp.
        
        Args:
            start_time (float): Time in seconds to add glitch
            duration (float): Duration of glitch effect
        """
        self.clip = GlitchEffect.apply(self.clip, start_time, duration)
    
    def add_slow_motion(self, start_time, end_time, speed=0.5, abruptness=0, soonness=1):
        """Add slow motion effect to a segment of video.
        
        Args:
            start_time (float): Start time in seconds
            end_time (float): End time in seconds
            speed (float): Playback speed (0.1 to 1.0)
        """
        new_duration = (end_time - start_time) / speed
        self._update_duration(start_time, end_time, new_duration)
        
        self.effects.append({
            'type': 'slow_motion',
            'time': start_time,
            'duration': new_duration,
            'params': {
                'speed': speed,
                'abruptness': abruptness,
                'soonness': soonness
            }
        })
        
        self.clip = SlowMotion.apply(
            self.clip, 
            start_time, 
            end_time, 
            speed,
            abruptness,
            soonness
        )

    def add_zoom(self, start_time, duration, zoom_factor=1.5):
        """Add dynamic zoom effect.
        
        Args:
            start_time (float): Start time of zoom
            duration (float): Duration of zoom effect
            zoom_factor (float): Maximum zoom level
        """
        self.clip = DynamicZoom.apply(self.clip, start_time, duration, zoom_factor)

    def add_flash(self, timestamp, duration=0.1, intensity=1.0):
        """Add flash effect.
        
        Args:
            timestamp (float): Time to add flash
            duration (float): Duration of flash
            intensity (float): Flash intensity (0 to 1)
        """
        self.clip = FlashEffect.apply(self.clip, timestamp, duration, intensity)
    
    def save(self, output_path, codec='libx264', fps=None):
        """Save the edited video.
        
        Args:
            output_path (str): Path to save the output video
            codec (str): Video codec to use
            fps (int, optional): Output frame rate
        """
        self.clip.write_videofile(
            output_path,
            codec=codec,
            fps=fps if fps else self.clip.fps
        )

    def add_filter(self, filter_name, start_time, duration):
        """Add filter effect to video.
        
        Args:
            filter_name (str): Name of filter to apply:
                - 'grayscale': Black and white effect
                - 'sepia': Vintage brownish effect
                - 'warm': Warm color temperature
                - 'cool': Cool color temperature
                - 'vintage': Retro style effect
                - 'gaussian_blur': Soft blur effect, ideal for dream or memory scenes
                - 'box_blur': Uniform blur effect, good for defocus simulation
                - 'glass': Frosted glass effect, creates mystical or dreamy atmosphere
                - 'motion_blur': Motion blur effect, emphasizes movement or speed
            start_time (float): Start time of filter effect
            duration (float): Duration of filter effect
        """
        # 调整时间点以适应之前的时长变化
        adjusted_time = self._get_adjusted_time(start_time)
        
        # 添加效果记录
        self.effects.append({
            'type': 'filter',
            'name': filter_name,
            'time': adjusted_time,
            'duration': duration
        })
        
        # 应用滤镜效果
        self.clip = FilterEffect.apply(
            self.clip,
            filter_name,
            adjusted_time,
            duration
        )

    def add_animated_text(self, text, start_time, duration, 
                         position='center', fontsize=70, color='white',
                         animation='fade', stroke_color='black', stroke_width=2,
                         font_style='default', blur_background=None):
        """Add animated text overlay.
        
        Args:
            text (str): Text to display
            start_time (float): Start time in seconds
            duration (float): Duration to display text
            position (str/tuple): Position of text ('center' or (x,y))
            fontsize (int): Font size
            color (str): Text color
            animation (str): Animation type ('fade', 'slide', 'scale')
            stroke_color (str): Color of text outline
            stroke_width (int): Width of text outline
            font_style (str): Font style to use ('default', 'bold', 'elegant', 'modern', 'impact', 'comic')
            blur_background (str): Type of blur effect for text background (None, 'box_blur', 'gaussian_blur', 'glass', 'motion_blur')
        """
        self.clip = DynamicText.animated_text(
            self.clip, text, start_time, duration,
            position, fontsize, color, animation,
            stroke_color, stroke_width, font_style,
            blur_background
        )

    def add_particle_explosion(self, start_time, duration=1.0, num_particles=100, position='center'):
        """Add particle explosion effect.
        
        Args:
            start_time (float): Time to trigger explosion
            duration (float): Duration of effect
            num_particles (int): Number of particles
            position (str/tuple): Position of explosion ('center' or (x,y))
        """
        particles = ParticleEffect(num_particles)
        
        def particle_transform(get_frame, t):
            frame = get_frame(t)
            
            if start_time <= t <= start_time + duration:
                # Get explosion origin
                height, width = frame.shape[:2]
                if position == 'center':
                    origin = (width // 2, height // 2)
                elif isinstance(position, (tuple, list)) and len(position) == 2:
                    # 将百分比位置转换为像素坐标
                    origin = (int(position[0] * width), int(position[1] * height))
                else:
                    raise ValueError("Position must be 'center' or a tuple of (x,y) in range 0-1")
                
                # Initialize particles if this is the start
                if abs(t - start_time) < 0.1:
                    particles.initialize_particles(origin)
                
                # Update and render particles
                particles.update_particles(1/self.clip.fps)
                return particles.render(frame.copy(), t)
            return frame
        
        self.clip = self.clip.transform(particle_transform)

    def add_flash_cuts(self, timestamps, cut_duration=0.1, flash_intensity=1.0):
        """Add flash cut transitions at specified timestamps.
        
        Args:
            timestamps: List of timestamps where to add flash effects
            cut_duration: Duration of flash transition effect
            flash_intensity: Intensity of flash effect (0 to 1)
        """
        print("\n=== Flash Cuts Debug ===")
        print(f"Original timestamps: {timestamps}")
        
        # Convert timestamps to float
        adjusted_timestamps = [float(t) for t in timestamps]
        
        # Add flash cuts
        self.clip = FlashCut.create(
            clip=self.clip,  # 传入整个视频片段
            timestamps=adjusted_timestamps,  # 传入时间戳列表
            cut_duration=cut_duration,
            flash_intensity=flash_intensity
        )

    def add_slide_transition(self, start_time, duration=1.0, direction='left'):
        """Add slide transition effect.
        
        Args:
            start_time (float): Time to trigger transition
            duration (float): Duration of transition effect
            direction (str): Direction of slide ('left', 'right', 'up', 'down')
        """
        self.clip = SlideTransition.apply(
            self.clip,
            start_time,
            duration,
            direction
        )