from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.FadeOut import FadeOut
from moviepy.video.fx.FadeIn import FadeIn

class TransitionEffect:
    @staticmethod
    def fade(clip1, clip2, duration=1.0):
        """Create a fade transition between two clips.
        
        Args:
            clip1: First video clip
            clip2: Second video clip
            duration: Duration of the fade effect
        """
        clip1 = clip1.FadeOut(duration)
        clip2 = clip2.FadeIn(duration)
        return concatenate_videoclips([clip1, clip2])
    
    @staticmethod
    def slide(clip1, clip2, direction='left', duration=1.0):
        """Create a slide transition between clips.
        
        Args:
            clip1: First video clip
            clip2: Second video clip
            direction: Direction of slide ('left', 'right', 'up', 'down')
            duration: Duration of the slide effect
        """
        w, h = clip1.size
        
        def make_frame(t):
            progress = t / duration
            if direction in ['left', 'right']:
                offset = int(w * progress) if direction == 'left' else int(w * (1 - progress))
                return clip2.get_frame(t)[:, offset:] if direction == 'left' else clip1.get_frame(t)[:, :offset]
            else:
                offset = int(h * progress) if direction == 'up' else int(h * (1 - progress))
                return clip2.get_frame(t)[offset:, :] if direction == 'up' else clip1.get_frame(t)[:offset, :]
        
        return VideoFileClip(make_frame, duration=duration) 