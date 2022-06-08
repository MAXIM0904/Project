
def _update_status(instance_feedback):
    if instance_feedback.status == 'archive':
        instance_feedback.status = 'received'
    else:
        instance_feedback.status = 'archive'
    instance_feedback.save()
