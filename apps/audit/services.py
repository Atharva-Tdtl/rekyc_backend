from .models import AuditLog
def log_action(action, entity, actor=None, before=None, after=None, request=None):
    return AuditLog.objects.create(action=action, entity_type=entity.__class__.__name__, entity_id=str(getattr(entity,'id','')), actor=actor, before=before or {}, after=after or {}, ip_address=(request.META.get('REMOTE_ADDR') if request else None))
