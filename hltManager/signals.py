from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile




@receiver(post_save, sender=User)
def create_personal_info(sender,instance,created,**kwargs):
  '''
  this is a function that creates a profile of a user after registration
  '''
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_personal_info(sender,instance, **kwargs):

  '''
  this is a fuunction that saves the profile after been made
  '''
  instance.profile.save()



  





