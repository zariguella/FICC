from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from obispado.libros_contables.models import *
from obispado.plan_de_cuentas.models import *
from django.contrib.auth.models import User
import time
import csv

def index(request):
    # get_object_or_404(Poll, pk=poll_id)
    return render_to_response('balances/index.html')

def ver_balance(request):
    ''' Funcion para mostrar el balance '''

    balance = generar_balance(1, 2) # aca le paso dos enteros, pero 
                                                # deberian ser las fechas
    

def index(request):
    '''Solo muestra el template para pedir el balance'''
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        return render_to_response('balances/generar_balance.html', {'nombreuser': tipouser.username})
    else:
        return HttpResponseRedirect('/obispado/login/')

def generar_balance(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        fechaini_de_html = request.GET['fechainicio']
        fechafin_de_html = request.GET['fechafin']
        fechaini = time.strptime(str(fechaini_de_html), "%d/%m/%Y")
        fechaisoini = time.strftime("%Y-%m-%d", fechaini)
        fechafin = time.strptime(str(fechafin_de_html), "%d/%m/%Y")
        fechaisofin = time.strftime("%Y-%m-%d", fechafin)
        balance = generar_balance2(fechaisoini, fechaisofin) # como se podria llamar mejor a esta funcion? deberia llamarse desde ver_balance, o algo asi

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=balance.csv'

        writer = csv.writer(response, delimiter=';')
        #writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        #writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
        writer.writerow(['Balance']) # titulo
        writer.writerow(['']) # linea en blanco
        writer.writerow(['', '', '', '', '', 'Saldos', '', 'Inventario', '', 'Resultado'])
        writer.writerow(['', 'Concepto', '', '', '', 'Deudor', 'Acreedor', 'Activo', 'Pasivo', 'Debe', 'Haber'])
        
        for g in balance:
            saldo_tipo = g.tipo_de_saldo
            if saldo_tipo == 'd':
                writer.writerow(['', str(g.nombre), '', '', '', int(balance[g]['suma'])])
            else:
                writer.writerow(['', str(g.nombre), '', '', '', '', int(balance[g]['suma'])])
            for n1 in balance[g]:
                if n1 != 'suma':
                    if saldo_tipo == 'd':
                        writer.writerow(['', '', str(n1.nombre), '', '', int(balance[g][n1]['suma'])])
                    else:
                        writer.writerow(['', '', str(n1.nombre), '', '', '', int(balance[g][n1]['suma'])])
                    for n2 in balance[g][n1]:
                        if n2 != 'suma':
                            if saldo_tipo == 'd':
                                writer.writerow(['', '', '', str(n2.nombre), '', int(balance[g][n1][n2]['suma'])])
                            else:
                                writer.writerow(['', '', '', str(n2.nombre), '', '', int(balance[g][n1][n2]['suma'])])
                            for n3 in balance[g][n1][n2]:
                                if n3 != 'suma':
                                    if saldo_tipo == 'd':
                                        writer.writerow(['', '', '', '', str(n3.nombre), int(balance[g][n1][n2][n3]['suma'])])
                                    else:
                                        writer.writerow(['', '', '', '', str(n3.nombre), '', int(balance[g][n1][n2][n3]['suma'])])

        return response
    else:
        return HttpResponseRedirect('/obispado/login/')
