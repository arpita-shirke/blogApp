from django.db import models

# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length=50)
    content=models.CharField(max_length=100)
    Author=models.CharField(max_length=100)
    created_at=models.DateField()
    updated_at=models.DateField()
    def __str__(self):
        return self.title
    
class Author(models.Model):
    pid=models.ForeignKey(Post,on_delete=models.CASCADE)
    