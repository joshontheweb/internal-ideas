# ideas views.py
from django.shortcuts import render_to_response
from models import Idea
from voting.models import Vote

# def list(request):
#     idea_tuples = Vote.objects.get_top(Idea, limit=3)
#     return render_to_response('idea/idea_list.html', locals(), context_instance=RequestContext(request))