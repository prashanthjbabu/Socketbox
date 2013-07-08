from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^send/$','sock_test'),
#    url(r'^socketbox/',include('socketbox.urls')),
    url(r'/',include('socketbox.urls')),
	url(r'^$', 'sockserv.views.index', {}, name='home_url_name'),
    url(r'^features/$', 'sockserv.views.features', {}, name='home_url_name'),
    url(r'^tutorials/$', 'sockserv.views.tutorials', {}, name='home_url_name'),
    url(r'^contact/$', 'sockserv.views.contact', {}, name='home_url_name'),
    url(r'^about/$', 'sockserv.views.about', {}, name='home_url_name'),
    url(r'^js/socketbox-1.0.js$', 'sockserv.views.js', {}, name='home_url_name'),
    # Examples:
    # url(r'^$', 'sockserv.views.home', name='home'),
    # url(r'^sockserv/', include('sockserv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
