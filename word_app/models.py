from django.db import models

class Word(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    



