from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,InvestmentProject

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'address', 'country', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders to each field
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'country': 'Country',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

# class InvestmentProjectForm(forms.ModelForm):
#     class Meta:
#         model = InvestmentProject
#         fields = ["project_name", "total_investment", "min_roi", "max_roi", "project_description", "image1", "image2", "image3", "is_active"]


class InvestmentProjectForm(forms.ModelForm):
    class Meta:
        model = InvestmentProject
        fields = ["project_name", "total_investment", "min_roi", "max_roi", "project_description", "image1", "image2", "image3", "is_active"]
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control  border-end-1',
                'placeholder': 'Enter Project Name'
            }),
            'total_investment': forms.NumberInput(attrs={
                'class': 'form-control border-start-1 border-end-1',
                'placeholder': 'Total Investment'
            }),
            'min_roi': forms.NumberInput(attrs={
                'class': 'form-control border-start-1 border-end-1',
                'placeholder': 'Min ROI (%)'
            }),
            'max_roi': forms.NumberInput(attrs={
                'class': 'form-control border-start-1 border-end-1',
                'placeholder': 'Max ROI (%)'
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'form-control rounded p-3 shadow-sm',
                'placeholder': 'Describe your project...',
                'rows': 4
            }),
            'image1': forms.FileInput(attrs={'class': 'form-control shadow-sm'}),
            'image2': forms.FileInput(attrs={'class': 'form-control shadow-sm'}),
            'image3': forms.FileInput(attrs={'class': 'form-control shadow-sm'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'project_name': 'Project Name',
            'total_investment': 'Total Investment',
            'min_roi': 'Minimum ROI (%)',
            'max_roi': 'Maximum ROI (%)',
            'project_description': 'Project Description',
            'image1': 'Image 1',
            'image2': 'Image 2',
            'image3': 'Image 3',
            'is_active': 'Is Active?',
        }
        help_texts = {
            'min_roi': 'Enter the minimum expected return on investment in percentage.',
            'max_roi': 'Enter the maximum expected return on investment in percentage.',
            'image1': 'Upload an image for the project (optional).',
            'image2': 'Upload an additional image (optional).',
            'image3': 'Upload another image (optional).',
        }

    def clean(self):
        cleaned_data = super().clean()
        min_roi = cleaned_data.get('min_roi')
        max_roi = cleaned_data.get('max_roi')

        if min_roi and max_roi and min_roi > max_roi:
            raise forms.ValidationError("Minimum ROI cannot be greater than Maximum ROI.")

        return cleaned_data




from django import forms
from .models import Transaction, AssignedProject

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['project', 'amount', 'transaction_type', 'return_period','narration', 'receipt']
        widgets = {
            #  'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction amount'
            }),
             'narration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'narration'
            }),
            
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        # Filter projects based on assigned projects for the user
        if self.user:
            assigned_projects = AssignedProject.objects.filter(user=self.user).values_list('project', flat=True)
            self.fields['project'].queryset = self.fields['project'].queryset.filter(id__in=assigned_projects)
            
from django import forms
from .models import AssignedProject

class AssignProjectForm(forms.ModelForm):
    class Meta:
        model = AssignedProject
        fields = ['user', 'project', 'rate_of_interest', 'return_period']  # Include relevant fields
        widgets = {
            'rate_of_interest': forms.NumberInput(attrs={'placeholder': 'Enter interest rate'}),
            'return_period': forms.Select(attrs={'class': 'form-select'}),
        }
      
      
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'address', 'country']

class PasswordEditForm(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']              
        
        
from django import forms
from .models import Transaction, AssignedProject


from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        validators=[validate_password]
    )
    reenter_password = forms.CharField(
        label="Re-enter New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        reenter_password = cleaned_data.get("reenter_password")

        if new_password and reenter_password and new_password != reenter_password:
            raise ValidationError("New passwords don't match!")
        return cleaned_data            
    
    
from django import forms
from .models import Transaction, CustomUser, InvestmentProject

class StaffTransactionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label="Select User"
    )
    project = forms.ModelChoiceField(
        queryset=InvestmentProject.objects.filter(is_active=True),
        label="Select Project"
    )
    transaction_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Transaction Date"
    )

    class Meta:
        model = Transaction
        fields = ['user', 'project', 'amount', 'transaction_type', 
                 'narration', 'receipt', 'transaction_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No need for user-specific project filtering anymore
        
        
# documents/forms.py
from django import forms
from .models import UserDocument

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UserDocument
        fields = ['document_type', 'file', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }            