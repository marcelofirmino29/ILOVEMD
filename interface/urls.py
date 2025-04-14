from django.contrib import admin
from django.urls import path
from interface.views import home # Importa a view diretamente
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'), # Mapeia a raiz para a view 'home'
    path('admin/', admin.site.urls),
]

# Configuração para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)