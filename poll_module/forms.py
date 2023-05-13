from django import forms


class PollCreateForm(forms.Form):
    question = forms.CharField(widget=forms.TextInput(attrs={"id": "question-title" }), label="سوال نظرسنجی")
    option_list = forms.JSONField()
