from django import forms
from .models import ActiveRecord
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
ActiveRecordFormSet = forms.modelformset_factory(
    ActiveRecord,form=ActiveRecordCreateForm, extra=10,max_num=100, can_delete=True,localized_fields='__all__'
)