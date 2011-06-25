# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Transporte'
        db.create_table('transportes_transporte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('tempo_viagem', self.gf('django.db.models.fields.FloatField')()),
            ('capacidade_maxima', self.gf('django.db.models.fields.IntegerField')()),
            ('capacidade_atual', self.gf('django.db.models.fields.IntegerField')()),
            ('coeficiente_conforto', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('transportes', ['Transporte'])


    def backwards(self, orm):
        
        # Deleting model 'Transporte'
        db.delete_table('transportes_transporte')


    models = {
        'transportes.transporte': {
            'Meta': {'object_name': 'Transporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_maxima': ('django.db.models.fields.IntegerField', [], {}),
            'coeficiente_conforto': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tempo_viagem': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['transportes']
