import sys
import subprocess
import pkg_resources
from reelrush.effects_processor import (
    VideoProcessingParams, 
    TextEffectParams,
    SlowMotionParams,
    FreezeFrameParams,
    CameraShakeParams,
    GlitchParams,
    ParticleExplosionParams,
    ZoomParams,
    FlashCutsParams,
    SlideTransitionParams,
    FilterParams,
    process_video_effects
)

def check_dependencies():
    """检查依赖项是否安装"""
    required = {'moviepy', 'numpy', 'opencv-python'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    
    if missing:
        print("Installing missing packages...")
        subprocess.check_call(['pip', 'install', *missing])

def test_video_effects():
    """测试视频特效处理"""
    # 创建处理参数
    params = VideoProcessingParams(
        video_path="origin.mp4",
        
        # 文字特效
        text_effects=[
            TextEffectParams(
                text="BASKETBALL HIGHLIGHTS",
                start_time=0.5,
                duration=3,
                fontsize=80,
                animation='fade',
                stroke_color='black',
                stroke_width=1,
                font_style='elegant',
                blur_background='box_blur'
            ),
            TextEffectParams(
                text="AMAZING SHOT!",
                start_time=10.5,
                duration=2,
                fontsize=100,
                animation='fade',
                color='yellow',
                stroke_color='red',
                stroke_width=3,
                font_style='impact'
            )
        ],
        
        # 慢动作特效
        slow_motion_effects=[
            SlowMotionParams(
                start_time=11,
                duration=3,
                speed=0.6,
                abruptness=0,
                soonness=1
            )
        ],
        
        # 冻结帧特效
        freeze_frame_effects=[
            FreezeFrameParams(
                start_time=6,
                duration=1
            )
        ],
        
        # 镜头抖动特效
        camera_shake_effects=[
            CameraShakeParams(
                start_time=4,
                duration=3,
                intensity=0.3
            )
        ],
        
        # 故障特效
        glitch_effects=[
            GlitchParams(
                start_time=20,
                duration=0.5
            )
        ],
        
        # 粒子爆炸特效
        particle_effects=[
            ParticleExplosionParams(
                start_time=25,
                duration=1.5,
                num_particles=300,
                position=(0.7, 0.3)
            )
        ],
        
        # 缩放特效
        zoom_effects=[
            ZoomParams(
                start_time=28,
                duration=1.5,
                zoom_factor=1.8
            )
        ],
        
        # 闪光切换特效
        flash_cuts=FlashCutsParams(
            timestamps=[30, 31, 32, 33],
            cut_duration=0.4,
            flash_intensity=0.7
        ),
        
        # 滑动转场特效
        slide_transitions=[
            SlideTransitionParams(
                start_time=12,
                duration=1.0,
                direction='left'
            )
        ],
        
        # 滤镜特效
        filter_effects=[
            FilterParams(
                start_time=15,
                duration=5,
                filter_name='grayscale'
            ),
            FilterParams(
                start_time=31,
                duration=1,
                filter_name='gaussian_blur'
            ),
            FilterParams(
                start_time=33,
                duration=2,
                filter_name='motion_blur'
            )
        ]
    )
    
    # 处理视频并保存
    process_video_effects(params, "target.mp4", fps=30)

if __name__ == "__main__":
    try:
        check_dependencies()
        test_video_effects()
    except Exception as e:
        print(f"Error: {str(e)}") 