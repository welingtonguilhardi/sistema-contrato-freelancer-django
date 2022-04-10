from . import views
from django.contrib import admin
from django.urls import path,include
from jobs.views import JobsAll, JobsNovo, JobsUpdate

urlpatterns = [
    path('encontrar_jobs/', views.encontrar_jobs, name="encontrar_jobs"),
    path('aceitar_job/<int:id>/', views.aceitar_job, name="aceitar_job"),
    path('perfil/', views.perfil, name="perfil"),
    path('enviar_projeto/', views.enviar_projeto, name="enviar_projeto"),
    path('novo/',JobsNovo.as_view(), name='job-novo'),
    path('all/',JobsAll.as_view(), name='all'),
    path('update/<int:pk>/',JobsUpdate.as_view(), name='update'),
]
