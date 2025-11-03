from django.test import SimpleTestCase

from mockups_api.tasks import calculate_good_text_color


class CalculateGoodTextColorTest(SimpleTestCase):
    def test_light_text_on_dark_background(self):
        rgb = (200, 200, 200)
        self.assertEqual(calculate_good_text_color(rgb), (0, 0, 0))

    def test_dark_text_on_light_background(self):
        rgb = (100, 100, 100)
        self.assertEqual(calculate_good_text_color(rgb), (255, 255, 255))
