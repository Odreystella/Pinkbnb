from django import forms


# 하나의 field만 사용하면 굳이 django form을 사용할 필요 없음
class CommentForm(forms.Form):

    message = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Write a message"}))
