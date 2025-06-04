import os
import statistics

from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip, AudioFileClip
from moviepy.video.fx import FadeIn, FadeOut 
import numpy as np
from PIL import Image, ImageOps


class SlideShow:
    def __init__(self, images, config={}):
        self.images = images
        self.resized_images = []
        self.size = config.get('size', (480,768)) # 480p 16:8 in portrait by default
        self.orientation = config.get('orientation') or 'portrait'
        self.image_duration = config.get('image_duration', 2)  # seconds each image stays fully visible
        self.transition_duration = config.get('transition_duration', 2)
        self.total_duration = 0
        self.config = config

    def convert_aspect_ratio(self, img, target_size):
        w_a, h_a = img.size
        w_b, h_b = target_size

        aspect_a = w_a / h_a
        aspect_b = w_b / h_b
        if aspect_a > aspect_b:
            # A is wider — crop width
            new_width = int(h_a * aspect_b)
            left = (w_a - new_width) // 2
            return img.crop((left, 0, left + new_width, h_a))
        elif aspect_a < aspect_b:
            # A is taller — crop height
            new_height = int(w_a / aspect_b)
            top = (h_a - new_height) // 2
            return img.crop((0, top, w_a, top + new_height))
        return img  # Aspect ratios are equal, no crop needed   

    def resize_image(self, img, target_size):
        """
        Resize an image to the target size while maintaining aspect ratio.

        PIL Image.size = (width, height)
        """
        img = self.convert_aspect_ratio(img, target_size)
        return img.resize(target_size, Image.LANCZOS)

    def resize_images(self):
        for image in self.images:
            self.resized_images.append(self.resize_image(image, target_size=self.size))

    def create_slideshow(self):
        self.resize_images()
        fadein = FadeIn(self.transition_duration)
        fadeout = FadeOut(self.transition_duration)

        clips = []

        for i, image in enumerate(self.resized_images):
            start = 0 if i == 0 else i * (self.image_duration + self.transition_duration)
            end = start + self.image_duration + self.transition_duration if i < len(self.resized_images) - 1 else start + self.image_duration
            clip = ImageClip(np.array(image)).with_duration(end - start).with_start(start)
            if i > 0:
                clip = fadein.apply(clip)
            if i < len(self.resized_images) - 1:
                clip = fadeout.apply(clip)
            clips.append(clip)
        
        self.total_duration = clips[-1].end if clips else 0
        self.video = CompositeVideoClip(clips).with_duration(self.total_duration)

    def add_audio(self, audio_file_path):
        audioclip = AudioFileClip(audio_file_path).subclipped(0, self.total_duration)
        new_audioclip = CompositeAudioClip([audioclip])
        self.video.audio = new_audioclip

    def save(self, output_file_path):
        # Write video
        self.video.write_videofile(output_file_path, fps=24)

    @staticmethod
    def load_images(path):
        return [Image.open(os.path.join(path, img_file)) for img_file in os.listdir(path)]


if __name__ == "__main__":
    # Creates default Nic Cage slideshow with crossfade transitions
    images = SlideShow.load_images('./input_images')
    slideshow = SlideShow(images, config={'orientation': 'portrait', 'image_duration': 2, 'transition_duration': 2})
    slideshow.create_slideshow()
    slideshow.add_audio("audio/nic_cage.mp3")
    slideshow.save("crossfade_slideshow.mp4")

