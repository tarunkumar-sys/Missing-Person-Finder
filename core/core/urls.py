from django.contrib import admin
from django.urls import path
from missingperson.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('detect/', detect, name='detect'),
    path('surveillance/', surveillance, name='surveillance'),
    path('register/', register, name='register'),
    path('missing/', missing, name='missing'),
    path('delete/<int:person_id>/', delete_person, name='delete_person'),
    path('update/<int:person_id>/', update_person, name='update_person'),
    path('admin/', admin.site.urls),

    path('cameras/', camera_list, name='camera_list'),
    path('cameras/add/', add_camera, name='add_camera'),
    path('cameras/edit/<int:camera_id>/', edit_camera, name='edit_camera'),
    path('cameras/delete/<int:camera_id>/', delete_camera, name='delete_camera'),
    path('multi-camera/start/', start_multi_camera_detection, name='start_multi_camera'),
    path('multi-camera/stop/', stop_multi_camera_detection, name='stop_multi_camera'),
    
    # Camera preview URLs
    path('camera-preview/<int:camera_id>/', camera_preview, name='camera_preview'),
    path('all-cameras-preview/', all_cameras_preview, name='all_cameras_preview'),
    path('detection-status/', detection_status, name='detection_status'),
    
    # Test URLs
    path('test-detection/', test_detection, name='test_detection'),
    path('check-cameras/', check_cameras, name='check_cameras'),
    path('test-face-detection/', test_face_detection, name='test_face_detection'),
    path('reset-email-flags/', reset_email_flags, name='reset_email_flags'),
    path('debug-detection/', debug_detection, name='debug_detection'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)