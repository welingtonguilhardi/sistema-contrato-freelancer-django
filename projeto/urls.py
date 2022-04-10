from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('autenticacao.urls')),
    path('jobs/',include('jobs.urls')),
]
#cria url para os arquivos de Referencias que são baixados no site 
from django.conf import settings
from django.conf.urls.static import static
...
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#para entender melhor veja o settings e pesquise MEDIA_ROOT,MEDIA_URL

