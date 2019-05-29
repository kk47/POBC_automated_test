from django.db import models

# Create your models here.
class Mail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()

class Rule(models.Model):
    module = models.CharField(max_length=100)
    filter = models.CharField(max_length=100)
    chart = models.CharField(max_length=100)
    variable = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    threshold = models.CharField(max_length=100)
    level = models.IntegerField()
    to = models.CharField(max_length=1000)
    comment = models.TextField()

class Message(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    msg = models.TextField()
    isread = models.BooleanField()