from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # url(r'^$', views.welcome, name='welcome'),
    url(r'^$',views.index,name='home'),
    path('profile/',views.user_profile,name = 'profile'),
    path('rate/<int:id>/',views.Rate,name='rate'),
    path('comment/<int:id>/',views.comment,name='comment'),
    path('profileEdit/',views.profileEdit,name='profileEdit'),
    url(r'^singleproject/(\d+)',views.singleProject,name='singleproject'),
    path('newproject/',views.Newproject,name='newproject'),
    url(r'^search/',views.search_reslts,name = 'search_outcomes'),
    url(r'^logout/$',views.logoutRequest,name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'^api/profile/$',views.ProfileList.as_view()),
    # url(r'^api/projects/$',views.ProfileList.as_view()),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)