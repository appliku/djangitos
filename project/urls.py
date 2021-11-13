from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('demo.urls')),
    path('accounts/', include('allauth.urls')),
    path('sns/', include('ses_sns.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
