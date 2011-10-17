# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Simulacao'
        db.create_table('mundo_simulacao', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mundo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='simulacoes', to=orm['mundo.Mundo'])),
            ('qtd_pessoas_usadas', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('qtd_transportes_usados', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('qtd_carros_usados', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
        ))
        db.send_create_signal('mundo', ['Simulacao'])


    def backwards(self, orm):
        
        # Deleting model 'Simulacao'
        db.delete_table('mundo_simulacao')


    models = {
        'mundo.mundo': {
            'Meta': {'object_name': 'Mundo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'qtd_carros': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'qtd_pessoas': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'qtd_transportes': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
        },
        'mundo.quadrante': {
            'Meta': {'object_name': 'Quadrante'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mundo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quadrantes'", 'to': "orm['mundo.Mundo']"}),
            'percentual_pessoas': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'percentual_transportes': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mundo.simulacao': {
            'Meta': {'object_name': 'Simulacao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mundo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'simulacoes'", 'to': "orm['mundo.Mundo']"}),
            'qtd_carros_usados': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'qtd_pessoas_usadas': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'qtd_transportes_usados': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['mundo']
