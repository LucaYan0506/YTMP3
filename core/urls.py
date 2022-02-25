from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name="index"),
    path('convert/',views.convert,name="convert"),
    path('download/',views.download,name="download"),
    path('check_task/',views.check_task,name="check_task"),
]
