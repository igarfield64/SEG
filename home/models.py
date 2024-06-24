from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Contractor(models.Model):
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.TextField()
    badge = models.CharField(max_length=20)
    created_by = models.CharField(max_length=20)
    created_on = models.DateTimeField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'contractors'

class Communications(models.Model):
    COMM_CLASS = ((0,'Batch'), 
                  (1, 'One to One'))
    
    SERVICE_TYPE = ((0,'Chat'), 
                    (1,'Call'))
    
    COMM_TYPE = ((0, 'Inbound'),
                 (1,'Outbound'))
    
    #contractor = models.ForeignKey('Contractors', on_delete=models.CASCADE)
    comm_class = models.IntegerField(choices=COMM_CLASS)
    label = models.TextField()
    service_type = models.IntegerField(choices=SERVICE_TYPE)
    comm_type = models.IntegerField(choices = COMM_TYPE)
    message = models.TextField()
    created_by = models.CharField(max_length=20)
    created_on = models.DateField(auto_now_add = False)
    notes = models.TextField()
    is_parent = models.BooleanField(default = False)
    parent_id = models.IntegerField(default = 0)

    def __str__(self):
        return self.label
    
    """ def parent_id_def(self, *args, **kwargs):
        if not self.is_parent:
            self.parent_id = 0
        super().save(*args, **kwargs)"""
    


class todo(models.Model):

    STATUS = ((0,'Pending'),
              (1, 'Completed'))

    task = models.TextField()
    status = models.IntegerField(choices = STATUS)
    description = models.TextField()
    assigned_to = models.CharField(max_length = 30)
    created_by = models.CharField(max_length = 30)
    added_on = models.DateField(auto_now_add = False)
    comm_id = models.IntegerField()

    def clean(self):
        try:
            comm = Communications.objects.get(id=self.comm_id)
        except Communications.DoesNotExist:
            raise ValidationError("Communication with this ID does not exist")