from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    unread_count = notifications.filter(is_read=False).count()

    return render(
        request,
        'notifications/notification_list.html',
        {
            'notifications': notifications,
            'unread_count': unread_count,
        }
    )


@login_required
def notification_detail(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    # Automatically mark the notification as read
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    return render(
        request,
        'notifications/notification_detail.html',
        {'notification': notification}
    )


@login_required
@require_POST
def mark_all_read(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    messages.success(
        request,
        'All notifications marked as read.'
    )

    return redirect('notification_list')


@login_required
def notification_delete(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    if request.method == 'POST':
        notification.delete()

        messages.success(
            request,
            'Notification deleted successfully.'
        )

        return redirect('notification_list')

    return render(
        request,
        'notifications/notification_confirm_delete.html',
        {'notification': notification}
    )


@login_required
@require_POST
def notification_delete_all_read(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=True
    ).delete()

    messages.success(
        request,
        'All read notifications have been deleted.'
    )

    return redirect('notification_list')
