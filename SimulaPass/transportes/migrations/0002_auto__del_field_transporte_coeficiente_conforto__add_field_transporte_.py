# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Transporte.coeficiente_conforto'
        db.delete_column('transportes_transporte', 'coeficiente_conforto')

        # Adding field 'Transporte.capacidade_confortavel'
        db.add_column('transportes_transporte', 'capacidade_confortavel', self.gf('django.db.models.fields.IntegerField')(default=2), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Transporte.coeficiente_conforto'
        db.add_column('transportes_transporte', 'coeficiente_conforto', self.gf('django.db.models.fields.IntegerField')(default=2), keep_default=False)

        # Deleting field 'Transporte.capacidade_confortavel'
        db.delete_column('transportes_transporte', 'capacidade_confortavel')


    models = {
        'transportes.transporte': {
            'Meta': {'object_name': 'Transporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_confortavel': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_maxima': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tempo_viagem': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['transportes']
