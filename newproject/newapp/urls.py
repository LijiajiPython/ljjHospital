from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path(r'^$',views.home),
    re_path(r'^home/$', views.home),
    re_path(r'^login/$', views.login),
    re_path(r'^register/$', views.register),
    re_path(r'^logout/$', views.logout),
    re_path(r'^back/$', views.back),
    re_path(r'^news/$', views.news),
    re_path(r'^fords/(\d+)/$', views.fords),
    re_path(r'^hospitals/(\d+)/$', views.hospitals),
    re_path(r'^rooms/(\d+)/$', views.rooms),
    re_path(r'^forillness/(\d+)/$', views.forillness),
    re_path(r'^doctors/(\d+)/$', views.doctors),
    re_path(r'^messagesubmit/(\d+)/$', views.messagesubmit),
    re_path(r'^success/(\d+)/(\d+)$', views.success),
    re_path(r'^userhome/(\d+)/$', views.userhome),
    re_path(r'^dochome/(\d+)/$', views.dochome),
    re_path(r'^onenews/(\d+)/$', views.onenews),
    re_path(r'^userchange/(\d+)/$', views.userchange),
    re_path(r'^page1/$', views.page1),
    re_path(r'^pay/$', views.pay),
    re_path(r'^search/$', views.search),
	# url(r'^page2/', views.page2),




]