from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'done', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.fields['description'].required = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            'done',
            Submit('Submit', 'submit', css_class="btn-primary"),
        )
        # self.helper.add_input(Submit('Submit', 'submit', css_class="btn-primary"))
