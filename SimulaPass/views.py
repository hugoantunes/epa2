# encoding: utf-8
import time
import random

from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from passageiros.models import Passageiro, AgentePassageiro
from transportes.models import Transporte, AgenteTransporte
from mundo.models import Mundo, Simulacao
from mega_evento.models import MegaEvento

def teste(request):
    Simulacao.objects.all().delete()
    AgenteTransporte.objects.all().delete()
    AgentePassageiro.objects.all().delete()

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

def entra_no_transporte(request,id_mundo, id_quadrante):
    json={'passageiros':[], 'transportes': []}
    
    
    mundo = Mundo.objects.get(id=id_mundo)
    simulacao = Simulacao.objects.filter(mundo=mundo)
    origem = mundo.quadrantes.get(id=id_quadrante)
    destinos = mundo.quadrantes.all().exclude(id=id_quadrante)
    destino = random.choice(destinos)
 
    tipos_passageiros = Passageiro.objects.all()
    tipo_passageiro_escolhido = random.choice(tipos_passageiros)
    
    if not len(simulacao):
        simulacao = Simulacao.objects.create(
            mundo=mundo,
            qtd_pessoas_usadas=0,
            qtd_transportes_usados=0,
            qtd_carros_usados=0,
            )
    else:
        simulacao = simulacao[0]
    
    passageiro = AgentePassageiro.objects.create(
            tipo_passageiro=tipo_passageiro_escolhido,
            conforto_atual=100,
            simulacao=simulacao,
            origem=origem,
    )

    json['passageiros'].append(passageiro)
    
    if request.POST: 
        if mundo.qtd_transportes > simulacao.qtd_transportes_usados: 

            tipos_transportes = Transporte.objects.all()            
            lista_transportes = [] 

            for tipo_transporte in tipos_transportes:
                lista_transportes.append(tipo_transporte)
            
            if mundo.qtd_carros >= simulacao.qtd_carros_usados:
                lista_transportes.append('carro')

            #import ipdb; ipdb.set_trace()
            #escolhe o transporte
            escolha = random.choice(lista_transportes)
            escolha = 0            
            if lista_transportes[escolha] == 'carro':
                pass
            else:
                #quando não é carro
                tipo_transporte_escolhido = tipos_transportes[escolha]
               
                if simulacao.transportes.all() and not simulacao.transportes.filter(tipo_transporte=tipo_transporte_escolhido) :
                    #busca um transporte escolhido, que de pra ele entrar e confortavel.
                    transportes_escolhidos = simulacao.transportes.filter(tipo_transporte=tipo_transporte_escolhido, capacidade_atual__lt=tipo_transporte_escolhido.capacidade_maxima, desconforto__lte=passageiro.tipo_passageiro.conforto_toleravel)
                    
                    qtd_transportes_escolhidos = len(transportes_escolhidos)
                   
                    #se existir mais de um ele escolhe um deles.
                    if qtd_transportes_escolhidos > 0:
                        tipo_transporte_escolhido = random.choice(transportes_escolhidos)
                    else:
                        #busca transporte escolhido mesmo desconfortavel
                        transportes_escolhidos = simulacao.transportes.filter(tipo_transporte=tipo_transporte_escolhido, capacidade_atual__lt=tipo_transporte_escolhido.capacidade_maxima)
                        qtd_transportes_escolhidos = len(transportes_escolhidos)
                        if qtd_transportes_escolhidos > 0:
                            tipo_transporte_escolhido = random.choice(transportes_escolhidos)     
                        else:
                            #busca por qualquer transporte que ele possa entrar
                            transportes_escolhidos = simulacao.transportes.filter(capacidade_atual__lt=tipo_transporte_escolhido.capacidade_maxima).exclude(tipo_transporte=tipo_transporte_escolhido)
                            #
                            #
                            #
                            #ainda falta coisa aqui !!!
                            #
                            #
                            #
                        transporte = AgenteTransporte.objects.create(
                           tipo_transporte = tipo_transporte_escolhido,
                           simulacao=simulacao,
                           origem=origem, 
                           destino=destino,  
                           capcidade_atual=0,
                           desconforto=0,
                           )

                        transporte.capacidade_atual += 1
                else:
                    if mundo.qtd_transportes >= simulacao.qtd_transportes_usados+1:

                        #se não existe nenhum transporte ainda desse tipo, ele é criado e o passageiro entra
                        transporte = AgenteTransporte.objects.create(
                                tipo_transporte = tipo_transporte_escolhido,
                                simulacao=simulacao,
                                origem=origem,
                                destino=destino,
                                capacidade_atual=0,desconforto=0,
                                )

                        transporte.capacidade_atual += 1

            passageiro.transporte = transporte
                       
            if transporte.tipo_transporte.capacidade_confortavel < transporte.capacidade_atual:
                desconforto = int(float(transporte.capacidade_confortavel)/float(transporte.transporte_tipo.capacidade_confortavel)*100) 
                transporte.desconforto = desconforto
            
            transporte.save()
            passageiro.save()
            import ipdb; ipdb.set_trace()
            
            json['transportes'].append(transporte);
            json = simplejson.dumps(json)
        
    return HttpResponse(json, mimetype = 'application/json')

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

 
def posiciona_passageiro(request,numero):

    if int(numero)%2 ==0:
        resultado = 'par'
    else:
        resultado = 'impar'

    return HttpResponse('ajax ---- %s é %s'%(str(numero),resultado))


def posiciona_transporte(request):

    return HttpResponse('ajax2')
