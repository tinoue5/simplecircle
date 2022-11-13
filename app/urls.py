from django.urls import path
from . import views

app_name='app'
urlpatterns = [
    path('circle_board', views.circle_board, name='circle_board'),
    path('circle_switch/<int:to_circle>', views.circle_switch, name='circle_switch'),
    path('create_new_circle', views.create_new_circle, name='create_new_circle'),
    path('make_invite_url', views.make_invite_url, name='make_invite_url'),
    path('join_from_invite/<str:key>', views.join_from_invite, name='join_from_invite'),

    path('portal',views.portal, name='portal'),
    path('bridge',views.bridge, name='bridge'),
    path('trytoken',views.trytoken, name='trytoken'),

    path('empw_login',views.empw_login, name='empw_login'),
    path('logout_firebase',views.logout_firebase, name='logout_firebase'),

    # 不要っぽい
    path('register', views.register, name='register'),
    path('tokentest',views.tokentest, name='tokentest'),
    path('fbtest',views.fbtest, name='fbtest'),
    path('fbtest2',views.fbtest2, name='fbtest2'),

]
