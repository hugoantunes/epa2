# encoding: utf-8
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse

from passageiros.models import Passageiro
from transportes.models import Transporte

import random

def home(request):
    template = u'index.html'
    
    passageiros = Passageiro.objects.all()
    transportes = Transporte.objects.all()
    
    json_passageiros = {'passageiros':[]}

    for passageiro in passageiros:
        json_passageiros['passageiros'].append({
            'id':passageiro.id,
            'nome':passageiro.nome,
            'conforto_toleravel':passageiro.conforto_toleravel
        })
    
    context = {'passageiros':passageiros,
            'json_passageiro':simplejson.dumps(json_passageiros),
            'transportes':transportes,
    }

    return render_to_response(template, context)

def ajax(request, numero):
    
    passageiros = Passageiro.objects.all()
    transportes = Transporte.objects.all().order_by('tempo_viagem')
    possibilidades_passageiros = len(passageiros)
    
    json={'passageiros':[]}

    for i in range(int(numero)):
        embarcou = 0
        lista_transportes = []
        passageiro_modelo = Passageiro()
        transporte_modelo = Transporte()
        
        if possibilidades_passageiros > 0:
            indice = random.randint(0,possibilidades_passageiros-1)
        else:
            indice = 0
        
        passageiro_modelo = passageiros[indice]
        
        for transporte in transportes:
            if transporte.capacidade_atual<transporte.capacidade_maxima:                
                desconforto_transporte = transporte.capacidade_atual*transporte.coeficiente_conforto
                lista_transportes.append(desconforto_transporte)
                
                if desconforto_transporte < passageiro_modelo.conforto_toleravel and not transporte_modelo.nome:
                    transporte_modelo = transporte
                    transporte.capacidade_atual+=1
                    embarcou = 1
            else:
                lista_transportes.append('')
                embarcou = 0

        if lista_transportes and not embarcou:
            if min(lista_transportes) != '':
                transporte_modelo = transportes[lista_transportes.index(min(lista_transportes))]
                transportes[lista_transportes.index(min(lista_transportes))].capacidade_atual+=1
                embarcou = 1
        
        json['passageiros'].append({
            'tipo':passageiro_modelo.nome,
            'transporte':transporte_modelo.nome,
            'embarcou':embarcou,   
        })
        
    json = simplejson.dumps(json)
    
    return HttpResponse(json)