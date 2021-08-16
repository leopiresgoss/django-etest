from django.contrib import admin
from django.urls import path, include

from .views import home, login_view, logout_view
 

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('test/', include('participants.urls',namespace='participants')),
    path('tests/', include('tests.urls', namespace='tests')),
]
