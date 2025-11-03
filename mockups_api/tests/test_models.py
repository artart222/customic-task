from django.test import TestCase

from mockups_api.models import MockupTask


class TestMockupTaskModel(TestCase):
    # NOTE: setUp methods runs before every test because of its special name.
    def setUp(self):
        self.mockup_task_model = MockupTask.objects.create(
            text="Hello",
            status="PENDING",
            message="ساخت تصویر آغاز شد",
            font="Lemynotes.ttf",
            text_color="#ffffff",
            shirt_color=["blue", "white"],
        )

    def test_mockup_initiated_correctly(self):
        self.assertEqual(self.mockup_task_model.text_color, "#ffffff")
        self.assertIsNotNone(self.mockup_task_model.created_at)
