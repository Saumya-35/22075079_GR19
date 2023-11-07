
from django.urls import path,include
from . import views
import administrator

urlpatterns = [
   path("login_user",views.login_user,name="login"),
   path("administrator/",include("administrator.urls")),
   path("logout_user",views.logout_user,name="logout"),
   path('register_user', views.register_user, name="register"),
   path("profile",views.profile,name="profile"),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
]
