from django.urls import path
from . import views

urlpatterns = [
    path('test1/<b_id>', views.test1),
    path('data_display/', views.data_display)
]