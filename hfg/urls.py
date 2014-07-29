from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from app.admin import manager_admin, provider_admin
from ajax_select import urls as ajax_select_urls
#admin.autodiscover()
from app.views import CustomBlogIndex, CustomEntryDetail

from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    url(r'', include('app.urls')),
    url(r'account/', include('account.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^blog/$', CustomBlogIndex.as_view(), name="blog"),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        CustomEntryDetail.as_view(),
        name='entry_detail'),
    url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^provider/', include(provider_admin.urls)),
    url(r'^manager/lookups/', include(ajax_select_urls)),
    url(r'^manager/', include(manager_admin.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^payments/", include("payments.urls")),

)


from django.conf import settings
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
    )
