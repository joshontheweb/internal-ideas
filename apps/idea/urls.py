# ideas urls.py
from django.conf.urls.defaults import *
from models import Idea
# from views import list
from tagging.views import tagged_object_list
from voting.views import vote_on_object
from voting.models import Vote


info_dict = {
    'queryset': Idea.objects.all(),
    # 'queryset': Vote.objects.get_top(Idea, limit=3),
    'template_object_name': 'idea',
}

# generic views
urlpatterns = patterns('django.views.generic',
    (r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, 
        dict(
            model=Idea, 
            template_object_name='idea',
            allow_xmlhttprequest=True, 
            post_vote_redirect='/',
        ),
    ),

    (r'^(?P<object_id>\d+)/$', 'list_detail.object_detail', info_dict, 'idea_detail'),
    (r'^$', 'list_detail.object_list', info_dict, 'idea_detail'),

)

urlpatterns += patterns('',

    # (r'^$', 'list', None, 'idea_list'),


    url(r'^tag/(?P<tag>[^/]+)/$',
        tagged_object_list,
        dict(queryset_or_model=Idea, paginate_by=20, allow_empty=True,
            template_object_name='idea'),
            name='idea_tag_list'),
)

