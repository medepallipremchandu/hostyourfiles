from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
 
urlpatterns = [
         path('', views.index, name ='index'),
         path('add_term/', views.add_term, name='add_term'),
         path('blog/<uuid:public_url>/', views.blog_detail, name='blog_detail'),
         path("contact/", views.contact, name="contact"),
         path('success/', views.success, name='success'),
         path('blogs/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
         path('blogs/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
         path('upload_pdf', views.upload_pdf, name='upload_pdf'),
         path('pdf_list', views.pdf_list, name='pdf_list'),    
]