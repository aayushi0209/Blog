from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Posts(models.Model):
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg',upload_to='profile_pics')
    def __str__(self):
        # return f'{{self.user.username}}Profile'
        return self.user.username
    
    # def save(self):
    #     # super().save()
    #     img=Image.open(self.image.path)
    #     if img.height>300 or img.width>300:
    #         newsize = (200, 200)
    #         img = img.resize(newsize)
    #         img.save(self.image.path)
