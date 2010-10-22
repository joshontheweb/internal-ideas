from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ideas/', include('ideas.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^$', include('idea.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^ideas/', include('idea.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^$', 'idea.views.idea_list'),    
)

from idea.models import Idea, IdeaForm
home_dict = {
    'queryset': Idea.objects.all(),
    'template_name': 'home.html',
    'template_object_name': 'idea',
    'extra_context': { 'form': IdeaForm, 'this': 'THAT' },
}

# generic views
urlpatterns += patterns('django.views.generic',
    # (r'^$', 'list_detail.object_list', home_dict),    
)


from django.conf import settings

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$',
		'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
		'show_indexes': True}),
    )
