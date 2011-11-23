# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Passageiro'
        db.delete_table('passageiros_passageiro')

        # Adding model 'TipoPassageiro'
        db.create_table('passageiros_tipopassageiro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('tem_carro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('conforto_toleravel', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('passageiros', ['TipoPassageiro'])

        # Changing field 'AgentePassageiro.tipo_passageiro'
        db.alter_column('passageiros_agentepassageiro', 'tipo_passageiro_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['passageiros.TipoPassageiro']))


    def backwards(self, orm):
        
        # Adding model 'Passageiro'
        db.create_table('passageiros_passageiro', (
            ('conforto_toleravel', self.gf('django.db.models.fields.IntegerField')()),
            ('tem_carro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=90)),
        ))
        db.send_create_signal('passageiros', ['Passageiro'])

        # Deleting model 'TipoPassageiro'
        db.delete_table('passageiros_tipopassageiro')

        # Changing field 'AgentePassageiro.tipo_passageiro'
        db.alter_column('passageiros_agentepassageiro', 'tipo_passageiro_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['passageiros.Passageiro']))


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
            'permite_carros': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vazao_confortavel': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'vazao_maxima': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'vazao_moderada': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
        },
        'mundo.simulacao': {
            'Meta': {'object_name': 'Simulacao'},
            'conforto_total': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mundo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'simulacoes'", 'to': "orm['mundo.Mundo']"}),
            'qtd_carros_usados': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'qtd_pessoas_usadas': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'qtd_transportes_usados': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'tempo_total': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
        },
        'passageiros.agentepassageiro': {
            'Meta': {'object_name': 'AgentePassageiro'},
            'conforto_atual': ('django.db.models.fields.IntegerField', [], {}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destino_passageiro'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'origem_passageiro'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'simulacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'passageiros'", 'to': "orm['mundo.Simulacao']"}),
            'tem_carro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tipo_passageiro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agente_passageiro'", 'to': "orm['passageiros.TipoPassageiro']"}),
            'transporte': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'passageiros'", 'null': 'True', 'to': "orm['transportes.AgenteTransporte']"})
        },
        'passageiros.tipopassageiro': {
            'Meta': {'object_name': 'TipoPassageiro'},
            'conforto_toleravel': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tem_carro': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'transportes.agentetransporte': {
            'Meta': {'object_name': 'AgenteTransporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'desconforto': ('django.db.models.fields.IntegerField', [], {}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destino_transporte'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'origem_transporte'", 'null': 'True', 'to': "orm['mundo.Quadrante']"}),
            'simulacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transportes'", 'to': "orm['mundo.Simulacao']"}),
            'tempo_percurso': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tipo_transporte': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agente_transporte'", 'to': "orm['transportes.TipoTransporte']"})
        },
        'transportes.tipotransporte': {
            'Meta': {'object_name': 'TipoTransporte'},
            'capacidade_atual': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_confortavel': ('django.db.models.fields.IntegerField', [], {}),
            'capacidade_maxima': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'tempo_viagem': ('django.db.models.fields.FloatField', [], {}),
            'velocidade_confortavel': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['passageiros']
