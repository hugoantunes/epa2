# -*- coding: utf-8 -*-
from unittest import TestCase
from transportes.models import Transporte

class TestUnitarioTransportes(TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_unicode_transportes(self):
	    transporte = Transporte()
	    transporte.nome = u'Buzão'

	    assert u'Buzão' == transporte.__unicode__()

	def test_transportes_deveria_ter_atirbutos_corretos(self):
		transporte = Transporte()

		assert hasattr(transporte, 'nome')
		assert hasattr(transporte, 'tempo_viagem')
		assert hasattr(transporte, 'capacidade_maxima')
		assert hasattr(transporte, 'capacidade_atual')
		assert hasattr(transporte, 'coeficiente_conforto')
	