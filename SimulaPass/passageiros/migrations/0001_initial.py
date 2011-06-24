# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Passageiro'
        db.create_table('passageiros_passageiro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('tem_carro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('conforto_toleravel', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('passageiros', ['Passageiro'])


    def backwards(self, orm):
        
        # Deleting model 'Passageiro'
        db.delete_table('passageiros_passageiro')


    models = {
        'passageiros.passageiro': {
            'Meta': {'object_name': 'Passageiro'},
            'conforto_toleravel': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tem_carro': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['passageiros']
