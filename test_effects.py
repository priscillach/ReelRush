import sys
import subprocess
import pkg_resources

def check_dependencies():
    """检查并安装所需依赖"""
    try:
        import pip
        print("正在安装/更新依赖...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'moviepy'], stdout=subprocess.DEVNULL)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'opencv-python'], stdout=subprocess.DEVNULL)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'numpy'], stdout=subprocess.DEVNULL)
        print("依赖安装完成")
    except Exception as e:
        print(f"安装依赖时出错: {e}")
        raise

def test_video_effects():
    from reelrush import VideoEditor
    
    # 创建视频编辑器实例
    input_path = "./origin.mp4"
    
    # 检查输入文件是否存在
    import os
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到输入视频文件: {input_path}")
    
    editor = VideoEditor(input_path)
    
    print("开始添加特效...")
    
    # 1. 在开始添加淡入效果
    print("添加开场文字...")
    editor.add_animated_text(
        "Basketball Highlights", 
        start_time=0.5, 
        duration=3,
        fontsize=80,
        animation='fade',
        stroke_color='black',
        stroke_width=2
    )
    
    # 2. 在精彩时刻添加慢动作
    editor.add_slow_motion(
        start_time=11,
        end_time=14,
        speed=0.6,
        abruptness=0,
        soonness=1
    )

    # 3. 添加冻结帧
    editor.add_freeze_frame(
        timestamp=6,
        duration=1
    )
    
    # 4. 添加镜头摇晃效果
    editor.add_camera_shake(
        start_time=4,
        duration=3,
        intensity=0.3
    )
    
    # 5. 添加画面故障效果
    editor.add_glitch(
        timestamp=20,
        duration=0.5
    )
    
    # 6. 添加粒子爆炸效果
    editor.add_particle_explosion(
        timestamp=25,
        duration=1.5,
        num_particles=300,
        position=(0.7, 0.3)  # 在屏幕70%宽度，30%高度的位置
    )
    
    # 7. 添加动态缩放
    editor.add_zoom(
        timestamp=28,
        duration=1.5,
        zoom_factor=1.8
    )
    
    # 8. 添加快速切换效果，用在片段分割间
    editor.add_flash_cuts(
        timestamps=[30, 31, 32, 33],
        cut_duration=0.4,
        flash_intensity=0.7
    )

    # 9. 添加滑动转场效果，用在片段分割间
    editor.add_slide_transition(
    timestamp=12,
    duration=1.0,
    direction='left'  # 可选: 'left', 'right', 'up', 'down'
)
    # 10. 添加滤镜效果
    editor.add_filter(
        filter_name='grayscale',  # 可选: 'grayscale', 'sepia', 'warm', 'cool', 'vintage'
        start_time=15,
        duration=5
    )
    
    editor.save("target.mp4", fps=30)

if __name__ == "__main__":
    try:
        test_video_effects()
    except Exception as e:
        import traceback
        traceback.print_exc() 