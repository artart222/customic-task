from rest_framework import serializers
from .models import Mockup, MockupTask


class MockupTaskGenerateBodySerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True, allow_blank=False)
    font = serializers.CharField(required=False, allow_blank=True)
    text_color = serializers.CharField(required=False, allow_blank=True)
    shirt_color = serializers.JSONField(required=False)

    class Meta:
        model = MockupTask
        fields = [
            "text",
            "font",
            "text_color",
            "shirt_color",
        ]


class MockupTaskGenerateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockupTask
        fields = [
            "task_id",
            "status",
            "message",
        ]
        read_only_fields = fields


class MockupTaskGetResponseSerializer(serializers.ModelSerializer):
    # NOTE: This tells DRF that results is a computed field.
    results = serializers.SerializerMethodField()

    class Meta:
        model = MockupTask
        fields = ["task_id", "status", "results"]

    # NOTE: get_something allow me to give data for something field.
    def get_results(self, obj):
        # NOTE: Filter enables me to get more than one object with task_id.
        print(len(Mockup.objects.filter(task_id=obj.task_id)))
        if len(Mockup.objects.filter(task_id=obj.task_id)) == 0:
            return {"result": {}}
        else:
            return_data = []
            for i in Mockup.objects.filter(task_id=obj.task_id):
                return_data.append(
                    {"image_url": i.image_url, "created_at": i.created_at}
                )
        return return_data


class MockupGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mockup
        fields = [
            "id",
            "text",
            "image_url",
            "font",
            "text_color",
            "shirt_color",
            "created_at",
        ]
