from django.db import models

class Passageiro(models.Model):
    nome =  models.CharField(max_length=90)
    tem_carro =  models.BooleanField()
    conforto_toleravel = models.FloatField()
    
    def __unicode__(self):
        return self.nome