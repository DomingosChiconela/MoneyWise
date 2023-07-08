def calcula_total(obj,campo):
    saldo_total=0
    for i in obj:
       saldo_total+=getattr(i,campo) 
       return saldo_total 