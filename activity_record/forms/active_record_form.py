from django import forms
from activity_record.models import ActiveRecord
from activity_record.models import Subject
from activity_record.models import Gear
from activity_record.models import Review

class ActiveRecordForm(forms.ModelForm):
    class Meta:
        model = ActiveRecord
        fields = ('active_type','task','memo')
    active_exists = forms.BooleanField(required=True,widget=forms.HiddenInput)
    active_id = forms.IntegerField(required=True,widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['active_type'].widget = forms.HiddenInput()
        self.fields['task'].widget = forms.HiddenInput()
