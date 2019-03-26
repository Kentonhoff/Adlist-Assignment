from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('', views.AdListView.as_view()),
    path('ads', views.AdListView.as_view(), name='ads'),
    path('ads/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/create',
        views.AdCreateView.as_view(success_url=reverse_lazy('ads')), name='ad_create'),
    path('ads/<int:pk>/update',
        views.AdUpdateView.as_view(success_url=reverse_lazy('ads')), name='ad_update'),
    path('ads/<int:pk>/delete',
        views.AdDeleteView.as_view(success_url=reverse_lazy('ads')), name='ad_delete'),
]