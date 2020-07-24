from activity_record.models.active_record import ActiveRecord

def load_logs(activity_type):
    logs = ActiveRecord.objects.filter(active_type=activity_type).order_by('-today')
    return logs
def load_log_info(log):
    log_exists = log.is_active if log != None else False
    log_info = {
        "id": -1,
        "name": "",
        "memo": "",
        "status": "開始",
        "is_exists": False
    }
    print(log_info)
    print("----------------------")
    if log_exists:
        log_info["id"] = log.id
        log_info["name"] = log.task
        log_info["memo"] = log.memo
        log_info["status"] = "終了"
        log_info["is_exists"] = True
    return log_info