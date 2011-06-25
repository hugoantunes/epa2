# encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse

from passageiros.models import Passageiro
from transportes.models import Transporte

def home(request):
    template = u'index.html'
    
    passageiros = Passageiro.objects.all()
    transportes = Transporte.objects.all()

    context = {'passageiros':passageiros,
            'transportes':transportes,
    }


    return render_to_response(template, context)

def ajax(request):
    return HttpResponse('foi no ajax')