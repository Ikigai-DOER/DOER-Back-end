from django.contrib import admin
from .models import *

models = [Profession, Doer, Employer, Request, RequestSubmission, ReportRequest, ReportProfile, Message, Rating]

admin.site.register(models)

