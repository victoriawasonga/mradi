from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class NotificationManager(models.Manager):
    def for_user(self, user):
        return self.filter(receipient=user)
    
    def unread(self, user):
        return self.for_user(user).filter(is_read=False)
    
    def read(self, user):
        return self.for_user(user).filter(is_read=True)
    
    def mark_as_read(self, user):
        return self.for_user(user).update(is_read=True)

class Notification(models.Model):
    receipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object =GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    objects = NotificationManager()

    def __str__(self):
        return f'{self.actor} {self.verb} {self.content_object} to {self.receipient}'
    class Meta:
        ordering=['-created_at']

    @property
    def noftification_time_formatted(self):
        return self.created_at.strftime('%d %b %I:%M %p')
    
