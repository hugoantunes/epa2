# encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse

from passageiros.models import Passageiro
from transportes.models import Transporte

import time

def home(request):
    template = u'index.html'
    
    passageiros = Passageiro.objects.all()
    transportes = Transporte.objects.all()
    
    context = {'passageiros':passageiros,
            'transportes':transportes,
    }


    return render_to_response(template, context)

def ajax(request, numero):
    
    if int(numero)%2 ==0:
        time.sleep(10);
        return HttpResponse('par')
    time.sleep(5)
    return HttpResponse('impar')