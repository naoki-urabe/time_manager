from activity_record.views.activity_detail_view import ActivityDetailView
from activity_record.views.activity_log_view import ActivityLogView
from activity_record.views.activity_record_view import ActivityRecordView
from activity_record.views.edit_log_view import EditLogView
from activity_record.views.register_gear_view import RegisterGearView
from activity_record.views.register_subject_view import RegisterSubjectView
from activity_record.views.review_list_view import ReviewListView
from activity_record.views.subject_log_view import SubjectLogView
from activity_record.views.study_log_view import StudyLogView
from activity_record.views.kuji_log_view import KujiLogView

activity_record = ActivityRecordView.as_view()
activity_log = ActivityLogView.as_view()
activity_detail = ActivityDetailView.as_view()
subject_log = SubjectLogView.as_view()
register_subject = RegisterSubjectView.as_view()
register_gear = RegisterGearView.as_view()
review_list = ReviewListView.as_view()
edit_log = EditLogView.as_view()
study_log = StudyLogView.as_view()
kuji_log = KujiLogView.as_view()