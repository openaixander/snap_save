from django.urls import path


from . import views

app_name = 'accounts'


urlpatterns = [
    path('register_photographer/', views.register_photographer, name='register_photographer'),
    path('register_client/', views.register_client, name='register_client'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
    
    # activation of accounts
    path('activate/<uidb64>/<token>/<account_type>/', views.activate, name='activate'),
    # reset password for a user
    path('reset_password_validate/<uidb64>/<token>/<account_type>/', views.reset_password_validate, name='reset_password_validate'),
]