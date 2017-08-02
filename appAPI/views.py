# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Task, ChartData
from rest_framework import viewsets
from .serializers import TaskSerializer
from .serializers import ChartDataSerializer
from django.db.models import Sum, Avg, Min, Max
from rest_framework import generics


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer
# Create your views here.


class ChartDataViewSet(viewsets.ModelViewSet):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer

    def get_queryset(self):
        agg = self.request.query_params.get('agg', None)
        if agg == "sum":
            queryset = ChartData.objects.values('label').annotate(value=Sum('value'))
        elif agg == "avg":
            queryset = ChartData.objects.values('label').annotate(value=Avg('value'))
        elif agg == "min":
            queryset = ChartData.objects.values('label').annotate(value=Min('value'))
        elif agg == "max":
            queryset = ChartData.objects.values('label').annotate(value=Max('value'))
        else:
            queryset = ChartData.objects.all()
        return queryset






