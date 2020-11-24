from django import forms
from django.forms import SelectDateWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Row, Column, Div, MultiWidgetField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Profile
from django.core.validators import validate_email

# Create your views here.


def clean_user_info(value):
    if not value.isalpha():
        raise ValidationError('Only characters are allowed !')
    else:
        return value


alpha = RegexValidator(r'^[0-9a-zA-Z_\-+.@]*$', 'Only number, character & (-,_) are allowed !')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'example@example.com'}
        ),
        required=True,
        validators=[validate_email]
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=40,
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': 'True'}
        ),
        validators=[clean_user_info]
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=40,
        min_length=4,
        required=True,
        validators=[clean_user_info]
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        min_length=4,
        required=True,
        validators=[alpha]
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email is already in use! Try another email.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'card pt-4 mt-5'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Sign Up',
                     Row(
                         Column('first_name', css_class='form-group col-md-6 mb-0'),
                         Column('last_name', css_class='form-group col-md-6 mb-0')
                     ),
                     'username',
                     'email',
                     Row(
                         Column('password1', css_class='form-group col-md-6 mb-0'),
                         Column('password2', css_class='form-group col-md-6 mb-0')
                     ),
                     Submit('submit', 'Create New Account', css_class='btn-danger btn-block '),
                     css_class='card-body'),
            Div(HTML("""Already have an account? <a href="{% url 'login' %}">Log in</a>"""),
                css_class='card-footer text-center')
        )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'example@example.com'}
        ),
        required=True,
        validators=[validate_email]
    )
    username = forms.CharField(
        label='Username',
        max_length=40,
        required=True,
        validators=[alpha]
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=40,
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': 'True'}
        ),
        validators=[clean_user_info]
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=40,
        min_length=4,
        required=True,
        validators=[clean_user_info]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email is already in use! Try another email.')
        return email


class ProfileUpdateForm(forms.ModelForm):
    years = [x for x in range(1960, 2020)]
    numeric = RegexValidator(r'^[0-9+]*$', 'Invalid Phone Number ! only numbers are allowed')
    phone = forms.CharField(validators=[numeric], min_length=13, required=False)
    profile_pic = forms.ImageField(max_length=200, required=False)
    birth_date = forms.DateField(widget=SelectDateWidget(years=years), required=False)

    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'phone', 'birth_date', 'url_facebook', 'url_twitter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'profile_pic',
            'bio',
            MultiWidgetField('birth_date', attrs=({'style': 'width: 32%; display: inline-block;', 'class': 'mr-1','data-date-format': 'dd/mm/yyyy'})),
            'phone',
            'url_facebook',
            'url_twitter',
            Submit('submit', 'Save Changes', css_class='btn-info btn-block ')
        )
