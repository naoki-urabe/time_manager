from django import forms
from .models import ActiveRecord
class ActiveRecordCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['end_time'].required = False
        self.fields['period'].required = False
        self.fields['active_type'].required = False
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ActiveRecord
        fields = '__all__'

ActiveRecordFormSet = forms.modelformset_factory(
    ActiveRecord,form=ActiveRecordCreateForm, extra=10,max_num=100
)