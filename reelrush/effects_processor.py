import logging
from dataclasses import dataclass
from typing import List, Union, Optional, Tuple
from moviepy import VideoFileClip
from .editor import VideoEditor

log = logging.getLogger()

# 基础特效参数类
@dataclass
class BaseEffectParams:
    start_time: float  # 特效开始时间（秒）
    duration: float    # 特效持续时间（秒）

    def validate(self) -> bool:
        if self.start_time < 0 or self.duration <= 0:
            log.error(f"Invalid timing parameters: start_time={self.start_time}, duration={self.duration}")
            return False
        return True

# 文字特效参数
@dataclass
class TextEffectParams(BaseEffectParams):
    text: str                                     # 要显示的文字内容
    position: Union[str, Tuple[int, int]] = 'center'  # 文字位置，可以是'center'或(x,y)坐标
    fontsize: int = 70                           # 字体大小（像素）
    color: str = 'white'                         # 字体颜色
    animation: str = 'fade'                      # 动画类型：'fade'(淡入淡出),'slide'(滑动),'scale'(缩放)
    stroke_color: str = 'black'                  # 描边颜色
    stroke_width: int = 2                        # 描边宽度（像素）
    font_style: str = 'default'                  # 字体样式：'default','bold','elegant','modern','impact','comic'
    blur_background: Optional[str] = None        # 背景模糊效果：None,'box_blur','gaussian_blur','glass','motion_blur'

    def validate(self) -> bool:
        if not super().validate():
            return False
        if not self.text:
            log.error("Text content cannot be empty")
            return False
        if isinstance(self.position, str) and self.position != 'center':
            log.error(f"Invalid position: {self.position}")
            return False
        if self.fontsize <= 0:
            log.error(f"Invalid font size: {self.fontsize}")
            return False
        if self.animation not in ['fade', 'slide', 'scale']:
            log.error(f"Invalid animation type: {self.animation}")
            return False
        return True

# 慢动作特效参数
@dataclass
class SlowMotionParams(BaseEffectParams):
    speed: float = 0.5      # 速度因子(0-1)，值越小越慢
    abruptness: float = 0   # 速度变化的突然程度(0-1)，0表示平滑变化，1表示突然变化
    soonness: float = 1     # 速度变化的时机(0-1)，0表示在结束时变化，1表示在开始时变化

    def validate(self) -> bool:
        if not super().validate():
            return False
        if not 0 < self.speed < 1:
            log.error(f"Invalid speed: {self.speed}")
            return False
        if not 0 <= self.abruptness <= 1:
            log.error(f"Invalid abruptness: {self.abruptness}")
            return False
        if not 0 <= self.soonness <= 1:
            log.error(f"Invalid soonness: {self.soonness}")
            return False
        return True

# 其他特效参数类...
@dataclass
class FreezeFrameParams(BaseEffectParams):
    """冻结帧特效参数"""
    def validate(self) -> bool:
        if not super().validate():
            log.error("Invalid freeze frame timing parameters")
            return False
        return True

@dataclass
class CameraShakeParams(BaseEffectParams):
    intensity: float = 0.5  # 抖动强度(0-1)，值越大抖动越剧烈

    def validate(self) -> bool:
        if not super().validate():
            return False
        if not 0 <= self.intensity <= 1:
            log.error(f"Invalid shake intensity: {self.intensity}")
            return False
        return True

@dataclass
class GlitchParams(BaseEffectParams):
    """故障特效参数"""
    def validate(self) -> bool:
        return super().validate()

@dataclass
class ParticleExplosionParams(BaseEffectParams):
    num_particles: int = 100                        # 粒子数量
    position: Union[str, Tuple[float, float]] = 'center'  # 爆炸中心位置，可以是'center'或(x,y)坐标(0-1范围)

    def validate(self) -> bool:
        if not super().validate():
            return False
        if self.num_particles <= 0:
            log.error(f"Invalid number of particles: {self.num_particles}")
            return False
        if isinstance(self.position, str) and self.position != 'center':
            log.error(f"Invalid particle position: {self.position}")
            return False
        if isinstance(self.position, tuple):
            x, y = self.position
            if not (0 <= x <= 1 and 0 <= y <= 1):
                log.error(f"Position coordinates must be between 0 and 1: {self.position}")
                return False
        return True

@dataclass
class ZoomParams(BaseEffectParams):
    zoom_factor: float = 1.5  # 缩放倍数，大于1表示放大，小于1表示缩小

    def validate(self) -> bool:
        if not super().validate():
            return False
        if self.zoom_factor <= 0:
            log.error(f"Invalid zoom factor: {self.zoom_factor}")
            return False
        return True

@dataclass
class FlashCutsParams:
    timestamps: List[float]           # 闪光切换的时间点列表（秒）
    cut_duration: float = 0.4         # 每次切换的持续时间（秒）
    flash_intensity: float = 0.7      # 闪光强度(0-1)，值越大越亮

    def validate(self) -> bool:
        if not self.timestamps:
            log.error("Flash cuts timestamps cannot be empty")
            return False
        if any(t < 0 for t in self.timestamps):
            log.error(f"Invalid timestamps (must be >= 0): {self.timestamps}")
            return False
        if self.cut_duration <= 0:
            log.error(f"Invalid cut duration: {self.cut_duration}")
            return False
        if not 0 <= self.flash_intensity <= 1:
            log.error(f"Invalid flash intensity: {self.flash_intensity}")
            return False
        return True

@dataclass
class SlideTransitionParams(BaseEffectParams):
    direction: str = 'left'  # 滑动方向：'left'(左移),'right'(右移),'up'(上移),'down'(下移)

    def validate(self) -> bool:
        if not super().validate():
            return False
        if self.direction not in ['left', 'right', 'up', 'down']:
            log.error(f"Invalid slide direction: {self.direction}")
            return False
        return True

@dataclass
class FilterParams(BaseEffectParams):
    filter_name: str  # 滤镜类型：'grayscale'(灰度),'sepia'(复古),'warm'(暖色),'cool'(冷色),'vintage'(老电影),
                     # 'gaussian_blur'(高斯模糊),'box_blur'(方框模糊),'glass'(毛玻璃),'motion_blur'(运动模糊)

    def validate(self) -> bool:
        if not super().validate():
            return False
        valid_filters = ['grayscale', 'sepia', 'warm', 'cool', 'vintage', 
                        'gaussian_blur', 'box_blur', 'glass', 'motion_blur']
        if self.filter_name not in valid_filters:
            log.error(f"Invalid filter name. Must be one of {valid_filters}")
            return False
        return True

# 视频处理参数结构体
@dataclass
class VideoProcessingParams:
    video_path: Optional[str] = None              # 输入视频文件路径
    video_file_clip: Optional[VideoFileClip] = None  # 或直接传入 VideoFileClip 对象
    text_effects: List[TextEffectParams] = None   # 文字特效列表
    slow_motion_effects: List[SlowMotionParams] = None  # 慢动作特效列表
    freeze_frame_effects: List[FreezeFrameParams] = None  # 冻结帧特效列表
    camera_shake_effects: List[CameraShakeParams] = None  # 镜头抖动特效列表
    glitch_effects: List[GlitchParams] = None     # 故障特效列表
    particle_effects: List[ParticleExplosionParams] = None  # 粒子爆炸特效列表
    zoom_effects: List[ZoomParams] = None         # 缩放特效列表
    flash_cuts: Optional[FlashCutsParams] = None  # 闪光切换特效
    slide_transitions: List[SlideTransitionParams] = None  # 滑动转场特效列表
    filter_effects: List[FilterParams] = None     # 滤镜特效列表

    def validate(self) -> bool:
        if not self.video_path and not self.video_file_clip:
            log.error("Either video_path or video_file_clip must be provided")
            return False
        return True

def process_video_effects(params: VideoProcessingParams, output_path: str, fps: int = 30) -> None:
    """处理视频特效

    Args:
        params: 视频处理参数
        output_path: 输出文件路径
        fps: 输出视频帧率
    """
    # 验证参数
    if not params.validate():
        log.error("Invalid video processing parameters")
        return

    # 初始化编辑器
    editor = VideoEditor(
        video_path=params.video_path,
        vide_file_clip=params.video_file_clip
    )

    # 收集所有时序特效
    timed_effects = []
    
    # 添加各类特效到列表
    effect_lists = [
        ('text', params.text_effects),
        ('slow_motion', params.slow_motion_effects),
        ('freeze', params.freeze_frame_effects),
        ('camera_shake', params.camera_shake_effects),
        ('glitch', params.glitch_effects),
        ('particle', params.particle_effects),
        ('zoom', params.zoom_effects),
        ('slide', params.slide_transitions),
        ('filter', params.filter_effects)
    ]

    for effect_type, effects in effect_lists:
        if effects:
            for effect in effects:
                if effect.validate():
                    timed_effects.append((effect_type, effect))
                else:
                    log.warning(f"Skipping invalid {effect_type} effect")

    # 按开始时间排序
    timed_effects.sort(key=lambda x: x[1].start_time)

    # 按顺序应用特效
    for effect_type, effect in timed_effects:
        if effect_type == 'text':
            editor.add_animated_text(
                text=effect.text,
                start_time=effect.start_time,
                duration=effect.duration,
                position=effect.position,
                fontsize=effect.fontsize,
                color=effect.color,
                animation=effect.animation,
                stroke_color=effect.stroke_color,
                stroke_width=effect.stroke_width,
                font_style=effect.font_style,
                blur_background=effect.blur_background
            )
        elif effect_type == 'slow_motion':
            editor.add_slow_motion(
                start_time=effect.start_time,
                end_time=effect.start_time + effect.duration,
                speed=effect.speed,
                abruptness=effect.abruptness,
                soonness=effect.soonness
            )
        elif effect_type == 'freeze':
            editor.add_freeze_frame(
                start_time=effect.start_time,
                duration=effect.duration
            )
        elif effect_type == 'camera_shake':
            editor.add_camera_shake(
                start_time=effect.start_time,
                duration=effect.duration,
                intensity=effect.intensity
            )
        elif effect_type == 'glitch':
            editor.add_glitch(
                start_time=effect.start_time,
                duration=effect.duration
            )
        elif effect_type == 'particle':
            editor.add_particle_explosion(
                start_time=effect.start_time,
                duration=effect.duration,
                num_particles=effect.num_particles,
                position=effect.position
            )
        elif effect_type == 'zoom':
            editor.add_zoom(
                start_time=effect.start_time,
                duration=effect.duration,
                zoom_factor=effect.zoom_factor
            )
        elif effect_type == 'slide':
            editor.add_slide_transition(
                start_time=effect.start_time,
                duration=effect.duration,
                direction=effect.direction
            )
        elif effect_type == 'filter':
            editor.add_filter(
                filter_name=effect.filter_name,
                start_time=effect.start_time,
                duration=effect.duration
            )

    # 最后处理 flash_cuts
    if params.flash_cuts:
        if params.flash_cuts.validate():
            editor.add_flash_cuts(
                timestamps=params.flash_cuts.timestamps,
                cut_duration=params.flash_cuts.cut_duration,
                flash_intensity=params.flash_cuts.flash_intensity
            )
        else:
            log.warning("Skipping invalid flash_cuts effect")

    # 保存结果
    editor.save(output_path, fps=fps) 