from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse

from . models import Categoria, Conta
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from.utils import calcula_total

def home(request):
    contas = Conta.objects.all()
    saldo_total = calcula_total(contas, 'valor')
    return render(request, 'home.html', {'contas': contas, 'saldo_total': saldo_total})
        
        
def gerenciar(request):
    contas = Conta.objects.all()
    categorias=Categoria.objects.all()
    #total_contas = contas.aggregate(Sum('valor'))
 
    valor_total = calcula_total(contas, 'valor')
    return render(request, 'gerenciar.html', {'contas': contas,'valor_total': valor_total,'categorias':categorias})
 
 
def cadastrar_banco(request):
   apelido= request.POST.get('apelido')
   banco = request.POST.get('banco')
   tipo = request.POST.get('tipo')
   valor = request.POST.get('valor')
   icone = request.FILES.get('icone')
   
   
   if len( apelido.strip()) == 0 or len(valor.strip()) == 0:
      #TODO realizar mais validacoes
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
      return redirect(reverse('gerenciar'))

    
    
   conta=Conta(apelido=apelido,banco=banco,tipo=tipo,valor=valor,icone=icone)
   
   conta.save()
   return redirect(reverse('gerenciar'))
   
   
def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect(reverse('gerenciar'))
 
 
def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
#TODO realizar validacoes 
    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect(reverse('gerenciar'))


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect(reverse('gerenciar'))
   
   
