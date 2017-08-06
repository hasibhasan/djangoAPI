# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Task, ChartData
from rest_framework import viewsets
from .serializers import TaskSerializer
from .serializers import ChartDataSerializer
from django.db.models import Sum, Avg, Min, Max
from rest_framework import generics
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker,mapper
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer
# Create your views here.


class ChartDataViewSet(viewsets.ModelViewSet):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer



class CustomGet(APIView):
    def get(self, request, format=None):
        engine = create_engine('mysql+pymysql://root:@localhost/test?charset=utf8', echo=True)
        conn = engine.connect(close_with_result=True)
        agg = request.GET.get('agg', None)
        if agg == "sum":
            # queryset = ChartData.objects.values('label').annotate(value=Sum('value'))
            result = conn.execute('SELECT district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        elif agg == "avg":
            # queryset = ChartData.objects.values('label').annotate(value=Avg('value'))
            result = conn.execute('SELECT district as label, AVG(salary_basic) as value FROM teacher_final_data group by district;')
        elif agg == "min":
            # queryset = ChartData.objects.values('label').annotate(value=Min('value'))
            result = conn.execute(
                'SELECT district as label, MIN(salary_basic) as value FROM teacher_final_data group by district;')
        elif agg == "max":
            # queryset = ChartData.objects.values('label').annotate(value=Max('value'))
            result = conn.execute(
                'SELECT district as label, MAX(salary_basic) as value FROM teacher_final_data group by district;')
        else:
            result =  conn.execute('SELECT district, SUM(salary_basic) as newVal FROM teacher_final_data group by district;');
        # result = conn.execute(
        #     'SELECT district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        a = json.dumps([dict(r) for r in result], cls=DjangoJSONEncoder)
        b = json.JSONDecoder().decode(a)
        response = Response(b, status=status.HTTP_200_OK)
        return response