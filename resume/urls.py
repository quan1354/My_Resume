"""
URL configuration for resume project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.about),
    # path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('journal/', views.journal, name='journal'),
    path('project/', views.project, name='project'),
    path('skill/', views.skill, name='skill'),

    path('get_notes/', views.get_notes, name='get_notes'),
    path('save_note/', views.save_note, name='save_note'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('delete_note/', views.delete_note, name='delete_note'),
    path('edit_note/', views.edit_note, name='edit_note'),

]
