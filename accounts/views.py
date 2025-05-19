from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile
from notifications.models import Notification

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        latest_project=Project.objects.all()[:5]
        latest_task=Task.objects.all()[:5]
        latest_members=Profile.objects.all()[:8]
        latest_notifications=Notification.objects.for_user(request.user)[:5]
        context={
            'latest_task':latest_task,
            'latest_project':latest_project,
            'latest_members':latest_members,
            'latest_notifications':latest_notifications,
            'notification_count':latest_notifications.count(),
        }
        return render(request, 'accounts/dashboard.html',context)
