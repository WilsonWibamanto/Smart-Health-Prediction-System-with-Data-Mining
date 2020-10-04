from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Liver(models.Model):
    age = models.PositiveIntegerField()
    gender = models.IntegerField()
    totBilirubin = models.FloatField()
    dirBilirubin = models.FloatField()
    alkPhos = models.FloatField()
    alanAmino = models.FloatField()
    asparAmino = models.FloatField()
    totProt = models.FloatField()
    albumin = models.FloatField()
    agratio = models.FloatField()
    result =  models.FloatField()
    class Meta:
        db_table = "liver"

class Heart(models.Model):
    age = models.PositiveIntegerField()
    gender = models.IntegerField()
    cp = models.FloatField()
    trestbps = models.FloatField()
    chol = models.FloatField()
    fbs = models.FloatField()
    restecg = models.FloatField()
    thalach = models.FloatField()
    exang = models.FloatField()
    oldpeak = models.FloatField()
    slope =  models.FloatField()
    ca = models.FloatField()
    thal = models.FloatField()
    result =  models.IntegerField()
    class Meta:
        db_table = "heart"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    specialism = models.TextField()
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size =(200,200)
            img.thumbnail(output_size)
            img.save(self.image.path)