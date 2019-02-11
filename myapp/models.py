from django.db import models
from django.urls import reverse

class Employee(models.Model):  
    eid = models.IntegerField()  
    ename = models.CharField(max_length=100)  
    eemail = models.EmailField()  
    econtact = models.CharField(max_length=15)
    eimage = models.ImageField(upload_to='Employee')  


    class Meta:  
        db_table = "emp"
        ordering = ['-ename']
        
    def __str__(self):
    	return self.ename

    def get_absolute_url(self):
        return reverse('detail' ,kwargs={'id':self.id})    
'''        
# Create your models here.
class Property(models.Model):  
    #thumb = models.ImageField(upload_to='Employee')  
    images = models.ManyToManyField(ImageModel)

class ImageModel(models.Model):
    image = models.ImageField(upload_to='Employee')  
    is_thumb = models.BooleanField(default=False)
'''

























