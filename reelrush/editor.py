from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import cv2
import numpy as np
from reelrush.effects.filter import VideoFilter
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

class VideoEditor:
    def __init__(self, video_path):
        """Initialize the video editor with a video file.
        
        Args:
            video_path (str): Path to the input video file
        """
        self.video_path = video_path
        self.clip = VideoFileClip(video_path)
        self.effects = []
    
    def add_freeze_frame(self, timestamp, duration=2):
        """Add a freeze frame effect at the specified timestamp.
        
        Args:
            timestamp (float): Time in seconds where to freeze
            duration (float): Duration of freeze in seconds
        """
        self.clip = FreezeFrame.apply(self.clip, timestamp, duration)
        
        
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
    
    def add_glitch(self, timestamp, duration=0.5):
        """Add glitch effect at specified timestamp.
        
        Args:
            timestamp (float): Time in seconds to add glitch
            duration (float): Duration of glitch effect
        """
        self.clip = GlitchEffect.apply(self.clip, timestamp, duration)
    
    def add_slow_motion(self, start_time, end_time, speed=0.5, abruptness= 0, soonness=1):
        """Add slow motion effect to a segment of video.
        
        Args:
            start_time (float): Start time in seconds
            end_time (float): End time in seconds
            speed (float): Playback speed (0.1 to 1.0)
        """
        self.clip = SlowMotion.apply(self.clip, start_time, end_time, speed, abruptness, soonness)

    def add_zoom(self, timestamp, duration, zoom_factor=1.5):
        """Add dynamic zoom effect.
        
        Args:
            timestamp (float): Start time of zoom
            duration (float): Duration of zoom effect
            zoom_factor (float): Maximum zoom level
        """
        self.clip = DynamicZoom.apply(self.clip, timestamp, duration, zoom_factor)

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

    def add_filter(self, filter_type, **kwargs):
        """Apply video filter effect.
        
        Args:
            filter_type (str): Type of filter ('grayscale', 'sepia', 'vignette', 'rgb_shift')
            **kwargs: Additional filter parameters
        """
        filter_funcs = {
            'grayscale': VideoFilter.grayscale,
            'sepia': VideoFilter.sepia,
            'vignette': lambda f: VideoFilter.vignette(f, kwargs.get('intensity', 0.5)),
            'rgb_shift': lambda f: VideoFilter.rgb_shift(f, kwargs.get('offset', 10))
        }
        
        if filter_type not in filter_funcs:
            raise ValueError(f"Unknown filter type: {filter_type}")
        
        def apply_filter(frame, t):
            return filter_funcs[filter_type](frame)
        
        self.clip = self.clip.fl(apply_filter)

    def add_animated_text(self, text, start_time, duration, 
                         position='center', fontsize=70, color='white',
                         animation='fade', stroke_color='black', stroke_width=2):
        """Add animated text overlay.
        
        Args:
            text (str): Text to display
            start_time (float): Start time in seconds
            duration (float): Duration to display text
            position (str/tuple): Position of text ('center' or (x,y))
            fontsize (int): Font size
            color (str): Text color
            animation (str): Animation type ('fade', 'slide', 'scale')
        """
        self.clip = DynamicText.animated_text(
            self.clip, text, start_time, duration,
            position, fontsize, color, animation, stroke_color, stroke_width
        )

    def add_particle_explosion(self, timestamp, duration=1.0, num_particles=100):
        """Add particle explosion effect.
        
        Args:
            timestamp (float): Time to trigger explosion
            duration (float): Duration of effect
            num_particles (int): Number of particles
        """
        particles = ParticleEffect(num_particles)
        
        def particle_transform(get_frame, t):
            # 获取当前帧
            frame = get_frame(t)
            
            if timestamp <= t <= timestamp + duration:
                # Get center of frame for explosion origin
                height, width = frame.shape[:2]
                origin = (width // 2, height // 2)
                
                # Initialize particles if this is the start
                if abs(t - timestamp) < 0.1:  # 使用近似值检查
                    particles.initialize_particles(origin)
                
                # Update and render particles
                particles.update_particles(1/self.clip.fps)
                return particles.render(frame.copy(), t)
            return frame
        
        self.clip = self.clip.transform(particle_transform)

    def add_flash_cuts(self, timestamps, cut_duration=0.1, flash_intensity=1.0):
        """Add flash cut effect at specified timestamps.
        
        Args:
            timestamps (list): List of timestamps for flash transitions
            cut_duration (float): Duration of flash transition effect
            flash_intensity (float): Intensity of flash effect (0 to 1)
        """
        # 获取基础视频
        base_clip = self.clip
        if isinstance(self.clip, CompositeVideoClip):
            base_clip = self.clip.clips[0]  # 获取主视频层
        
        clips = []
        timestamps.sort()
        
        # 处理第一个片段
        if timestamps[0] > 0:
            first_clip = base_clip.subclipped(0, timestamps[0])
            if isinstance(self.clip, CompositeVideoClip):
                # 为第一个片段添加其他效果层
                other_layers = [layer.subclipped(0, timestamps[0]) for layer in self.clip.clips[1:]]
                first_clip = CompositeVideoClip([first_clip] + other_layers)
            clips.append(first_clip)
        
        # 处理中间片段
        for i in range(len(timestamps) - 1):
            start, end = timestamps[i], timestamps[i + 1]
            current_clip = base_clip.subclipped(start, end)
            if isinstance(self.clip, CompositeVideoClip):
                # 为中间片段添加其他效果层
                other_layers = [layer.subclipped(start, end) for layer in self.clip.clips[1:]]
                current_clip = CompositeVideoClip([current_clip] + other_layers)
            clips.append(current_clip)
        
        # 处理最后一个片段
        if timestamps[-1] < self.clip.duration:
            last_clip = base_clip.subclipped(timestamps[-1], self.clip.duration)
            if isinstance(self.clip, CompositeVideoClip):
                # 为最后片段添加其他效果层
                other_layers = [layer.subclipped(timestamps[-1], self.clip.duration) 
                              for layer in self.clip.clips[1:]]
                last_clip = CompositeVideoClip([last_clip] + other_layers)
            clips.append(last_clip)
        
        # 应用闪光切换效果
        self.clip = FlashCut.create(
            clips,
            cut_duration=cut_duration,
            flash_intensity=flash_intensity
        )

    def add_slide_transition(self, timestamp, duration=1.0, direction='left'):
        """Add slide transition effect.
        
        Args:
            timestamp (float): Time to trigger transition
            duration (float): Duration of transition effect
            direction (str): Direction of slide ('left', 'right', 'up', 'down')
        """
        self.clip = SlideTransition.apply(
            self.clip,
            timestamp,
            duration,
            direction
        )