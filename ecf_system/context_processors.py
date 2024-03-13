from dashboard.models import Notification


def notifications(request):
    if not request.user.is_authenticated:
        return {}
    
    return {
        "notifications": Notification.objects.filter(user=request.user).order_by("-created_at")[0:5],
        "unread_notifications": True if Notification.objects.filter(user=request.user, viewed=False) else False
    }
