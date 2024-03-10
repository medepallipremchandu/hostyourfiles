from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_view
from django.contrib.auth import views as auth
from django.contrib.auth import views as auth_views
from accounts.views import ResetPasswordView
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
 
    path('admin/', admin.site.urls),
 
    ##### user related path########################## 
    path('', include('accounts.urls')),
    path('index1/', accounts_view.index1, name='index1'),
    path('login/', accounts_view.Login, name ='login'),
    path('logout/', accounts_view.logout_view, name='logout'),
    path('register/', accounts_view.register, name ='register'),
    path('password-reset/', ResetPasswordView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'), 
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)