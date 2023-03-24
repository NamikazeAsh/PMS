from django.forms import ModelForm, DateInput
from calendarapp.models import Event
from django import forms
from django.contrib.auth.models import User


# class EventForm(ModelForm):
#     members = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Professor','Sr Intern','Intern']))
#     class Meta:
#         model = Event
#         fields = ["title", "description", "start_time", "end_time"]
#         # datetime-local is a HTML5 input type
#         widgets = {
#             "title": forms.TextInput(
#                 attrs={"class": "form-control", "placeholder": "Enter event title"}
#             ),
            
#             "description": forms.Textarea(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Enter event description",
#                 }
#             ),
#             "start_time": DateInput(
#                 attrs={"type": "datetime-local", "class": "form-control"},
#                 format="%Y-%m-%dT%H:%M",
#             ),
#             "end_time": DateInput(
#                 attrs={"type": "datetime-local", "class": "form-control"},
#                 format="%Y-%m-%dT%H:%M",
#             ),
#         }
#         exclude = ["user"]

#     def __init__(self, *args, **kwargs):
#         super(EventForm, self).__init__(*args, **kwargs)
#         # input_formats to parse HTML5 datetime-local input to datetime field
#         self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
#         self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


# class AddMemberForm(forms.ModelForm):
#     user = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Professor','Sr Intern','Intern']))
#     class Meta:
#         model = EventMember
#         fields = ["user"]

class EventForm(ModelForm):
    user=forms.ModelChoiceField(queryset=User.objects.all())
    title = forms.CharField(widget=forms.TextInput)
    members = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Professor','Sr Intern','Intern']))
    description = forms.CharField(widget=forms.Textarea)
    start_time=forms.DateField(widget=DateInput(
        attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ))
    end_time = forms.DateField(widget=DateInput(
        attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ))
    

    class Meta:
        model = Event
        fields = ["title", "members","description", "start_time", "end_time"]
        exclude = ["user"]


    def save(self, commit=True):
        
        Event = super(EventForm, self).save(commit=False)
        evemembers = self.cleaned_data['members']
        for members in evemembers:
            Event.members.add((members))

        if commit:
            Event.save()

        return Event


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Enter event title'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter event description'
        self.fields['members'].widget.attrs['class'] = 'form-control'
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))