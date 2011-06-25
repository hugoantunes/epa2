# encoding: utf-8
from django.shortcuts import render_to_response
from passageiros.models import Passageiro

def home(request):
    template = u'index.html'
    context = {}

    return render_to_response(template, context)