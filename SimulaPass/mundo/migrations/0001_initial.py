# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Mundo'
        db.create_table('mundo_mundo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qtd_pessoas', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('qtd_transportes', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('permite_carros', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mundo', ['Mundo'])

        # Adding model 'Quadrante'
        db.create_table('mundo_quadrante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mundo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mundo_related', to=orm['mundo.Mundo'])),
            ('percentual_pessoas', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('percentual_trnasportes', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('permite_carros', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mundo', ['Quadrante'])


    def backwards(self, orm):
        
        # Deleting model 'Mundo'
        db.delete_table('mundo_mundo')

        # Deleting model 'Quadrante'
        db.delete_table('mundo_quadrante')


    models = {
        'mundo.mundo': {
            'Meta': {'object_name': 'Mundo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'qtd_pessoas': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'qtd_transportes': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mundo.quadrante': {
            'Meta': {'object_name': 'Quadrante'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mundo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mundo_related'", 'to': "orm['mundo.Mundo']"}),
            'percentual_pessoas': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'percentual_trnasportes': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mundo']
