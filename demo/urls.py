from django.conf.urls import patterns, include, url
from demo import views

urlpatterns = patterns ('',
	url(r'^$', views.main, name = 'main'),
	url(r'^login/$', views.login_user, name='login'),
	url(r'^(?P<user>\w+)/$', views.index, name='home'),
	url(r'^(?P<user>\w+)/logout/$', views.logout_user, name='logout'),
	url(r'^(?P<user>\w+)/post/add/$', views.add_post, name='post'),
	url(r'^post/(?P<post_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<user>\w+)/post/(?P<post_id>\d+)/comment/add/$', views.add_comment, name='comment'),
	url(r'^user/(?P<user>\w+)$', views.user, name='user'),
)
