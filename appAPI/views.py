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


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer
# Create your views here.

class Bookmarks(object):
    pass

class ChartDataViewSet(viewsets.ModelViewSet):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer

    def get_queryset(self):
        engine = create_engine('mysql+pymysql://root:@localhost/test?charset=utf8', echo=True)
        metadata = MetaData(engine)
        moz_bookmarks = Table('teacher_final_data', metadata, autoload=True)
        mapper(Bookmarks, moz_bookmarks)
        Session = sessionmaker(bind=engine)
        session = Session()
        res = session.query(Bookmarks).filter('inst_name')
        for result in res:
            print result['inst_name']




        # conn = engine.connect(close_with_result=True)
        # result = conn.execute('SELECT * FROM teacher_final_data;')
        #
        # # after you iterate over the results, the result and connection get closed
        # for row in result:
        #     print(row['inst_name'])

            # or you can explicitly close the result, which also closes the connection

        # Session = sessionmaker(bind=engine)
        # session = Session()
        # for student in session.query('inst_name','year'):
        #     print student.inst_name, student.year

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






