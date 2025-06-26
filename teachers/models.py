from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.name