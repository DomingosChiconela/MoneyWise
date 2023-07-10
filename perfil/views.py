from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse

from . models import Categoria, Conta
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from.utils import calcula_total,calcula_equilibrio_financeiro
from extrato.models import Valores
from datetime import datetime

def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    #total_entradas = calcula_total(entradas, 'valor')
    #total_saidas = calcula_total(saidas, 'valor')
    total_entradas=0
    for conta in entradas:
        total_entradas += conta.valor
       #total saida  
        total_saidas=0
    for saida in saidas:
      total_saidas += saida.valor
    
    
    contas = Conta.objects.all()
    #saldo_total = calcula_total(contas, 'valor')
    saldo_total=0
    for conta in contas:
        saldo_total += conta.valor
        
    #gastos essencias e nao essencias 
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    
    
    print(f'nao{percentual_gastos_nao_essenciais}')
    print(percentual_gastos_essenciais)
    
    return render(request, 'home.html', {'contas': contas, 'saldo_total': saldo_total,'total_saidas': total_saidas,'total_entradas': total_entradas,'percentual_gastos_essenciais': int (percentual_gastos_essenciais),'percentual_gastos_nao_essenciais':int(percentual_gastos_nao_essenciais)})
        
        
def gerenciar(request):
    contas = Conta.objects.all()
    categorias=Categoria.objects.all()
    #total_contas = contas.aggregate(Sum('valor'))
 
   # saldo_total = calcula_total(contas,'valor')
    saldo_total=0
    for conta in contas:
        saldo_total += conta.valor

    return render(request, 'gerenciar.html', {'contas': contas,'saldo_total': saldo_total,'categorias':categorias})
 
 
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
   
def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        total=0
        valores=Valores.objects.filter(categoria=categoria)
        for v in valores:
            total=total+ v.valor
        
        dados[categoria.categoria]=total
    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})
   
