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
import pandas as pd



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer
# Create your views here.


class ChartDataViewSet(viewsets.ModelViewSet):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer



class CustomGet(APIView):
    def get(self, request, format=None):

        variables = json.loads(request.GET.get('variables', None))
        for item in variables:
            print item['variable_name']
            if item['axis'] == 'x':
                xaxis = item['variable_name']
            if item['axis'] == 'y':
                yaxis = item['variable_name']

        #collection name check
        if variables[0]['collection_name'] == variables[1]['collection_name']:
            collectionname = variables[0]['collection_name']


        engine = create_engine('mysql+pymysql://root:@localhost/test?charset=utf8', echo=True)
        conn = engine.connect(close_with_result=True)

        cnx = engine.raw_connection()
        xx = pd.read_sql('Select '+ xaxis +' as label, '+ yaxis +' as value FROM '+ collectionname, cnx)



        xxsum = xx.groupby(['label']).sum()
        xxsum['index_col'] = range(1, len(xxsum) + 1)
        xxmin = xx.groupby(['label']).min()
        xxmin['index_col'] = range(1, len(xxmin) + 1)
        xxmax = xx.groupby(['label']).max()
        xxmax['index_col'] = range(1, len(xxmax) + 1)
        xxavg = xx.groupby(['label']).mean()
        xxavg['index_col'] = range(1, len(xxavg) + 1)

        resultsumdump = json.JSONDecoder().decode(xxsum.reset_index().to_json(orient="records"))
        resultmindump = json.JSONDecoder().decode(xxmin.reset_index().to_json(orient="records"))
        resultmaxdump = json.JSONDecoder().decode(xxmax.reset_index().to_json(orient="records"))
        resultavgdump = json.JSONDecoder().decode(xxavg.reset_index().to_json(orient="records"))





        # resultsum = conn.execute('Select district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        # resultAvg = conn.execute('SELECT district as label, AVG(salary_basic) as value FROM teacher_final_data group by district;')
        # resultMin = conn.execute('SELECT district as label, MIN(salary_basic) as value FROM teacher_final_data group by district;')
        # resultMax = conn.execute('SELECT district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        #
        # resultsumdump = json.JSONDecoder().decode(json.dumps([dict(r) for r in resultsum], cls=DjangoJSONEncoder))
        # resultavgdump = json.JSONDecoder().decode(json.dumps([dict(r) for r in resultAvg], cls=DjangoJSONEncoder))
        # resultmindump = json.JSONDecoder().decode(json.dumps([dict(r) for r in resultMin], cls=DjangoJSONEncoder))
        # resultmaxdump = json.JSONDecoder().decode(json.dumps([dict(r) for r in resultMax], cls=DjangoJSONEncoder))

        finalRes =[];
        finalRes.append({"sum": resultsumdump,"avg": resultavgdump, "min": resultmindump, "max": resultmaxdump})

        # agg = request.GET.get('agg', None)
        # if agg == "sum":
        #     # queryset = ChartData.objects.values('label').annotate(value=Sum('value'))
        #     result = conn.execute('Select district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        # elif agg == "avg":
        #     # queryset = ChartData.objects.values('label').annotate(value=Avg('value'))
        #     result = conn.execute('SELECT id, district as label, AVG(salary_basic) as value FROM teacher_final_data group by district;')
        # elif agg == "min":
        #     # queryset = ChartData.objects.values('label').annotate(value=Min('value'))
        #     result = conn.execute(
        #         'SELECT id, district as label, MIN(salary_basic) as value FROM teacher_final_data group by district;')
        # elif agg == "max":
        #     # queryset = ChartData.objects.values('label').annotate(value=Max('value'))
        #     result = conn.execute(
        #         'SELECT id, district as label, MAX(salary_basic) as value FROM teacher_final_data group by district;')
        # else:
        #     result = conn.execute(
        #         'SELECT  id, district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        # # result = conn.execute(
        # #     'SELECT district as label, SUM(salary_basic) as value FROM teacher_final_data group by district;')
        # a = json.dumps([dict(r) for r in result], cls=DjangoJSONEncoder)
        # b = json.JSONDecoder().decode(a)
        response = Response(finalRes, status=status.HTTP_200_OK)
        return response