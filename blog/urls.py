from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),

    path('export/', views.export_blog, name='export_csv'),

    path('upload_csv/', views.upload_csv, name='uploading_csv'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),

    path('<int:post_id>/share/',views.post_share, name='post_share'),
]