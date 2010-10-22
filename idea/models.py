from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from django.forms import ModelForm
# from views import idea_desc_form

class Idea(models.Model):
    author = models.ForeignKey(User, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    tags = TagField()
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return('idea_detail', [str(self.id)])
    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
                
class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        exclude = ('author')

