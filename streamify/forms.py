from django import forms
from .models import *


# class CreateQuestionForm(forms.ModelForm):

#     description = "Effettua il login"

#     def clean(self):

#         if (len(self.cleaned_data["question_text"]) < 5):
#             self.add_error("question_text", "Error: question text must be at least 5 characters long")

#         return self.cleaned_data


#     class Meta:
#         model = Question
#         fields = "__all__"
#         widgets = {
#         'pub_date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
#         }