from django import  forms

from news_module.models import News


class NewsAddForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["image", "title", "content"]