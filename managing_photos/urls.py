from django.urls import path
from managing_photos.views import PhotoListView,  PhotoUpdateView, ObjectsView
from . import views

app_name = 'managing_photos'

urlpatterns = [
    path('', PhotoListView.as_view(), name = 'list_photo'),
    path('photo_delete/<int:id>', views.delete_photo, name='delete_photo'),
    path('photo_update/<int:pk>', PhotoUpdateView.as_view(), name='photo_update'),
    path('upload/', views.upload, name = 'upload'),
    path('objects_view/', ObjectsView.as_view(), name = 'objects_name'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('create_photo/', views.create_photo, name = 'create_photo')
]
