from django.urls import path
from managing_photos.views import PhotoListView,  PhotoUpdateView, ObjectsView, UploadFail, ConfirmAllDelete
from . import views

app_name = 'managing_photos'

urlpatterns = [
    path('', PhotoListView.as_view(), name = 'list_photo'),
    path('photo_delete/<int:id>', views.delete_photo, name='delete_photo'),
    path('photo_update/<int:pk>', PhotoUpdateView.as_view(), name='photo_update'),
    path('upload/', views.upload, name = 'upload'),
    path('objects_view/', ObjectsView.as_view(), name = 'objects_view'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('create_photo/', views.create_photo, name = 'create_photo'),
    path('upload_fail/', UploadFail.as_view(), name = 'upload_fail'),
    path('api_link/', views.api_link, name = 'api_link'),
    path('confirm_all_delete/', ConfirmAllDelete.as_view(), name = 'confirm_all_delete')
]

handler404 = 'managing_photos.views.error_404_view' 