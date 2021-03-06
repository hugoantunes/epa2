# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AgentePassageiro.transporte'
        db.alter_column('passageiros_agentepassageiro', 'transporte_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['transportes.AgenteTransporte']))

        # Changing field 'AgentePassageiro.origem'
        db.alter_column('passageiros_agentepassageiro', 'origem_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['mundo.Quadrante']))


    def backwards(self, orm):
        
        # Changing field 'AgentePassageiro.transporte'
        db.alter_column('passageiros_agentepassageiro', 'transporte_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['transportes.AgenteTransporte']))

        # Changing field 'AgentePassageiro.origem'
        db.alter_column('passageiros_agentepassageiro', 'origem_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['mundo.Quadrante']))


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
        'passageiros.agentepassageiro': {
            'Meta': {'object_name': 'AgentePassageiro'},
            'conforto_atual': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'origem'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'simulacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'passageiros'", 'to': "orm['mundo.Simulacao']"}),
            'tem_carro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tipo_passageiro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agente_passageiro'", 'to': "orm['passageiros.Passageiro']"}),
            'transporte': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'passageiros'", 'null': 'True', 'to': "orm['transportes.AgenteTransporte']"})
        },
        'passageiros.passageiro': {
            'Meta': {'object_name': 'Passageiro'},
            'conforto_toleravel': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tem_carro': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'transportes.agentetransporte': {
            'Meta': {'object_name': 'AgenteTransporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'desconforto': ('django.db.models.fields.IntegerField', [], {}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quadrantes_destinos'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quadrantes_origens'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'simulacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transportes'", 'to': "orm['mundo.Simulacao']"}),
            'tipo_transporte': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quadrantes_origens'", 'to': "orm['transportes.Transporte']"})
        },
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

    complete_apps = ['passageiros']
