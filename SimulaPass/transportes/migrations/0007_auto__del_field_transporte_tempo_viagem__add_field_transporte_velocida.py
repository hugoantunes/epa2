# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Transporte.tempo_viagem'
        db.delete_column('transportes_transporte', 'tempo_viagem')

        # Adding field 'Transporte.velocidade_confortavel'
        db.add_column('transportes_transporte', 'velocidade_confortavel', self.gf('django.db.models.fields.FloatField')(default=5), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Transporte.tempo_viagem'
        db.add_column('transportes_transporte', 'tempo_viagem', self.gf('django.db.models.fields.FloatField')(default=5), keep_default=False)

        # Deleting field 'Transporte.velocidade_confortavel'
        db.delete_column('transportes_transporte', 'velocidade_confortavel')


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
        },
        'transportes.agentetransporte': {
            'Meta': {'object_name': 'AgenteTransporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'desconforto': ('django.db.models.fields.IntegerField', [], {}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destino_transporte'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'origem_transporte'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'simulacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transportes'", 'to': "orm['mundo.Simulacao']"}),
            'tipo_transporte': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agente_transporte'", 'to': "orm['transportes.Transporte']"})
        },
        'transportes.transporte': {
            'Meta': {'object_name': 'Transporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_confortavel': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_maxima': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'velocidade_confortavel': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['transportes']
