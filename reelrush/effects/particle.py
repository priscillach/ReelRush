import numpy as np
import cv2

class ParticleEffect:
    def __init__(self, num_particles):
        """Initialize particle system.
        
        Args:
            num_particles (int): Number of particles to simulate
        """
        self.num_particles = num_particles
        self.particles = []
        
    def initialize_particles(self, origin):
        """Initialize particles at given origin point.
        
        Args:
            origin (tuple): (x,y) coordinates for particle origin
        """
        self.particles = []
        for _ in range(self.num_particles):
            # 使用 float 数组来存储位置和速度
            angle = np.random.uniform(0, 2*np.pi)
            speed = np.random.uniform(100, 300)
            particle = {
                'pos': np.array(origin, dtype=np.float64),  # 改为 float64
                'vel': np.array([
                    speed * np.cos(angle),
                    speed * np.sin(angle)
                ], dtype=np.float64),  # 改为 float64
                'life': np.random.uniform(0.5, 1.0)
            }
            self.particles.append(particle)
            
    def update_particles(self, dt):
        """Update particle positions and lifetimes.
        
        Args:
            dt (float): Time step for simulation
        """
        for p in self.particles:
            # 更新位置 (使用 float64 计算)
            p['pos'] = p['pos'] + p['vel'] * dt
            # 添加重力效果
            p['vel'][1] += 500 * dt  # 向下的加速度
            # 减少生命值
            p['life'] -= dt
            
        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def render(self, frame, t):
        """Render particles onto frame.
        
        Args:
            frame: Video frame to draw on
            t (float): Current time
        """
        for p in self.particles:
            if p['life'] > 0:
                # 转换为整数坐标进行绘制
                pos = p['pos'].astype(np.int32)
                alpha = p['life']  # 使用生命值作为透明度
                cv2.circle(
                    frame,
                    (pos[0], pos[1]),
                    2,
                    (255, 255, 255),
                    -1
                )
        return frame 