from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('', views.monitor, name='monitor'),
    path('result/', views.result, name='try'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)