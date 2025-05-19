from django.db import models
from django.contrib.auth.models import User
#importing django signals 
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import hashlib
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=255,null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def full_name(self):
        """Returns the full name of the user."""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    @property
    def date_joined(self):
        time_diff=timezone.now() - self.user.date_joined
        if time_diff <= timezone.timedelta(days=2):
            return timesince(self.join_date)+ " ago"
        else:
            return self.user.date_joined.strftime("%d-%m-%Y")
        # elif time_diff <= timezone.timedelta(days=30):
        #     return f"{time_diff.days} days ago"
        # elif time_diff <= timezone.timedelta(days=365):
        #     return f"{time_diff.days // 30} months ago"
        # else:
        #     return f"{time_diff.days // 365} years ago"   
    
    @property
    def profile_picture_url(self):
        try:
             image= self.profile_picture.url
             print(image)
        except:
            image= 'https://cdn1.iconfinder.com/data/icons/flat-business-icons/128/user-512.png'
        return image



    @property
    def avatar_initial(self):
        return self.username[0].upper() if self.username else "U"

    @property
    def avatar_color(self):
        """Generates a consistent color hex code based on the username."""
        if not self.username:
            return "#999999"

        colors = [
            "#FF5733", "#33B5FF", "#28A745", "#FFC107", "#6F42C1",
            "#E83E8C", "#17A2B8", "#FD7E14", "#20C997", "#6610f2"
        ]

        hash_val = int(hashlib.md5(self.username.encode()).hexdigest(), 16)
        return colors[hash_val % len(colors)]
        

# This function will create a profile for the user when the user is created
# It uses the post_save signal to trigger the function after a User instance is saved
# @receiver(post_save, sender=User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def create_user_profile(sender,instance,**kwargs):
        #if a user exists but no profile exists, create a profil
        Profile.objects.get_or_create(user=instance)
    

