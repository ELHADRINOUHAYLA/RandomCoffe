from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.




 
class Skill(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    






class UserProfile(models.Model):
    GENDER=(
         ('Female','Female'),
         ('Male','Male'),
         ('Others', 'Others'),
        )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    birthdate = models.DateTimeField(default=timezone.now, null=True)
    phone = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True, default=18)
    years_of_experience = models.IntegerField(null=True, default=5)
    job_title = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    profile_image = models.ImageField(null=True, blank=True)
    about = models.TextField(null=True)
    desired_user = models.ManyToManyField("self")
    skill = models.ManyToManyField("Skill")
    

    def __str__(self):
        return self.user.username





RATE_CHOICES = [
    (1, '1 - Sociable'),
    (2, '2 - Likable'),
    (3, '3 - Helpful'),
    (4, '4 - Reliable '),
    (5, '5 - Humble'),
    
]
class Review(models.Model):
    user_reviewing = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_reviewing', null=True)
    user_reviewed = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_reviewed', null=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, null=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)



    

