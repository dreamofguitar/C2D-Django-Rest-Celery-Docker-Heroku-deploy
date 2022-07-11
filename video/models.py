from django.db import models

# Create your models here.

class TWTestToken(models.Model):
    room = models.CharField(max_length=500)
    token = models.TextField(max_length=500)
    status = models.BooleanField(max_length=50,default= True)




    def __str__(self):
        return 'Token y Room %s %s' % self.token,self.room
        
    class Meta:
        db_table = 'TWTokenTest'

        

        