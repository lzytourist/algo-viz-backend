from django import forms
from tinymce.widgets import TinyMCE

from .models import AlgorithmCategory, Algorithm


class AlgorithmCategoryForm(forms.ModelForm):
    class Meta:
        model = AlgorithmCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            self.fields['parent'].queryset = AlgorithmCategory.objects.exclude(pk=instance.pk).all()


class AlgorithmForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Algorithm
        fields = '__all__'
