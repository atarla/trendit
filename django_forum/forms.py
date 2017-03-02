from django import forms
from django.forms import Textarea

from django_forum.models import Topic, Post, ProfaneWord

from trenditapp.settings import *

class TopicForm(forms.ModelForm):

    title = forms.CharField(max_length=60, required=True)

    class Meta():
        model = Topic
        exclude = ('creator','updated', 'created', 'closed', 'forum',)


class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=60, required=False)

    class Meta():
        model = Post
        exclude = ('creator', 'updated', 'created','topic', 'user_ip',)
        widgets={'body':Textarea(attrs={'cols':150, 'rows': 40}),}
    def clean_body(self):
        body = self.cleaned_data["body"]

        if DJANGO_SIMPLE_FORUM_FILTER_PROFANE_WORDS:
            profane_words = ProfaneWord.objects.all() 
            bad_words = [w for w in profane_words if w.word in body.lower()]

            if bad_words:
                raise forms.ValidationError("Bad words like '%s' are not allowed in posts." % (reduce(lambda x,y: "%s,%s" % (x,y),bad_words)))
        
        return body
