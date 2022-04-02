from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    # path('auth/demo/', view=views.auth_demo, name='auth_demo'),

    path('auth/portail/', view=views.auth_portal, name='auth_portal'),
    path('auth/connexion/', view=views.auth_login, name='auth_login'),
    path('auth/inscription/', view=views.auth_signup, name='auth_signup'),
]
