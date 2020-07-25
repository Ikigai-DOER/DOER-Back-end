from django.db import models
from django.contrib.auth.models import User


class Profession(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)


class Doer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Doer profile')
    phone_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='Doer phone no')
    profile_pic = models.ImageField(null=True, blank=True, upload_to='upload/profile_pictures', verbose_name='Profile picture')
    average_mark = models.DecimalField(max_digits=3, decimal_places=2)
    professions = models.ManyToManyField(Profession)
    AVAILABILITY_CHOICES = (
       ('A', 'Available'),
       ('B', 'Busy'),
       ('U', 'Unavailable'),
    )
    availability = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Employer profile')
    phone_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='Employer phone no')
    profile_pic = models.ImageField(null=True, blank=True, upload_to='upload/profile_pictures', verbose_name='Profile picture')
    favorite_doers = models.ManyToManyField(Doer)


class Request(models.Model):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=2048)
    professions = models.ManyToManyField(Profession)
    doer = models.ForeignKey(Doer, on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=32, null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=3, null=True, blank=True)
    STATUS_CHOICES = (
       ('A', 'Available'),
       ('B', 'Busy'),
       ('C', 'Closed'),
       ('D', 'Done'),
       ('P', 'In progress'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)


class RequestSubmission(models.Model):
    doer = models.ForeignKey(Doer, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ReportRequest(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    REPORT_STATUS_CHOICES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    report_status = models.CharField(max_length=1, choices=REPORT_STATUS_CHOICES)


class ReportProfile(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=True, blank=True)
    REPORT_STATUS_CHOICES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    report_status = models.CharField(max_length=1, choices=REPORT_STATUS_CHOICES)
    

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver',  on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2048)


class Rating(models.Model):
    rater = models.ForeignKey(User, related_name='rater', on_delete=models.CASCADE)
    ratee = models.ForeignKey(User, related_name='ratee', on_delete=models.CASCADE)
    rate = models.IntegerField()

