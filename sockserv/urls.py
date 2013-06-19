from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^send/$','sock_test'),
    url(r'^socketbox/',include('socketbox.urls')),
	 url(r'^$', 'sockserv.views.index', {}, name='home_url_name'),
    # Examples:
    # url(r'^$', 'sockserv.views.home', name='home'),
    # url(r'^sockserv/', include('sockserv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
