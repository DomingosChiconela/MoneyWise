from extrato.models import Valores
from datetime import datetime

def calcula_total(obj,campo):
    saldo_total=0
    for i in obj:
       saldo_total += getattr(i,campo) 
       return saldo_total 
   
   
def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)



    #total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    
    
    total_gastos_essenciais=0 
    for gastos_essenciai in gastos_essenciais:
     total_gastos_essenciais += gastos_essenciai.valor
        
    #total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')
    total_gastos_nao_essenciais=0 
    for gastos_nao_essenciai in gastos_nao_essenciais:
     total_gastos_nao_essenciais += gastos_nao_essenciai.valor

    total = (total_gastos_essenciais + total_gastos_nao_essenciais)
    try:
        percentual_gastos_essenciais =  ((total_gastos_essenciais * 100) / total)
        percentual_gastos_nao_essenciais =  ((total_gastos_nao_essenciais * 100) / total)

        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    except:
        return 0, 0