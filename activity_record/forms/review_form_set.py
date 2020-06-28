from django import forms
from activity_record.models import ActiveRecord
from activity_record.models import Subject
from activity_record.models import Gear
from activity_record.models import Review

class ReviewFormSet(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('subject_id','summary','is_online','version')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        subject_all = Subject.objects.all()
        CHOICE = [
            ('','科目を選択してください')
            ]
        for subject in subject_all:
            CHOICE.append((subject.subject_id,subject.subject))
        self.fields['subject_id'] = forms.ChoiceField(
            required=True,
            choices=CHOICE,
            widget=forms.Select
        )
        CHOICE = [
            ('','科目を選択してください'),
            ('online','オンライン'),
            ('offline','オフライン')
            ]
        self.fields['is_online'] = forms.ChoiceField(
            required=True,
            choices=CHOICE,
            widget=forms.Select
        )
        #self.queryset = self.queryset.order_by('gear')
