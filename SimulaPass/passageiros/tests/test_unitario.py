# -*- coding: utf-8 -*-
from unittest import TestCase
from passageiros.models import Passageiro

class TestUnitarioPassageiro(TestCase):

    def setUp(self):
    	pass

    def tearDown(self):
    	pass

    def test_unicode_passageiro(self):
        passageiro = Passageiro()
        passageiro.nome = 'Hugo'
        assert 'Hugo' == passageiro.__unicode__()

    def test_passageiros_deveria_ter_atirbutos_corretos(self):
    	passageiro = Passageiro()

    	assert hasattr(passageiro, 'nome')
    	assert hasattr(passageiro, 'tem_carro')
    	assert hasattr(passageiro, 'conforto_toleravel')

