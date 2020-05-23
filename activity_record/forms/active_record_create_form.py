from django import forms
from activity_record.models import ActiveRecord
from activity_record.models import Subject
from activity_record.models import Gear
from activity_record.models import Review

class ActiveRecordCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['begin_time'].required = False
        self.fields['end_time'].required = False
        self.fields['memo'].required = False
        self.fields['today'].required = False
        self.fields['active_type'].required = False
        self.fields['is_active'].widget = forms.HiddenInput()
        #self.fields['is_active'].initial = False
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        CHOICE = [
            ('','活動タイプを選択してください'),
            ('active','活動時間'),
            ('task','タスク'),
            ('schedule','スケジュール')]
        self.fields['active_type'] = forms.ChoiceField(
            required=True,
            choices=CHOICE,
            widget=forms.Select
        )
    class Meta:
        model = ActiveRecord
        fields = ('task','begin_time','end_time','memo','today','active_type','is_active')
