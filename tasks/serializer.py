from rest_framework import serializers


# local import
from . models import Task, Image
from django.conf import settings

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class TaskSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many = True, read_only = True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority', 'due_date', 'is_completed', 'images')


