from django import forms
from activity_record.models import ActiveRecord
from activity_record.models import Subject
from activity_record.models import Gear
from activity_record.models import Review
from activity_record.forms.active_record_create_form import ActiveRecordCreateForm
from activity_record.forms.active_record_form import ActiveRecordForm
from activity_record.forms.gear_form_set import GearFormSet
from activity_record.forms.review_form_set import ReviewFormSet
from activity_record.forms.subject_form_set import SubjectFormSet

ActiveRecordFormSet = forms.modelformset_factory(
    ActiveRecord,form=ActiveRecordCreateForm, extra=10,max_num=100, can_delete=True,localized_fields='__all__'
)

SubjectFormSet = forms.modelformset_factory(
    Subject,form=SubjectFormSet, extra=10,max_num=100, can_delete=True,localized_fields='__all__'
)

GearFormSet = forms.modelformset_factory(
    Gear,form=GearFormSet, extra=10,max_num=100, can_delete=True,localized_fields='__all__', can_order=True
)

ReviewFormSet = forms.modelformset_factory(
    Review,form=ReviewFormSet, extra=10,max_num=10, can_delete=True,localized_fields='__all__', can_order=True
)