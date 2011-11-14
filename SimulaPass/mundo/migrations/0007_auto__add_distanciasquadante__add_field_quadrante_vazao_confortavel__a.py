# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DistanciasQuadante'
        db.create_table('mundo_distanciasquadante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origem', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origens', to=orm['mundo.Quadrante'])),
            ('destino', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destinos', to=orm['mundo.Quadrante'])),
            ('distancia', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
        ))
        db.send_create_signal('mundo', ['DistanciasQuadante'])

        # Adding field 'Quadrante.vazao_confortavel'
        db.add_column('mundo_quadrante', 'vazao_confortavel', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=255), keep_default=False)

        # Adding field 'Quadrante.vazao_moderada'
        db.add_column('mundo_quadrante', 'vazao_moderada', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=255), keep_default=False)

        # Adding field 'Quadrante.vazao_maxima'
        db.add_column('mundo_quadrante', 'vazao_maxima', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=255), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'DistanciasQuadante'
        db.delete_table('mundo_distanciasquadante')

        # Deleting field 'Quadrante.vazao_confortavel'
        db.delete_column('mundo_quadrante', 'vazao_confortavel')

        # Deleting field 'Quadrante.vazao_moderada'
        db.delete_column('mundo_quadrante', 'vazao_moderada')

        # Deleting field 'Quadrante.vazao_maxima'
        db.delete_column('mundo_quadrante', 'vazao_maxima')


    models = {
        'mundo.distanciasquadante': {
            'Meta': {'object_name': 'DistanciasQuadante'},
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinos'", 'to': "orm['mundo.Quadrante']"}),
            'distancia': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origens'", 'to': "orm['mundo.Quadrante']"})
        },
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
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vazao_confortavel': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'vazao_maxima': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'vazao_moderada': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
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
