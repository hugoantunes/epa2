# encoding: utf-8
import time
import random

from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from passageiros.models import Passageiro
from transportes.models import Transporte
from mundo.models import Mundo
from mega_evento.models import MegaEvento

def teste(request):
    template = u'simula.html'
    
    passageiros = Passageiro.objects.all()
    transportes = Transporte.objects.all()
    mundo = Mundo.objects.all()[0]
    mega_evento = qtd_pessoas_esperadas = None

    try:
        mega_evento = MegaEvento.objects.all()[0]
        qtd_pessoas_esperadas = mega_evento.qtd_pessoas_esperadas 
    except:
        pass

    total_pessoas = int(mundo.qtd_pessoas) + int(qtd_pessoas_esperadas or 0)

    context = {'request': request,
            'passageiros': passageiros,
            'transportes': transportes,
            'mundo': mundo,
            'quadrantes': mundo.quadrantes.all(),
            'mega_evento': mega_evento,
            'total_pessoas': total_pessoas            
    }
    
    return render_to_response(template, context, context_instance=RequestContext(request))

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

    return render_to_response(template, context, context_instance=RequestContext(request))

def ajax(request, numero):
    #import ipdb;ipdb.set_trace()
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
    
    return HttpResponse(json, mimetype = 'application/json')

def entra_no_transporte(request, num_carros, id_quadrante):
    transportes = Transporte.objects.all().order_by('tempo_viagem')
    
    lista_transportes = [] 

    for transporte in transportes:
        lista_transportes.append(transporte)

    lista_transportes.append('carro')

    possibilidades_maximas_de_transporte = len(lista_transportes)

    escolha = random.randint(0, possibilidades_maximas_de_transporte-1)

    import ipdb; ipdb.set_trace()
    json={'passageiros':[]} 
    json = simplejson.dumps(json)
    
    return HttpResponse(json, mimetype = 'application/json')
 
def posiciona_passageiro(request,numero):

    if int(numero)%2 ==0:
        resultado = 'par'
    else:
        resultado = 'impar'

    return HttpResponse('ajax ---- %s é %s'%(str(numero),resultado))


def posiciona_transporte(request):

    return HttpResponse('ajax2')
