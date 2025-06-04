from PIL import Image

from slideshow import SlideShow

import unittest

class TestSlideshow(unittest.TestCase):
    def setUp(self):
        pass

    def test_resize_image(self):
        slideshow = SlideShow([], config={'orientation': 'portrait', 'size': (300, 450)})
        img = Image.new(mode="RGB", size=(400, 600))
        resized_img = slideshow.resize_image(img, target_size=(300, 450))
        self.assertEqual(resized_img.size, (300, 450))

    def test_resize_images(self):
        images = [Image.new(mode="RGB", size=(400, 600)), Image.new(mode="RGB", size=(200, 300)), Image.new(mode="RGB", size=(300, 450))]
        slideshow = SlideShow(images, config={'orientation': 'portrait', 'size': (300, 450)})
        slideshow.resize_images()
        self.assertEqual(len(slideshow.resized_images), len(images))
        for img in slideshow.resized_images:
            self.assertEqual(img.size, (300, 450))
    
    def test_create_slideshow(self):
        images = [Image.new(mode="RGB", size=(400, 600)), Image.new(mode="RGB", size=(200, 300)), Image.new(mode="RGB", size=(200, 300))]
        slideshow = SlideShow(images, config={'orientation': 'portrait', 'image_duration': 2, 'transition_duration': 2, 'size': (300, 450)})
        slideshow.create_slideshow()

        self.assertEqual(slideshow.video.start, 0)
        self.assertEqual(slideshow.video.end, 10)
        self.assertEqual(len(slideshow.video.clips), 3)
