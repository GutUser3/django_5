from django.contrib import admin
from django.urls import path, include
from movies import views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('', include('users.urls'))
]

