from django.db import models
from django.contrib.auth.models import User
import datetime as dt

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


#Profile model
class Profile(models.Model):
  prof_pic = models.ImageField (blank=True, )
  bio = models.CharField(max_length = 200)
  user = models.OneToOneField('auth.User',on_delete=models.CASCADE, default=None)
    
  def save_profile(self):
    self.save()
            
  def update_profile(self):
    prof=Profile.objects.filter(id=Profile.id).update()
        
  def delete_image(self):
    prof=Profile.objects.filter(id=Profile.id).delete()
        
    
  @classmethod
  def profile(cls):
    profile = cls.objects.filter(id=Profile.id)
    return profile
    
  def __str__(self):
    return str(self.user)

@receiver(post_save,sender=User)
def create_profile(sender, instance,created,**kwargs):
  if created:
    Profile.objects.create(user=instance)
        
@receiver(post_save,sender=User)
def save_profile(sender, instance,**kwargs):
  instance.profile.save()

#Image Model
class Image(models.Model):
  image = models.ImageField()
  name = models.CharField(max_length =70)
  caption = models.CharField(max_length =700)
  post_date = models.DateTimeField(auto_now_add=True)
  profile = models.ForeignKey(User, on_delete=models.CASCADE)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    
  def save_image(self):
    self.save()
            
  def update_image(self):
    img=Image.objects.filter(id=Image.id).update()
        
  def update_caption(self):
    img=Image.objects.filter(id=Image.id).update()     
        
  def delete_image(self):
    img=Image.objects.filter(id=Image.id).delete()
   
  class Meta:
    ordering = ['post_date']
    
  @classmethod
  def images(cls):
    images = cls.objects.filter(id=Image.id)
    return images
    
    
  @classmethod
  def search_by_username(cls,username):
    fetch_user= User.objects.get(username=username)
    foundUser = cls.objects.filter(profile=fetch_user)
    return foundUser
    
  @classmethod
  def filter_by_user_id(cls):
    photos = cls.objects.filter(id=User.user_id)
    return photos
    
  def __str__(self):
    return str(self.name)

class Like(models.Model):
  likes = models.IntegerField (blank=True)
  image = models.ForeignKey(Image, on_delete=models.CASCADE, default=None)
  user = models.ForeignKey(User,on_delete=models.CASCADE)

  def save_like(self):
    self.save()
        
  def __str__(self):
    return str(self.likes)

class Comment(models.Model):
  comments = models.CharField(max_length =200, blank=True)
  image = models.ForeignKey(Image, on_delete=models.CASCADE, default=None)
  user = models.ForeignKey(User,on_delete=models.CASCADE)
    
  def save_comment(self):
    self.save()
        
  @classmethod
  def get_comments(cls,id):
    comments = cls.objects.filter(image__id=id)
        
    return comments
        
  def __str__(self):
    return str(self.comments)
