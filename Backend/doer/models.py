from django.db import models


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Employer profile')
    phone_no = models.CharField(max_length=20, null=true, blank=true, verbose_name='Employer phone no')
    profile_pic = models.ImageField(null=True, blank=True, upload_to=upload_image_path, verbose_name='Profile picture')
    favorite_doers = models.ManyToManyField(Doer)


class Doer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Doer profile')
    phone_no = models.CharField(max_length=20, null=true, blank=true, verbose_name='Doer phone no')
    profile_pic = models.ImageField(null=True, blank=True, upload_to=upload_image_path, verbose_name='Profile picture')
    average_mark = models.DecimalField(max_digits=3, decimal_places=2)
    professions = models.ManyToManyField(Professions)
    AVAILABILITY_CHOICES = (
       ('A', 'Available'),
       ('B', 'Busy'),
       ('U', 'Unavailable'),
    )
    availability = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES)


class Professions(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)


class Request(models.Model):
    title = models.CharFiled(max_length=1024)
    description = models.CharField(max_length=2048)
    professions = models.ManyToManyFields(Professions)
    doer = models.ForeignKey(Doer, on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=32, null=True, blank=True)
    price = models.DecimalField(null=True, blank=True)
    STATUS_CHOICES = (
       ('A', 'Available'),
       ('B', 'Busy'),
       ('C', 'Closed'),
       ('D', 'Done'),
       ('P', 'In progress'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)


class RequestSubmission(models.Models):
    doer = models.ForeignKey(Doer)
    request = models.ForeignKey(Request, null=True, blank=True)
    offer = models.CharField(max_lenght=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ReportRequest(models.Models):
    request = models.ForeignKey(Request)
    description = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    REPORT_STATUS_CHOICES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    report_status = models.CharField(max_length=1, choices=REPORT_STATUS_CHOICES)


class ReportProfile(models.Models):
    profile = models.ForeignKey(User)
    description = models.CharField(max_length=512, null=True, blank=True)
    REPORT_STATUS_CHOICES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    report_status = models.CharField(max_length=1, choices=REPORT_STATUS_CHOICES)
    

class Messages(models.Models):
    sender = models.ForeignKey(User)
    receiver = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2048)

