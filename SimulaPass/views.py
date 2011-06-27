# encoding: utf-8
import time

from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse

from passageiros.models import Passageiro
from transportes.models import Transporte



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
    
    if int(numero)%2 ==0:
        time.sleep(10);
        return HttpResponse('par')
    time.sleep(5)
    return HttpResponse('impar')