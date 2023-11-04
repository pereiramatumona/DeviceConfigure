from django.db import models

# Create your models here.

class Devices(models.Model):

    fabricante_choices = (
        ('Cisco System','Cisco System'),
        ('Huawei','Huawei'),
        ('H3C','H3C'),
        )

    device = models.CharField('Devices',max_length=15)
    ip_addr = models.CharField('IP Address',max_length=15)
    fabricante = models.CharField('Manufacture',max_length=15, choices=fabricante_choices)

    class Meta:
        db_table = "Devices"

        
    def __str__(self) -> str:
        return f'{self.device} {self.ip_addr}'