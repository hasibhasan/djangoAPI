# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Task, ChartData
from rest_framework import viewsets
from .serializers import TaskSerializer
from .serializers import ChartDataSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer
# Create your views here.

class ChartDataViewSet(viewsets.ModelViewSet):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer