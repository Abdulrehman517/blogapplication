from django.urls import path
from .views import PostView
app_name = 'api'

urlpatterns = [
    path('list', PostView.as_view(),name='post_list'),
]