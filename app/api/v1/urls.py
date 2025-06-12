from django.urls import path
from .views import GetPDFView, GetAudioView

urlpatterns = [
    path('get-pdf/', GetPDFView.as_view(), name='get-pdf'),
    path('get-audio/', GetAudioView.as_view(), name='get-audio'),
]
