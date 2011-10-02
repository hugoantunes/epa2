# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Quadrante.percentual_trnasportes'
        db.delete_column('mundo_quadrante', 'percentual_trnasportes')

        # Adding field 'Quadrante.percentual_transportes'
        db.add_column('mundo_quadrante', 'percentual_transportes', self.gf('django.db.models.fields.CharField')(default=201109021846, max_length=255), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Quadrante.percentual_trnasportes'
        raise RuntimeError("Cannot reverse this migration. 'Quadrante.percentual_trnasportes' and its values cannot be restored.")

        # Deleting field 'Quadrante.percentual_transportes'
        db.delete_column('mundo_quadrante', 'percentual_transportes')


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
            'mundo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quadrantes'", 'to': "orm['mundo.Mundo']"}),
            'percentual_pessoas': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'percentual_transportes': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mundo']
