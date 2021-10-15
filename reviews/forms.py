from django import forms
from django.forms import widgets
from .models import Review

class CreateReviewForm(forms.ModelForm):
    accuracy = forms.IntegerField(max_value=5, min_value=1)
    communication = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )
        widgets = {
            "review": forms.TextInput(attrs={"placeholder": "리뷰를 남겨주세요"}),
            "accuracy": forms.NumberInput(attrs={"placeholder": "0~5"}),
            "communication": forms.NumberInput(attrs={"placeholder": "0~5"}),
            "cleanliness": forms.NumberInput(attrs={"placeholder": "0~5"}),
            "location": forms.NumberInput(attrs={"placeholder": "0~5"}),
            "check_in": forms.NumberInput(attrs={"placeholder": "0~5"}),
            "value": forms.NumberInput(attrs={"placeholder": "0~5"}),
        }

    def save(self):
        review = super().save(commit=False)
        return review