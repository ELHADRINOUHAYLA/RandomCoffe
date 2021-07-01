from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.




 
class Skill(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    

class PersonalSkill(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

FreeDay_CHOICES = (
               ('Monday' , 'Monday'),
               ('Tuesday', 'Tuesday'),
               ('Wednesday', 'Wednesday'),
               ('Thursday', 'Thursday'),
               ('Friday', 'Friday'),
               ('Saturday', 'Saturday'),
               ('Sunday', 'Sunday'),

           )

TIME_CHOICES = (
    ('8AM-10AM', '8AM-10AM'),
    ('10AM-12PM', '10AM-12PM'),
    ('12PM-2PM', '12PM-2PM'),
    ('2PM-4PM', '2PM-4PM'),
    ('4PM-6PM', '4PM-6PM'),
    ('6PM-8PM', '6PM-8PM'),
)


class FreeDate(models.Model):
    FreeDay = models.CharField(max_length=200, null=True, choices=FreeDay_CHOICES)
    FreeTime = models.CharField(max_length=200, null=True, choices=TIME_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    


class MeetingPlace(models.Model):
    CoffeeName = models.CharField(max_length=200, null=True)
    Address = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.CoffeeName

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
    personalskill = models.ManyToManyField("PersonalSkill")

    
    

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



    
class Employe(models.Model):
    Ref = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.Ref



STATE_CHOICES = [
    ('Accepte', 'Accepte'),
    ('Deny', 'Deny'),
]
RATE_MEETING = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    
]

class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    state = models.CharField(max_length=200, null=True, choices=STATE_CHOICES)
    text = models.TextField(max_length=3000, null=True, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_MEETING, null=True, blank=True)

    def __str__(self):
        return self.user.username




class Meeting(models.Model):
    match1 = models.ForeignKey(Match,on_delete=models.CASCADE, related_name='match1', null=True)
    match2 = models.ForeignKey(Match,on_delete=models.CASCADE, related_name='match2', null=True)
    meeeting_place = models.ForeignKey(MeetingPlace, on_delete=models.CASCADE, null=True)
    meeting_date = models.ForeignKey(FreeDate, null=True, on_delete=models.CASCADE)
    mail_sent = models.BooleanField(default=False)




