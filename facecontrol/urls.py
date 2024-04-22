from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from facecontrol import settings
from .views import (login_view, register_view, logout_view, home_view, find_user_view, edit_profile_view)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('classify/', find_user_view, name='classify'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
