from django.forms import ModelForm,DateTimeInput
from django.contrib.admin import widgets
from django import forms
from cdf import models as cdf_models

from django import forms
from django.contrib.auth.models import User
from . import models
from ckeditor.fields import RichTextField

class ContractorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','email','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class ContractorForm(forms.ModelForm):
    class Meta:
        model=models.Contractor
        fields=['address','mobile','profile_pic']


class EngineerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','email','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class EngineerForm(forms.ModelForm):
    class Meta:
        model=models.Engineer
        fields=['address','mobile','profile_pic']

class AdminUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','email','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class AdminForm(forms.ModelForm):
    class Meta:
        model=models.Manager
        fields=['address','mobile','profile_pic']
class EngineerActiveForm(forms.Form):
    salary=forms.IntegerField();

class AdminRequestForm(forms.Form):
    # fields = []
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    project_cont=forms.ModelChoiceField(queryset=models.Contractor.objects.all(),empty_label="Contractor Name",to_field_name='id')
    project_eng=forms.ModelChoiceField(queryset=models.Engineer.objects.all(),empty_label="Engineer Name",to_field_name='id')


class AdminReportsForm(forms.Form):
    # fields = []
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    # cdfproject=forms.ModelChoiceField(queryset=models.CdfProjects.objects.all(),empty_label="Project Name",to_field_name='id')
    contrdetails=forms.ModelChoiceField(queryset=models.ContractorDetails.objects.all(),empty_label="Contractor Project",to_field_name='id')
    engdetails=forms.ModelChoiceField(queryset=models.EngineerDetails.objects.all(),empty_label="Engineer Project",to_field_name='id')


class DetailsContractorForm(forms.ModelForm):

    class Meta:
        model = models.ContractorDetails
        fields = ['contr_report']

class DetailsEngineerForm(forms.ModelForm):
    class Meta:
        model = models.EngineerDetails
        fields = ['engineer_remarks']
        widgets = {
        'engineer_remarks':RichTextField(config_name="default")
        }        

class DetailsProjectForm(forms.ModelForm):
    class Meta:
        model = models.ProjectManager
        fields = ['project_remark']
        widgets = {
        'project_remark':RichTextField(config_name="default")
        }                
class CdfProjectRequestForm(forms.Form):
    # fields = []
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    cdfproject=forms.ModelChoiceField(queryset=models.CdfProjects.objects.all(),empty_label="Project Name",to_field_name='id')
    # project_eng=forms.ModelChoiceField(queryset=models.Engineer.objects.all(),empty_label="Engineer Name",to_field_name='id')


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )


class SuggestionForm(forms.ModelForm):

	class Meta:
		model = cdf_models.Suggestions
		fields = ['suggestion','body','status','name','email']

class SecurityReportForm(forms.ModelForm):

	class Meta:
		model = cdf_models.Report
		fields = ['description','image','opinion','geom']

class SecurityEventForm(forms.ModelForm):

	class Meta:
		model = cdf_models.SecurityEvent
		fields = ['title','description','mdate','mtime','geom']

		widgets = {
			'mtime':DateTimeInput(attrs={'type':'time'}),
			'mdate':DateTimeInput(attrs={'type':'date'})

		}

class CommentForm(forms.ModelForm):

    class Meta:
        model = cdf_models.Comment
        fields = ('author', 'text',)

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = cdf_models.ContactUs
		fields = ['fullname','email','phonenumber','body']