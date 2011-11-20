# encoding: utf-8
import random

from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from passageiros.models import Passageiro, AgentePassageiro
from transportes.models import Transporte, AgenteTransporte
from mundo.models import Mundo, Simulacao, Quadrante, DistanciasQuadrante 
from mega_evento.models import MegaEvento

def index(request):
    Simulacao.objects.all().delete()
    AgenteTransporte.objects.all().delete()
    AgentePassageiro.objects.all().delete()

    template = u'simula.html'
    
    passageiros = Passageiro.objects.all()
    transportes = Transporte.todos()
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
    mundo.permite_carros = request.POST.get('permite_carros', False)
    
    #obtem simulação 
    simulacao = Simulacao.objects.filter(mundo=mundo)

    #seta dados simulação de acordo com post
    try:
        #simulação ja criada
        simulacao = simulacao[0]
        simulacao.qtd_pessoas_usadas += len(simulacao.passageiros.all())
        simulacao.qtd_transportes_usados = len(simulacao.transportes.all())
        simulacao.qtd_carros_usados =  request.POST['num_carros_usados']
    except IndexError:
        #simulação nova
        simulacao = Simulacao.objects.create(
            mundo=mundo,
            qtd_pessoas_usadas=0,
            qtd_transportes_usados=0,
            qtd_carros_usados=0,
            tempo_total = 0,
            conforto_total = 100,
            )
    
    #seta quadrantes de acordo com post
    quadrantes = Quadrante.objects.all()
    for quadrante in quadrantes:
        quadrante.percentual_pessoas = request.POST['percent_pes_q%d' %quadrante.id]
        quadrante.percentual_transportes = request.POST['percent_trans_q%d' %quadrante.id]
        quadrante.permite_carros = request.POST.get('permite_carro_q%d' %quadrante.id, False)
        quadrante.vazao_confortavel = request.POST['vazao_confortavel_q%d' %quadrante.id] 
        quadrante.vazao_moderada = request.POST['vazao_moderada_q%d' %quadrante.id] 
        quadrante.vazao_maxima = request.POST['vazao_maxima_q%d' %quadrante.id]

    total_passageiros_geral = []
    total_passageiros_mega_evento = []
    total_transportes_geral = []
    
    soma_total_transportes = 0
    soma_total_passageiros_gerais = 0
    soma_total_passageiros_mega_evento = 0
    
    #monta lista aonde valor é o total de passageiros e indice é o quandrante
    for i in range(0,len(quadrantes)):
   
        if soma_total_passageiros_gerais < int(mundo.qtd_pessoas):
            numero_passageiros = float(mundo.qtd_pessoas)*float(quadrantes[i].percentual_pessoas)/100
            total_passageiros_geral.append(int(numero_passageiros))
            soma_total_passageiros_gerais += int(numero_passageiros) 

        if soma_total_transportes < int(mundo.qtd_transportes):
            numero_transportes = float(mundo.qtd_transportes)*float(quadrantes[i].percentual_transportes)/100
            if numero_transportes > 0 and numero_transportes < 1:
                numero_transportes = 1
            total_transportes_geral.append(int(numero_transportes))
            soma_total_transportes += int(numero_transportes)

        if soma_total_passageiros_mega_evento < int(mega_evento.qtd_pessoas_esperadas):
            numeros_passageiros_mega_evento = float(mega_evento.qtd_pessoas_esperadas)*float(quadrantes[i].percentual_pessoas)/100 
            total_passageiros_mega_evento.append(int(numeros_passageiros_mega_evento))
            soma_total_passageiros_mega_evento += int(numeros_passageiros_mega_evento)

    #traz lista de tipos de passageiros e transportes
    tipos_passageiros = Passageiro.objects.all()
    tipos_transportes = Transporte.todos()

    #cria todos os agentes de transporte por quadrantes
    for i in range(0, len(total_transportes_geral)):
        for j in range(0, total_transportes_geral[i]):
            AgenteTransporte.objects.create(
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
    random.shuffle(agentes_passageiros['id_passageiros'])
    json = simplejson.dumps(agentes_passageiros)
     
    return HttpResponse(json, mimetype = 'application/json')

def aloca_passageiros(request, id_passageiro):
    #obtem passageiro que vai ser alocado
    passageiro = AgentePassageiro.objects.get(id=id_passageiro)
    tem_carro = [True, False] 

    #obtem lista de transportes
    carro = Transporte.objects.get(nome='carro')
    transportes = AgenteTransporte.objects.filter(origem=passageiro.origem, destino=passageiro.destino).exclude(tipo_transporte=carro)

    #Possui carro ?
    passageiro.simulacao.mundo.qtd_carros = request.POST['num_carros']
    if request.POST.get('permite_carro_q%d' %passageiro.origem.id, False) == 'on':
        passageiro.origem.permite_carros=True
    else:
        passageiro.origem.permite_carros=False
    
    if request.POST.get('permite_carros', False) == 'on':
        passageiro.simulacao.mundo.permite_carros=True
    else:
        passageiro.simulacao.mundo.permite_carros=False

    #escolhe tipo de transporte
    tipo_transporte_escolhido = random.choice(Transporte.todos())
    #Se ainda há carros disponiveis no mundo
    
    #Se tipo do passageiro permite carro e quandrante permite carro
    if passageiro.tipo_passageiro.tem_carro == True and passageiro.origem.permite_carros and  passageiro.simulacao.mundo.permite_carros:

        if int(passageiro.simulacao.qtd_carros_usados) < int(passageiro.simulacao.mundo.qtd_carros):
            #Se passageiro tem carro
            if random.choice(tem_carro) == True:
                #Entra no carro
                passageiro.entra_carro()
                passageiro.simulacao.qtd_carros_usados += 1
                passageiro.simulacao.save()

    if not passageiro.dentro_transporte: 
        #passageiro tenta ir no transporte predileto
        transportes_possiveis = transportes.filter(tipo_transporte=tipo_transporte_escolhido)
        if transportes_possiveis:
            for transporte in transportes_possiveis:
                if not passageiro.dentro_transporte:
                    if transporte.ha_vagas:
                       passageiro.entra_transporte(transporte)
                       passageiro.simulacao.qtd_transportes_usados +=1
        else:
            #não tendo transporte predileto ele tenta ir no mais rapido, mais confortavel possivel
            transportes_possiveis = transportes.order_by('-tipo_transporte__tempo_viagem')
            for transporte in transportes_possiveis:
                if not passageiro.dentro_transporte:
                    if transporte.ha_vagas:
                        if int(transporte.desconforto) <= int(passageiro.tipo_passageiro.conforto_toleravel):
                           passageiro.entra_transporte(transporte)
                           passageiro.simulacao.qtd_transportes_usados +=1
                    else:
                        pass
                        #remove transporte que eu ja sei que não possui vagas
                        #transportes_possiveis.exclude(transporte)
                #se ainda não entrou ele tenta ir em qualquer um dando preferencia pelos mais rapidos
                if not passageiro.dentro_transporte: 
                    for transporte in transportes_possiveis:
                       if transporte.ha_vagas:
                           passageiro.entra_transporte(transporte)
                           passageiro.simulacao.qtd_transportes_usados +=1

    passageiro.simulacao.qtd_pessoas_usadas +=1
    passageiro.simulacao.save()
    
    json = {} 
    passageiros_alocados =  AgentePassageiro.objects.filter(origem=passageiro.origem).exclude(transporte=None).count()
    passageiros_desalocados = AgentePassageiro.objects.filter(origem=passageiro.origem).count() - passageiros_alocados
    if passageiro.transporte:
        json.update({
            'tipo_transporte':passageiro.transporte.tipo_transporte.nome,
            'passageiros_alocados': passageiros_alocados,
            'passageiros_desalocados': passageiros_desalocados,
            'quadrante': passageiro.origem.id,
            })
        if passageiro.tem_carro == True:
            
            aumento = float(1)/float(passageiro.simulacao.mundo.qtd_carros)*100
             
            json.update({
                    'transporte': 'q%d_carro'%passageiro.origem.id,
                    'aumento': aumento*2,
            })

        else:
            qtd_passageiros, total_lugares = 0, 0
            for transporte in AgenteTransporte.objects.filter(tipo_transporte = passageiro.transporte.tipo_transporte, origem=passageiro.transporte.origem):
                qtd_passageiros += transporte.capacidade_atual
                total_lugares += transporte.tipo_transporte.capacidade_maxima
            aumento = int(float(qtd_passageiros)/float(total_lugares)*100)

            
            json.update({
                    'transporte': 'q%d_t%d'%(passageiro.origem.id, passageiro.transporte.tipo_transporte.id),
                    'aumento': aumento*2,
            })
     
    json = simplejson.dumps(json)
        
    return HttpResponse(json, mimetype = 'application/json')

def monta_mapa(request):
    json = {'transportes': []}
     
    transportes = AgenteTransporte.objects.filter(capacidade_atual__gt=0)

    for transporte in transportes: 
        
        transporte.origem.vazao_confortavel = request.POST[u"vazao_confortavel_q%d"%transporte.origem.id]
        transporte.origem.vazao_moderada = request.POST[u"vazao_moderada_q%d"%transporte.origem.id]
        transporte.destino.vazao_confortavel = request.POST[u"vazao_confortavel_q%d"%transporte.destino.id]
        transporte.destino.vazao_moderada = request.POST[u"vazao_moderada_q%d"%transporte.destino.id]

        velocidade_origem = 0
        velocidade_destino = 0
        
        if transporte.origem != transporte.destino:
            distancia_percorrida = DistanciasQuadrante.objects.get(origem=transporte.origem, destino=transporte.destino)
            distancia_percorrida.distancia = request.POST['distancia_q%d_q%d' % (transporte.origem.id, transporte.destino.id)]
            percorrido_origem = float(distancia_percorrida.distancia)/2 
            percorrido_destino = float(distancia_percorrida.distancia)/2
        else:
            percorrido_origem = 0  
            percorrido_destino = 0 

        
        transportes_na_origem = transporte.simulacao.transportes.filter(origem=transporte.origem)
        transportes_no_destino = transporte.simulacao.transportes.filter(origem=transporte.origem)

        if transporte.tipo_transporte.nome == "metro":
            velocidade_origem = transporte.tipo_transporte.velocidade_confortavel
            velocidade_destino = transporte.tipo_transporte.velocidade_confortavel
            tempo_na_origem = percorrido_origem/velocidade_origem
            tempo_no_destino = percorrido_destino/velocidade_destino
        else:
        
            if len(transportes_na_origem) <= int(transporte.origem.vazao_confortavel):
                velocidade_origem = transporte.tipo_transporte.velocidade_confortavel
            elif len(transportes_na_origem) <= int(transporte.origem.vazao_moderada):
                velocidade_origem = transporte.tipo_transporte.velocidade_confortavel - transporte.tipo_transporte.velocidade_confortavel*0.5 
                if int(transporte.desconforto) <= 95:
                    transporte.desconforto += 5
            else:
                velocidade_origem = transporte.tipo_transporte.velocidade_confortavel - transporte.tipo_transporte.velocidade_confortavel*0.8 
                if int(transporte.desconforto) <= 90:
                    transporte.desconforto += 10
        
            tempo_na_origem = percorrido_origem/velocidade_origem
            
            if int(transporte.destino.vazao_confortavel) >= len(transportes_no_destino):
                velocidade_destino = transporte.tipo_transporte.velocidade_confortavel
            elif int(transporte.destino.vazao_moderada) >= len(transportes_no_destino):
                velocidade_destino = transporte.tipo_transporte.velocidade_confortavel - transporte.tipo_transporte.velocidade_confortavel*0.5 
                if int(transporte.desconforto) <= 95:
                    transporte.desconforto += 5
            else:
                velocidade_destino = transporte.tipo_transporte.velocidade_confortavel - transporte.tipo_transporte.velocidade_confortavel*0.8 
                if int(transporte.desconforto) <= 90:
                    transporte.desconforto += 10

            tempo_no_destino = percorrido_destino/velocidade_destino
        
        transporte.tempo_percurso = int((tempo_no_destino+tempo_na_origem))
        transporte.save()

        json['transportes'].append({
            "id":transporte.id,
            "tipo_transporte":transporte.tipo_transporte.nome,
            "origem": "q%d" %transporte.origem.id,
            "tempo_origem": tempo_na_origem,
            "destino":"q%d" %transporte.destino.id,
            "tempo_destino": tempo_no_destino,
            "tempo": transporte.tipo_transporte.tempo_viagem,
            "status":transporte.status,
            })
    
    
    transportes = AgenteTransporte.objects.filter(capacidade_atual__gt=0)
    total_desconforto = 0
    total_tempo = 0 

    for transporte in transportes:
        total_desconforto += transporte.desconforto 
        total_tempo += transporte.tempo_percurso

    numero_viagens = len(transportes)

    simulacao = Simulacao.objects.all()[0]
    simulacao.tempo_total = total_tempo/numero_viagens 
    simulacao.conforto_total = 100 - total_desconforto/numero_viagens 

    simulacao.save()
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
    transportes = Transporte.todos()
    
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
    transportes = Transporte.todos().order_by('tempo_viagem')
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
