from django.urls import path
from . import views
from .views import signup_view, login_view, logout_view, check_email_view


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('check-email/', check_email_view, name='check_email'),
    path('kakao_login', views.kakao_login, name='kakao_login'),
    path('kakao/callback', views.kakao_callback, name='kakao_callback'),
    path('logout/', views.logout_view, name='logout'),
    path('kakao/logout_done/', views.kakao_logout_done, name='kakao_logout_done/'),
    path('naver_login/', views.naver_login, name='naver_login'),
    path('naver/callback/', views.naver_callback, name='naver_callback'),

]