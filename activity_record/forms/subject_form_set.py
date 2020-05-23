from django import forms
from activity_record.models import ActiveRecord
from activity_record.models import Subject
from activity_record.models import Gear
from activity_record.models import Review

class SubjectFormSet(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('subject_id','subject')
