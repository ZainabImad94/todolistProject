from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',  'description', 'done')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal row'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.fields['description'].required = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            'done'
        )
