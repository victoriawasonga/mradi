from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

STATUS_CHOICES = [
    ('todo', 'Todo'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('on_hold', 'On Hold'),
]
PRIORITY_CHOICES=[
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]
class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcoming(self):
        return self.filter(due_date__gt=timezone.now().date(), status__in=['todo', 'in_progress'])


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    def all(self):
        return self.get_queryset().active().upcoming()

    
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status= models.CharField(max_length=50, choices=STATUS_CHOICES, default='todo')
    priority=models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    # budget = models.DecimalField(max_digits=10, decimal_places=2)

    objects = ProjectManager()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['-created_at']

    def days_until_due(self):
        if self.due_date:
            current_date = timezone.now().date()
            return (self.due_date - current_date).days
        return None
    @property
    def progress(self):
        progress_dict={
            'todo':0,
            'in_progress':50,
            'completed':100,
            'on_hold':25
        }
        return progress_dict.get(self.status, 0)
    
    @property
    def status_color(self):
        status_value=self.progress
        if status_value== 100:
            color="success"
        elif status_value==50:
            color="primary"
        else:
            color="warning"
        return color

    def priority_color(self):
        if self.priority=="low":
            color="success"
        elif self.priority=="medium":
            color="warning"
        else:
            color="danger"
        return color