# encoding: utf-8
import time
import random

from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from passageiros.models import Passageiro, AgentePassageiro
from transportes.models import Transporte, AgenteTransporte
from mundo.models import Mundo, Simulacao, Quadrante
from mega_evento.models import MegaEvento

def index(request):
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

def constroi_mundo(request,id_mundo):
    #obtem mundo
    mundo = Mundo.objects.get(id=id_mundo)
    
    mega_evento = MegaEvento.objects.all()[0]
    mega_evento.qtd_pessoas_esperadas = request.POST['num_pessoas_evento'] 

    #obtem seta dados do mundo de acordo com o post 
    mundo.qtd_pessoas = request.POST['num_pessoas']
    mundo.qtd_carros = request.POST['num_carros']
    mundo.qtd_transportes = request.POST['num_transportes']
    mundo.permite_carros = request.POST['permite_carros']
    
    #obtem simulação 
    simulacao = Simulacao.objects.filter(mundo=mundo)

    #seta dados simulação de acordo com post
    try:
        #simulação ja criada
        simulacao = simulacao[0]
        simulacao.qtd_pessoas_usadas += len(simulacao.passageiros)
        simulacao.qtd_transportes_usados = len(simulacao.transportes)
        simulacao.qtd_carros_usados =  request.POST['num_carros_usados']
    except IndexError:
        #simulação nova
        simulacao = Simulacao.objects.create(
            mundo=mundo,
            qtd_pessoas_usadas=0,
            qtd_transportes_usados=0,
            qtd_carros_usados=0,
            )
    
    #seta quadrantes de acordo com post
    quadrantes = Quadrante.objects.all()
    for quadrante in quadrantes:
        quadrante.percentual_pessoas = request.POST['percent_pes_q%d' %quadrante.id]
        quadrante.percentual_transportes = request.POST['percent_trans_q%d' %quadrante.id]
        quadrante.permite_carros = request.POST.get('permite_carro_q%d' %quadrante.id, False)
   
    total_passageiros_geral = []
    total_passageiros_mega_evento = []
    total_transportes_geral = []
    
    #monta lista aonde valor é o total de passageiros e indice é o quandrante
    for i in range(0,len(quadrantes)):
        total_passageiros_geral.append(int(float(mundo.qtd_pessoas)*float(quadrantes[i].percentual_pessoas)/100))
        total_transportes_geral.append(int(float(mundo.qtd_transportes)*float(quadrantes[i].percentual_transportes)/100))
    
        total_passageiros_mega_evento.append(int(float(mega_evento.qtd_pessoas_esperadas)*float(quadrantes[i].percentual_pessoas)/100))


    #traz lista de tipos de passageiros e transportes
    tipos_passageiros = Passageiro.objects.all()
    tipos_transportes = Transporte.objects.all()

    #cria todos os agentes de transporte por quadrantes
    for i in range(0, len(total_transportes_geral)):
        for j in range(0, total_transportes_geral[i]):
            transporte = AgenteTransporte.objects.create(
            tipo_transporte = random.choice(tipos_transportes),
            simulacao=simulacao,
            origem=quadrantes[i], 
            destino=random.choice(quadrantes.all().exclude(id=quadrantes[i].id)),  
            capacidade_atual=0,
            desconforto=0,
            )

    agentes_passageiros = {'id_passageiros':[]}
    #cria todos os agentes de passageiros por quadrantes
    for i in range(0, len(total_passageiros_geral)):
        for j in range(0, total_passageiros_geral[i]):
            passageiro = AgentePassageiro.objects.create(
            tipo_passageiro=random.choice(tipos_passageiros),
            conforto_atual=100,
            simulacao=simulacao,
            origem=quadrantes[i],
            destino=random.choice(quadrantes.all().exclude(id=quadrantes[i].id))
            )
            agentes_passageiros['id_passageiros'].append(passageiro.id)
    
    #cria todos os agentes de passageiros por quadrantes que vao ao mega evento
    for i in range(0, len(total_passageiros_mega_evento)):
        for j in range(0, total_passageiros_mega_evento[i]):
            passageiro = AgentePassageiro.objects.create(
            tipo_passageiro=random.choice(tipos_passageiros),
            conforto_atual=100,
            simulacao=simulacao,
            origem=quadrantes[i],
            destino=mega_evento.localizacao
            )
            agentes_passageiros['id_passageiros'].append(passageiro.id)
       
    #######retornar o total de lugares em cada tipo de transporte por quadrante no json 
    
    json = simplejson.dumps(agentes_passageiros)
        
    return HttpResponse(json, mimetype = 'application/json')

def aloca_passageiros(request, id_passageiro):
    #obtem passageiro que vai ser alocado
    passageiro = AgentePassageiro.objects.get(id=id_passageiro)
    tem_carro = [True, False] 
    #obtem lista de transportes
    transportes = AgenteTransporte.objects.all()
    
    #Possui carro ?
    if passageiro.simulacao.qtd_carros_usados < passageiro.simulacao.mundo.qtd_carros:
        if passageiro.tipo_passageiro.possui_carro == True:
            if random.choice(tem_carro) == True:
                #SETAR PASSAGEIRO COM CARRO, PENSAR NISSO MAIS UM POUCO
                passageiro.simulacao.qtd_carros_usados += 1
        else:
            pass
        #Qual transporte vai pra onde o passageiro que ir 

        #confortavel

        #rapido 

    passageiro.simulacao.qtd_pessoas_usadas +=1
    passageiro.simulacao.save()
    return HttpResponse('alocou')

    

def entra_no_transporte(request,id_mundo, id_quadrante):
    json={'passageiros':[], 'transportes': []}
    
    mundo = Mundo.objects.get(id=id_mundo)
    simulacao = Simulacao.objects.filter(mundo=mundo)

    #seta dados simulação de acordo com post
    try:
        #simulação ja criada
        simulacao = simulacao[0]
        simulacao.qtd_pessoas_usadas += len(simulacao.passageiros)
        simulacao.qtd_transportes_usados = len(simulacao.transportes)
        simulacao.qtd_carros_usados =  request.POST['num_carros_usados']
    except:
        pass
        
    #obtem origem dato o id do quadrante que pela url do ajax
    origem = mundo.quadrantes.get(id=id_quadrante)

    #seta os dados do quadrante de origem de acordo com post
    origem.percentual_pessoas = request.POST['percent_pes_q%d' %origem.id]
    origem.percentual_transportes = request.POST['percent_trans_q%d' %origem.id]
    origem.permite_carros = request.POST['permite_carro_q%d' %origem.id]
   
    #tudo que não é origem é destino,
    destinos = mundo.quadrantes.all().exclude(id=id_quadrante)

    #escolhe um destino 
    destino = random.choice(destinos)
 
    tipos_passageiros = Passageiro.objects.all()
    tipo_passageiro_escolhido = random.choice(tipos_passageiros)
    

    
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
                                capacidade_atual=0,
                                desconforto=0,
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



'''
#####################################################
                                                    #
                                                    #
    AS VIEWS ABAIXO FORAM USADAS PARA O PROTOTIPO   #
                                                    #
                                                    #
#####################################################
'''

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
