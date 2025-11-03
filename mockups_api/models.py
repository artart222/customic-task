import uuid

from django.db import models


class MockupTask(models.Model):
    task_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    # NOTE: If you use uuid.uuid4() then Django will call uuid.uuid4() once at startup
    # and reuse the same UUID for all new rows
    message = models.TextField(blank=True, null=True)
    status = models.TextField()
    text = models.TextField(blank=False, null=False)
    font = models.TextField(blank=True, null=True)
    text_color = models.TextField(blank=True, null=True)
    shirt_color = models.JSONField(blank=True, null=True)
    results = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.JSONField(blank=True, null=True)


class Mockup(models.Model):
    task = models.ForeignKey(
        MockupTask, on_delete=models.SET_NULL, null=True, blank=True
    )
    text = models.TextField(blank=True, null=True)
    font = models.TextField(blank=True, null=True)
    text_color = models.TextField(blank=True, null=True)
    shirt_color = models.JSONField(default=list, blank=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
