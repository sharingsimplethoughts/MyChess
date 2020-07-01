from django.db import models
from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class AboutUs(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=200,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'About Us-'+str(self.id)

class TermsAndCondition(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Terms and Condition-'+str(self.id)

class Help(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Help-'+str(self.id)

class Legal(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Legal-'+str(self.id)

class PrivacyPolicy(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'PrivacyPolicy-'+str(self.id)

class Faq(models.Model):
    title=models.CharField(max_length=500)
    title_ar=models.CharField(max_length=500,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return 'Faq-'+str(self.title)