# Create your views here.
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from obispado.ingresos.models import *
from obispado.aportantes.models import *
from obispado.libros_contables.models import *
from obispado.plan_de_cuentas.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q, Max, Min
import datetime, string
import time
from datetime import date
import csv
from django.db.models import Count  
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.template import RequestContext

def index(request):
    lista_ultimos_ingresos = Venta.objects.all().order_by('-fecha')[:5]
    return render_to_response('ingresos/index.html', {'lista_ultimos_ingresos': lista_ultimos_ingresos})

def sumar(x, y):
    return x + y    

def carga(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        listcuentas = []
        n1 = CuentaNivel1.objects.filter(nombre__icontains="Ingresos")
        n2 = CuentaNivel2.objects.filter(tipo = n1[0].id)
        if n2.count()>0:
            for z in n2:
                #listcuentas
                n3 = CuentaNivel3.objects.filter(tipo = z.id)
                if n3.count()>0:
                    for y in n3:
                        listcuentas.append({"id":y.id, "nombre":y.nombre})
        apo = Aportante.objects.all().order_by("id")
        
        if 'ap' in request.GET and request.GET['ap']:
            #d = request.GET['des1']
            ap = request.GET['ap']
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
            #tipodoc
            tipodoc = request.GET['tipodoc']
            #ruc = request.GET['ruc']
            nrofac = request.GET['nrofac']
            if 'tot' in request.GET and request.GET['tot']:
                tot = request.GET['tot']
            #else:
            #    tot = 1000
            #final = ap+fe+ruc+cant+des+pu+ex+tot
            
            verfac = Venta.objects.filter(numero_factura=nrofac)
            if verfac.count()>0:
                return render_to_response('ingresos/carga_ingreso.html', {'apo': apo, 'con':listcuentas, 'msj': 'Ya existe ese numero de documento.','button': 'Enviar'})
            
            tipo_doc_str = ''
            if tipodoc == '1':
                tipo_doc_str = 'f'
            elif tipodoc == '2':
                tipo_doc_str = 'r'
            id_aportante = Aportante.objects.filter(nombre=ap)
            valormaximo = Aportante.objects.aggregate(Max('id'))
            valapmax = valormaximo['id__max']
            if valapmax:
                valapmax = valapmax + 1
            else:
                valapmax = 1
            newingreso = Venta(fecha = fechaiso, aportante_id=ap, numero_factura=nrofac, tipo_comprobante=tipo_doc_str)
            newingreso.save()
            newasiento = AsientoContable(fecha = fechaiso, comentario = "ingreso: " + str(newingreso.id))
            newasiento.save()
            listcant = []
            listdes = []
            listpu = []
            listex = []
            cont = 0
            for i in range(1, 11):
                if 'cant'+str(i) in request.GET and request.GET['cant'+str(i)]:
                    listcant.append(request.GET['cant'+str(i)])
                    cont = cont + 1
                else:
                    listcant.append('0')
                if 'des'+str(i) in request.GET and request.GET['des'+str(i)]:
                    listdes.append(request.GET['des'+str(i)])
                else:
                    listdes.append('0')
                if 'pu'+str(i) in request.GET and request.GET['pu'+str(i)]:
                    listpu.append(request.GET['pu'+str(i)])
                else:
                    listpu.append('0')
                if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                    listex.append(request.GET['ex'+str(i)])
                else:
                    listex.append('0')
                
            summonto = 0
            for i in range(0, 10):
                if listdes[i] != '0':
                    newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id = int(listdes[i]), monto = float(listex[i]))
                    newventaasiento.save()
                    summonto = summonto + float(listex[i])
            #summonto = reduce(sumar, listex)
            #Cambiar a "Caja"
            id_de_cuenta = CuentaNivel3.objects.get(nombre="Caja")
            #cue = id_de_cuenta.count()
            newventaasiento = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id =id_de_cuenta.id, monto = summonto)
            newventaasiento.save()
            nuevoidasiento = Venta.objects.get(id=newingreso.id)
            nuevoidasiento.asiento_id = newasiento.id
            nuevoidasiento.save()
            #return render_to_response('ingresos/carga_ingreso.html')
            #Ventas.objects.get(id=request.GET['ap']).delete()
            #return HttpResponseRedirect('/carga_ingresos/')
            #apo = Aportante.objects.all().order_by("id")
            #con = CuentaNivel3.objects.all().order_by("id")
            fecha = time.strptime(str(date.today()), "%Y-%m-%d")
            #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
            path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
            archivo = open(path, "a")
            escribir = "El usuario " + tipouser.username + " cargo el ingreso del documento nro "+str(nrofac)+" el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
            archivo.write(escribir)
            archivo.close()
            return render_to_response('ingresos/carga_ingreso.html', {'nombreuser': tipouser.username,'apo': apo, 'con':listcuentas, 'msj': 'Ingreso Agregado Correctamente','button': 'Enviar'})
            #return render_to_response('ingresos/carga_ingreso.html', {'msj': fechaiso})
            #return render_to_response('ingresos/index.html', {'final': summonto})
        else:
            #con = CuentaNivel3.objects.all().order_by("id")
            return render_to_response('ingresos/carga_ingreso.html', {'nombreuser': tipouser.username,'apo': apo, 'con':listcuentas,'button': 'Enviar'})
        return render_to_response('ingresos/carga_ingreso.html',{'button': 'Editar'})
    else:
        return HttpResponseRedirect('/obispado/login/')

def edit_ingresos(request, i_id):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        listatot = []
        listf = []
        fact = ""
        fec = ""
        if i_id:
            listhd = AsientoHaberDetalle.objects.filter(asiento=i_id).distinct()
            idventa = Venta.objects.filter(asiento=i_id)
            if idventa.count()>0:
                idventa = Venta.objects.get(asiento=i_id)
                apor = Aportante.objects.get(id=int(idventa.aportante_id))
                if listhd.count()>0:
                    for z in listhd:
                        cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                        fact = idventa.tipo_comprobante
                        if fact == "f":
                            fact = "Factura"
                        elif fact == "r":
                            fact = "Recibo"
                        fecha = idventa.fecha.timetuple()
                        fec = time.strftime("%d/%m/%Y", fecha)
                        listatot.append({"id":z.asiento_id, "fecha":fec, "aportante":apor.nombre,"nro_fac":idventa.numero_factura,"tipo_doc":fact,"cuenta":cue.id,"monto":int(z.monto)})
                cantfalta = 10 - int(listhd.count())
                desde =int(listhd.count()) + 1
                for i in range(0, cantfalta):
                    listf.append(i+int(desde))
                apo = Aportante.objects.all().order_by("id")
                listcuentas = []
                n1 = CuentaNivel1.objects.filter(nombre__icontains="Ingresos")
                n2 = CuentaNivel2.objects.filter(tipo = n1[0].id)
                if n2.count()>0:
                    for z in n2:
                        #listcuentas
                        n3 = CuentaNivel3.objects.filter(tipo = z.id)
                        if n3.count()>0:
                            for y in n3:
                                    listcuentas.append({"id":y.id, "nombre":y.nombre})
                #apo = Aportante.objects.all().order_by("id")
                #venta_edit = Venta.objects.get(asiento=id)
                return render_to_response('ingresos/edit_ingreso.html',{'nombreuser': tipouser.username,'apo': apo, 'con':listcuentas,'ltot':listatot, 'idapo':apor.id, 'rucval':apor.ruc, 'feval':fec, 'tipo_doc':fact, 'nro_fact':idventa.numero_factura, 'cantval':listhd.count(), 'cantfalta':cantfalta, 'desde':desde, 'listf':listf, 'nro':i_id} )
            else:
                return HttpResponseRedirect('/obispado/ingresos_list/')
        else:
            return HttpResponseRedirect('/obispado/ingresos_list/')
        return HttpResponseRedirect('/obispado/ingresos_list/')
    else:
        return HttpResponseRedirect('/obispado/login/')
    
def update_ingresos(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        listcuentas = []
        n1 = CuentaNivel1.objects.filter(nombre__icontains="Ingresos")
        n2 = CuentaNivel2.objects.filter(tipo = n1[0].id)
        if n2.count()>0:
            for z in n2:
                #listcuentas
                n3 = CuentaNivel3.objects.filter(tipo = z.id)
                if n3.count()>0:
                    for y in n3:
                        listcuentas.append({"id":y.id, "nombre":y.nombre})
        apo = Aportante.objects.all().order_by("id")
        if 'ap' in request.GET and request.GET['ap']:
            #d = request.GET['des1']
            ap = request.GET['ap']
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
            #tipodoc
            tipodoc = request.GET['tipodoc']
            #ruc = request.GET['ruc']
            nrofac = request.GET['nrofac']
            nro_mod = request.GET['nro_mod']
            if 'tot' in request.GET and request.GET['tot']:
                tot = request.GET['tot']
            #else:
            #    tot = 1000
            #final = ap+fe+ruc+cant+des+pu+ex+tot
            tipo_doc_str = ''
            if tipodoc == '1':
                tipo_doc_str = 'f'
            elif tipodoc == '2':
                tipo_doc_str = 'r'
                
            
            #id_aportante = Aportante.objects.filter(nombre=ap)
            valormaximo = Aportante.objects.aggregate(Max('id'))
            valapmax = valormaximo['id__max']
            if valapmax:
                valapmax = valapmax + 1
            else:
                valapmax = 1
            newingreso = Venta.objects.get(asiento =nro_mod)
            
            verfac = Venta.objects.filter(numero_factura=nrofac)
            if verfac.count()>0 and verfac[0].numero_factura != newingreso.numero_factura:
                return render_to_response('ingresos/carga_ingreso.html', {'apo': apo, 'con':listcuentas, 'msj': 'Ya existe otro documento con ese numero.','button': 'Enviar', 'at': 'Ya existe otro documento con ese numero.'})    
            
            
            fecha = time.strptime(str(date.today()), "%Y-%m-%d")
            #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
            path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
            archivo = open(path, "a")
            escribir = "El usuario " + tipouser.username + " ha modificado el ingreso con numero de documento: "+str(newingreso.numero_factura)+ " el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
            archivo.write(escribir)
            if int(newingreso.numero_factura) != int(nrofac):
                escribir = "El usuario " + tipouser.username + " ha cambiado el numero de factura de ingreso: de "+str(newingreso.numero_factura)+ " a "+ str(nrofac) +" el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
                archivo.write(escribir)

            archivo.close()
            
            newingreso.fecha = fechaiso
            newingreso.aportante_id = ap
            newingreso.numero_factura = nrofac
            newingreso.tipo_comprobante = tipo_doc_str
            #newingreso = Venta(fecha = fechaiso, aportante_id=ap, numero_factura=nrofac, tipo_comprobante=tipo_doc_str)
            newingreso.save()
            newasiento = AsientoContable.objects.get(id=nro_mod)
            newasiento.fecha = fechaiso
            newasiento.comentario = "ingreso: " + str(newingreso.id)
            #newasiento = AsientoContable(fecha = fechaiso, comentario = "ingreso: " + str(newingreso.id))
            newasiento.save()
            listcant = []
            listdes = []
            listpu = []
            listex = []
            cont = 0
            
            delreg = AsientoHaberDetalle.objects.filter(asiento=nro_mod).distinct()
            if delreg.count()>0:
                for z in delreg:
                    z.delete()
            
            for i in range(1, 11):
                if 'cant'+str(i) in request.GET and request.GET['cant'+str(i)]:
                    listcant.append(request.GET['cant'+str(i)])
                    cont = cont + 1
                else:
                    listcant.append('0')
                if 'des'+str(i) in request.GET and request.GET['des'+str(i)]:
                    listdes.append(request.GET['des'+str(i)])
                else:
                    listdes.append('0')
                if 'pu'+str(i) in request.GET and request.GET['pu'+str(i)]:
                    listpu.append(request.GET['pu'+str(i)])
                else:
                    listpu.append('0')
                if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                    listex.append(request.GET['ex'+str(i)])
                else:
                    listex.append('0')
                
            summonto = 0
            for i in range(0, 10):
                if listdes[i] != '0':
                    newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id = int(listdes[i]), monto = float(listex[i]))
                    newventaasiento.save()
                    summonto = summonto + float(listex[i])
            #summonto = reduce(sumar, listex)
            #Cambiar a "Caja"
            id_de_cuenta = CuentaNivel3.objects.get(nombre="Caja")
            #cue = id_de_cuenta.count()
            newventaasiento = AsientoDebeDetalle.objects.get(asiento = nro_mod)
            newventaasiento.cuenta_id = id_de_cuenta.id
            newventaasiento.monto = summonto
            #newventaasiento = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id =id_de_cuenta.id, monto = summonto)
            newventaasiento.save()
            nuevoidasiento = Venta.objects.get(id=newingreso.id)
            nuevoidasiento.asiento_id = newasiento.id
            nuevoidasiento.save()
            #return render_to_response('ingresos/carga_ingreso.html')
            #Ventas.objects.get(id=request.GET['ap']).delete()
            #return HttpResponseRedirect('/carga_ingresos/')
            #apo = Aportante.objects.all().order_by("id")

            con = CuentaNivel3.objects.all().order_by("id")
            return HttpResponseRedirect('/obispado/ingresos_list/')
            #return render_to_response('ingresos/lista.html', {'apo': apo, 'con':con, 'msj': 'Ingreso Agregado Correctamente','button': 'Enviar'})
            #return render_to_response('ingresos/carga_ingreso.html', {'msj': fechaiso})
            #return render_to_response('ingresos/index.html', {'final': summonto})
        else:
            #apo = Aportante.objects.all().order_by("id")
            con = CuentaNivel3.objects.all().order_by("id")
            return render_to_response('ingresos/carga_ingreso.html', {'nombreuser': tipouser.username,'apo': apo, 'con':listcuentas,'button': 'Enviar'})
        #return render_to_response('ingresos/carga_ingreso.html',{'button': 'Editar'})
        return HttpResponseRedirect('/obispado/ingresos_list/')
    else:
        return HttpResponseRedirect('/obispado/login/')
    
#list y add
def carga_ingresos(request):
    return render_to_response('ingresos/carga_ingreso.html')

def list_ingresos(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        #valormaximo = Venta.objects.all()
        #valpesmax = valormaximo.count()
        valormaximo = Venta.objects.aggregate(Max('id'))
        valpesmax = valormaximo['id__max']
        listatot = []
        fact = ""
        fecha = ""
        fec = ""
        ap = ""
        fe = ""
        nro_fac = ""
        fechaiso=""
        filtro = 0
        if 'ap' in request.GET and request.GET['ap']:
            ap = request.GET['ap']
        if 'date1xx' in request.GET and request.GET['date1xx']:
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
        if 'nrofac' in request.GET and request.GET['nrofac']:
            nro_fac = request.GET['nrofac']
            
        #des = User.objects.filter(de)
        if ap:
            filtro =1
        if fe:
            filtro =1
        if nro_fac:
            filtro =1
        
        if valpesmax == 0 or valpesmax == None:
            return render_to_response('ingresos/lista.html', {'nombreuser': tipouser.username,'msj':'No hay ingresos'})
            
        #if valpesmax > 50 and not filtro:
        #    valpesmax = 50
            
        if not filtro:
            for i in range(1, int(valpesmax)+1):
                idv = Venta.objects.filter(id=i)
                if idv.count()>0:
                    idventa = Venta.objects.get(id=i)
                    apor = Aportante.objects.get(id=int(idventa.aportante_id))
                    listhd = AsientoHaberDetalle.objects.filter(asiento=idventa.asiento_id).distinct()
                    if listhd.count()>0:
                        for z in listhd:
                            cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                            fact = idventa.tipo_comprobante
                            if fact == "f":
                                fact = "Factura"
                            elif fact == "r":
                                fact = "Recibo"
                            fecha = idventa.fecha.timetuple()
                            fec = time.strftime("%d/%m/%Y", fecha)
                            listatot.append({"id":z.asiento_id, "fecha":fec, "aportante":apor.nombre,"nro_fac":idventa.numero_factura,"tipo_doc":fact,"cuenta":cue.nombre,"monto":int(z.monto)})
        else:
            i=0
            bp = ""
            if ap:
                bp = Q(aportante=ap)
            if fe:
                if bp:
                    bp = bp & Q(fecha = fechaiso)
                else:
                    bp = Q(fecha = fechaiso)
            if nro_fac:
                if bp:
                    bp = bp & Q(numero_factura=nro_fac)
                else:
                    bp = Q(numero_factura=nro_fac)
            #bp = Q(aportante=ap) & Q(fecha = fechaiso) & Q(numero_factura=nro_fac)
            idv = Venta.objects.filter(bp)
            if idv.count()>0:
                for i in idv:
                    apor = Aportante.objects.get(id=int(i.aportante_id))
                    listhd = AsientoHaberDetalle.objects.filter(asiento__exact=i.asiento_id).distinct()
                    if listhd.count()>0:
                        for z in listhd:
                            cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                            fact = i.tipo_comprobante
                            if fact == "f":
                                fact = "Factura"
                            elif fact == "r":
                                fact = "Recibo"
                            fecha = i.fecha.timetuple()
                            fec = time.strftime("%d/%m/%Y", fecha)
                            listatot.append({"id":i.asiento_id, "fecha":fec, "aportante":apor.nombre,"nro_fac":i.numero_factura,"tipo_doc":fact,"cuenta":cue.nombre,"monto":int(z.monto)})
                    #i = i + 1
        paginator = Paginator(listatot, 25)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            contacts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            contacts = paginator.page(paginator.num_pages)

        apo = Aportante.objects.all().order_by("id")
        return render_to_response('ingresos/lista.html', {'nombreuser': tipouser.username,'apo': apo,'ltot':contacts,'cant': valpesmax})
    else:
        return HttpResponseRedirect('/obispado/login/')

def solicitar_planilla_ingresos(request):
    '''Solo muestra el template para pedir el csv'''
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        return render_to_response('ingresos/solicitar_planilla_ingresos.html', {'nombreuser': tipouser.username})
    else:
        return HttpResponseRedirect('/obispado/login/')

def generar_planilla_csv_ingresos(request):
    '''Genera el csv, pero usa un metodo del modelo'''
    # dp vemos el parseo de fechas con Lore "javascript html css" Figueredo
    # mientras esto para probar
    #print 'funciona?'
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        fechaini = request.GET['date1xx']
        fechafin = request.GET['date1xx1']
        fechaini1 = time.strptime(str(fechaini), "%d/%m/%Y")
        fechaisoini = time.strftime("%Y-%m-%d", fechaini1)
        fechaini2 = time.strptime(str(fechafin), "%d/%m/%Y")
        fechaisofin = time.strftime("%Y-%m-%d", fechaini2)
        #fecha_inicio = date(2010, 1, 31) # quitar dp
        #fecha_fin = date.today() # quitar dp
        # aqui pedimos los datos del ingreso
        datos_ingresos = generar_resumen_ingresos(fechaisoini, fechaisofin)

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        # en el filename tal vez podriamos poner la fecha_inicio fecha_fin como parte del nombre
        response['Content-Disposition'] = 'attachment; filename=planila_ingresos.csv'

        writer = csv.writer(response, delimiter=';')
        
        writer.writerow(['', '', 'ingresos']) # titulo
        # le dejo muchas lineas en blanco para que escriban lo que quieran
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        # escribimos las columnas
        writer.writerow(['', '', 'Numero', 'Fecha', 'Tipo', 'Identificador RUC o C.I.', 'Nombre del Aportante', 'Concepto', 'Cantidad', 'Tipo', 'Total Iva Incluido', 'Total exentas', 'Gravadas 10%', 'Gravadas 5%'])
        for ingreso in datos_ingresos:
            writer.writerow(['', '', str(ingreso['nro_factura']), str(ingreso['fecha']), str(ingreso['tipo']), str(ingreso['id_ruc']), str(ingreso['nombre_aportante']), str(ingreso['concepto']), str(ingreso['cantidad']), str(ingreso['tipo_bien']), int(ingreso['total_iva_incluido']), int(ingreso['total_exentas']), '', ''])

        return response
    else:
        return HttpResponseRedirect('/obispado/login/')