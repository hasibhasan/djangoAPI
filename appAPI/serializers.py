from rest_framework import serializers
from .models import Task
from .models import ChartData

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_name', 'task_description')

class ChartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartData
        fields =('label', 'value')