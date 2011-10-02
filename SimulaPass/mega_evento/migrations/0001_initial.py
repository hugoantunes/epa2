# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MegaEvento'
        db.create_table('mega_evento_megaevento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('localizacao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='evento', to=orm['mundo.Quadrante'])),
            ('qtd_pessoas_esperadas', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mega_evento', ['MegaEvento'])


    def backwards(self, orm):
        
        # Deleting model 'MegaEvento'
        db.delete_table('mega_evento_megaevento')


    models = {
        'mega_evento.megaevento': {
            'Meta': {'object_name': 'MegaEvento'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localizacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evento'", 'to': "orm['mundo.Quadrante']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'qtd_pessoas_esperadas': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
            'mundo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quadrante'", 'to': "orm['mundo.Mundo']"}),
            'percentual_pessoas': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'percentual_trnasportes': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mega_evento']
