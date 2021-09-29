from django.urls import path
from .views import PostView, UploadCSV
app_name = 'api'

urlpatterns = [
    path('list', PostView.as_view(), name='post_list'),

    path('uploadcsv/', UploadCSV.as_view(), name='uploadcsv_post'),

]