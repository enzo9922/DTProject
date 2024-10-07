from django.db import models

# Create your models here.

class Participant(models.Model):
    IDParticipants = models.CharField(max_length=1000, default='none', unique=True)
    IDItems = models.CharField(max_length=1000, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Item(models.Model):
    property_name = models.CharField(max_length=255)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Items_ID = models.CharField(max_length=1000, default='none')
    
    def __str__(self):
        return f"{self.property_name} --- {self.Items_ID}"

class Bidding (models.Model):
    IDParticipants = models.CharField(max_length=1000)
    total = models.FloatField()
    item1 = models.IntegerField(default = 0)
    item2 = models.IntegerField(default = 0)
    item3 = models.IntegerField(default = 0)
    item4 = models.IntegerField(default = 0)
    item5 = models.IntegerField(default = 0)
    item6 = models.IntegerField(default = 0)
    item7 = models.IntegerField(default = 0)
    item8 = models.IntegerField(default = 0)
    item9 = models.IntegerField(default = 0)
    item10 = models.IntegerField(default = 0)
    item11 = models.IntegerField(default = 0)
    item12 = models.IntegerField(default = 0)
    item13 = models.IntegerField(default = 0)
    item14 = models.IntegerField(default = 0)
    item15 = models.IntegerField(default = 0)
    
    
    def __str__(self):
        return f"{self.IDParticipants}"

class Result(models.Model):
    fName = models.CharField(max_length=255)
    lName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    IDParticipants = models.CharField(max_length=1000)
    itemWon = models.CharField(max_length=1000)
    totalValue = models.FloatField(default=0)
    fairShare = models.FloatField(default=0)
    pay = models.FloatField(default=0)
    get = models.FloatField(default=0)

    def __str__(self):
        return f"{self.fName} {self.lName} --- {self.IDParticipants}"