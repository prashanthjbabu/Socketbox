from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('socketbox.views',
	url(r'^send/$','sock_test'),
	url(r'^user/add/$','add_user'),
	url(r'^user/login/$','login_user'),
	url(r'^create/app/$','create_app'),
	url(r'^show/apps/$','show_apps'),
	url(r'^delete/app/$','delete_app'),
	url(r'^rename/app/$','rename_app'),
	url(r'^app/secret/$','get_app_secret'),
	url(r'^account/activate/(?P<email>\S+)/(?P<actcode>\S+)/$','activate_account'),
	
	url(r'^account/reset/(?P<email>\S+)/(?P<resetcode>\S+)/$','reset_account'),

	url(r'^new/password/$','new_password'),
	url(r'^forgot/password/$','forgot_password'),
	url(r'^reset/password/$','reset_password'),

	url(r'^login/$','login'),
    # Examples:
    # url(r'^$', 'sockserv.views.home', name='home'),
    # url(r'^sockserv/', include('sockserv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
