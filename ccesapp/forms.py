from django.contrib.auth.hashers import make_password

from django import forms
from .models import Citizen, Province, District, Sector, Cell, Village, Complaint, Agent, PublicService, Feedback, AgencyFeedback

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CitizenForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = ['nid', 'nationality', 'dob', 'marital_status', 
                  'agent_reference', 'province', 'district', 'sector', 'cell', 'village', 'street']

    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label="Select Province")
    district = forms.ModelChoiceField(queryset=District.objects.none(), required=False)
    sector = forms.ModelChoiceField(queryset=Sector.objects.none(), required=False)
    cell = forms.ModelChoiceField(queryset=Cell.objects.none(), required=False)
    village = forms.ModelChoiceField(queryset=Village.objects.none(), required=False)

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['name']

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'province']

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['name', 'district']

class CellForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = ['name', 'sector']

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ['name', 'cell']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'agent_reference']

class AgentSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    agent_reference = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'agent_reference')
    
    def clean_agent_reference(self):
        reference = self.cleaned_data.get('agent_reference')
        if Agent.objects.filter(agent_reference=reference).exists():
            raise forms.ValidationError("This agent reference number is already in use.")
        return reference

class CitizenRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = Citizen
        fields = ['nid', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Hash the password before saving
        cleaned_data['password'] = make_password(password)
        return cleaned_data

class CitizenLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CitizenEditForm(forms.ModelForm):
    class Meta:
        model = Citizen
        exclude = ('user', 'password')  # <-- explicitly exclude 'password'

    def __init__(self, *args, **kwargs):
        super(CitizenEditForm, self).__init__(*args, **kwargs)

        self.readonly_fields = [
            'nid', 'account_number', 'agent_reference', 'username',
            'nationality', 'gender', 'dob', 'marital_status',
            'name' 
        ]

        for field in self.readonly_fields:
            if field in self.fields:
                self.fields[field].disabled = True
                self.fields[field].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Re-assign readonly fields just in case
        if self.instance:
            for field in self.readonly_fields:
                setattr(instance, field, getattr(self.instance, field))

        if commit:
            instance.save()
        return instance
class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = PublicService
        fields = ['serviceType', 'definition']
        widgets = {
            'serviceType': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service Category'
            }),
            'definition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Details'
            }),
        }

class PublicServiceForm(forms.ModelForm):
    class Meta:
        model = PublicService
        fields = ['serviceType', 'definition']
        widgets = {
            'serviceType': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Category'}),
            'definition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Details'}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['publicService', 'complaintNature', 'details']
        widgets = {
            'complaintNature': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'publicService': forms.Select(attrs={'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter feedback here...'})
        }



class AgencyFeedbackForm(forms.ModelForm):
    class Meta:
        model = AgencyFeedback
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback...'}),
        }
