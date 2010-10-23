# ideas views.py
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from models import Idea, IdeaForm
from voting.models import Vote
import operator

def idea_list(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
    idea_list = Idea.objects.all()
    for idea in idea_list:
        score_dict = Vote.objects.get_score(idea)
        idea.score = score_dict['score']
        idea.votes = score_dict['num_votes']
    score = Vote.objects.get_score(Idea.objects.get(pk=1))
    realscore = score['score']
    idea_list = list(idea_list)
    idea_list.sort(key=lambda x: x.score, reverse=True)
    # limit = len(idea_list)
    # idea_list = list(Vote.objects.get_top(Idea, limit=20))
    # scores = Vote.objects.get_scores_in_bulk(idea_list)
    # score_dict = Vote.objects.get_scores_in_bulk(idea_list)    
    # idea_dict.sort(key=idea_list.get_score())
    # sorted_list = sorted(idea_list, key=lambda x: get_score(x) )
    # assert False, idea_list
    return render_to_response('idea/idea_list.html', locals(), context_instance=RequestContext(request))

from django.views.decorators.csrf import csrf_protect
@csrf_protect
def idea_detail(request, object_id):
    idea = Idea.objects.get(pk=object_id)
    # for idea in idea_list:
    score_dict = Vote.objects.get_score(idea)
    idea.score = score_dict['score']
    idea.votes = score_dict['num_votes']
    score = Vote.objects.get_score(Idea.objects.get(pk=1))
    realscore = score['score']
    # idea_list = list(idea_list)
    # idea_list.sort(key=lambda x: x.score, reverse=True)
    # limit = len(idea_list)
    # idea_list = list(Vote.objects.get_top(Idea, limit=20))
    # scores = Vote.objects.get_scores_in_bulk(idea_list)
    # score_dict = Vote.objects.get_scores_in_bulk(idea_list)    
    # idea_dict.sort(key=idea_list.get_score())
    # sorted_list = sorted(idea_list, key=lambda x: get_score(x) )
    # assert False, idea
    return render_to_response('idea/idea_detail.html', locals(), context_instance=RequestContext(request))
    
def idea_submit(request):
    if request.method == "POST":
        if request.POST.has_key("part1"):
                idea_form = IdeaForm(initial={'description': request.POST['description']})
        else:
            idea_form = IdeaForm(request.POST)
            if idea_form.is_valid():
                title = idea_form.cleaned_data["title"]
                description = idea_form.cleaned_data["description"]
                tags = idea_form.cleaned_data["tags"]
                saveObj = idea_form.save(commit=False)
                saveObj.author = request.user
                saveObj.save()
                return HttpResponseRedirect("/")
    else:
        idea_form = IdeaForm()
    return render_to_response('idea/idea_submit.html', locals(), context_instance=RequestContext(request))
    
