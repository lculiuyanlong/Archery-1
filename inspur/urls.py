# -*- coding: UTF-8 -*-
from django.urls import path
from inspur import views

urlpatterns = [
    path('sqlupdate1/', views.sqlupdate1),
]