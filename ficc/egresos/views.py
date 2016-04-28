# Create your views here.
from django.shortcuts import render_to_response
from obispado.egresos.models import *
from obispado.proveedores.models import *
from obispado.libros_contables.models import *
from obispado.plan_de_cuentas.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q, Max, Min
import datetime, string
import time
from datetime import date
import csv
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def sumar(x, y):
    return x + y

def carga(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        listcuentas = []
        n1 = CuentaNivel1.objects.filter(tipo__nombre__icontains="Egreso").order_by("id")
        for i in n1:
            n2 = CuentaNivel2.objects.filter(tipo = i.id).order_by("id")
            if n2.count()>0:
                for z in n2:
                    #listcuentas
                    n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id").order_by("id")
                    if n3.count()>0:
                        for y in n3:
                            listcuentas.append({"id":y.id, "nombre":y.nombre, "tipo_de_iva":str(y.tipo_de_iva)})
        prov = Proveedor.objects.all().order_by("id")
        #con = CuentaNivel3.objects.all().order_by("id")
        if 'pro' in request.GET and request.GET['pro']:
            pro = request.GET['pro']
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
            if 'ruc' in request.GET and request.GET['ruc']:
                ruc = request.GET['ruc']
            nrofac = request.GET['nrofac']
            if 'tot' in request.GET and request.GET['tot']:
                tot = request.GET['tot']
            tipodoc = request.GET['tipodoc']
            #else:
            #    tot = 1000
            
            verfac = Compra.objects.filter(numero_comprobante=nrofac)
            if verfac.count()>0:
                return render_to_response('egresos/carga_egreso.html', {'nombreuser': tipouser.username,'pro': prov, 'con':listcuentas, 'msj': 'Ya existe ese numero de documento'})
                #return request
            
            id_proveedor = Proveedor.objects.filter(nombre=pro)
            valormaximo = Proveedor.objects.aggregate(Max('id'))
            valapmax = valormaximo['id__max']
            if valapmax:
                valapmax = valapmax + 1
            else:
                valapmax = 1
            newasiento = AsientoContable(fecha = fechaiso)
            newasiento.save()
            tipo_doc_str = ''
            if tipodoc == '1':
                tipo_doc_str = 'f'
            elif tipodoc == '2':
                tipo_doc_str = 'r'
            elif tipodoc == '3':
                tipo_doc_str = 'a'
            newingreso = Compra(fecha = fechaiso, proveedor_id = pro, numero_comprobante = nrofac, asiento = newasiento, tipo_comprobante=tipo_doc_str)
            newingreso.save()
            #newasiento.comentario = "egreso: " + str(newingreso.id))
            #newasiento.save()
            listcant = []
            listdes = []
            listpu = []
            lismon = []
            totiva = []
            g10 = []
            g5 = []
            listex = []
            cont = 0
            pos=-1
            for i in range(1, 51):
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
                if 'mon'+str(i) in request.GET and request.GET['mon'+str(i)]:
                    lismon.append(request.GET['mon'+str(i)])
                else:
                    lismon.append('0')
                if 'totiva'+str(i) in request.GET and request.GET['totiva'+str(i)]:
                    totiva.append(request.GET['totiva'+str(i)])
                else:
                    totiva.append('0')
                if 'g10'+str(i) in request.GET and request.GET['g10'+str(i)]:
                    g10.append(request.GET['g10'+str(i)])
                else:
                    g10.append('0')
                if 'g5'+str(i) in request.GET and request.GET['g5'+str(i)]:
                    g5.append(request.GET['g5'+str(i)])
                else:
                    g5.append('0')
                if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                    listex.append(request.GET['ex'+str(i)])
                else:
                    listex.append('0')
            totivat = 0
            totgv10 = 0
            totgv5 = 0
            totex = 0
            totgral = 0
            if 'totivah' in request.GET and request.GET['totivah']:
                totivat = request.GET['totivah']
            if 'totgv10h' in request.GET and request.GET['totgv10h']:
                totgv10 = request.GET['totgv10h']
            if 'totgv5h' in request.GET and request.GET['totgv5h']:
                totgv5 = request.GET['totgv5h']
            if 'totexh' in request.GET and request.GET['totexh']:
                totex = request.GET['totexh']
            #if 'totgralh' in request.GET and request.GET['totgralh']:
            totgral = request.GET['totgralh']
            #else:
            #    totgral = 555;
            listipos = []
            
            for i in range(0, 50):
                if listdes[i] != "0":
                    tipos_iva = CuentaNivel3.objects.get(id=listdes[i])
                    if(tipos_iva.tipo_de_iva == 'd'):
                        listipos.append('d')
                    if(tipos_iva.tipo_de_iva == 'c'):
                        listipos.append('c')
                    if(tipos_iva.tipo_de_iva == 'e' or tipos_iva.tipo_de_iva == 'n'):
                        listipos.append('e')
                else:
                    listipos.append('0')
            summonto = 0
            for i in range(0, 50):
                if listdes[i] != "0":
                    if(listipos[i] == 'd'):
                        # traemos la cuenta iva 10 %
                        cuenta_iva = CuentaNivel3.objects.get(nombre="IVA 10% Credito")
                        # cargamos la gravada
                        newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = g10[i])
                        newventaasiento.save()
                        # calculamos el iva y cargamos
                        monto_iva = float(totiva[i]) - float(g10[i])
                        newivadebe = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(cuenta_iva.id), monto = monto_iva)
                        newivadebe.save()
                    elif(listipos[i] == 'c'):
                        # traemos la cuenta iva 5 %
                        cuenta_iva = CuentaNivel3.objects.get(nombre="IVA 5% Credito")
                        # cargamos la gravada
                        newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = g5[i])
                        newventaasiento.save()
                        # calculamos el iva y cargamos
                        monto_iva = float(totiva[i]) - float(g5[i])
                        newivadebe = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(cuenta_iva.id), monto = monto_iva)
                        newivadebe.save()
                    elif(listipos[i] == 'e' or tipos_iva.tipo_de_iva == 'n'):
                        newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = listex[i])
                        newventaasiento.save()
                    
                # = summonto + int(listex[i])
            summonto = reduce(sumar, listex)
            #Cambiar a "Caja"
            id_de_cuenta = CuentaNivel3.objects.get(nombre="Caja")
            newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =id_de_cuenta.id, monto = float(totgral))
            #newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =1, monto = int(totgral))
            newventaasiento.save()
            nuevoidasiento = Compra.objects.get(id=newingreso.id)
            nuevoidasiento.asiento_id = newasiento.id
            nuevoidasiento.save()
            #return render_to_response('ingresos/carga_ingreso.html')
            #return HttpResponseRedirect('/carga_ingresos/')
            #return render_to_response('egresos/carga_egreso.html')
            #pro = Proveedor.objects.all().order_by("id")
            #con = CuentaNivel3.objects.all().order_by("id")
            
            fecha = time.strptime(str(date.today()), "%Y-%m-%d")
            #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
            path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
            archivo = open(path, "a")
            escribir = "El usuario " + tipouser.username + " cargo el egreso del documento nro "+str(nrofac)+" el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
            archivo.write(escribir)
            archivo.close()
            return render_to_response('egresos/carga_egreso.html', {'nombreuser': tipouser.username, 'pro': prov, 'con':listcuentas, 'msj': 'Egreso Agregado Correctamente'})
            #return render_to_response('principal/index.html', {'final': listex})
            #return HttpResponseRedirect('/carga_egresos/')
        else:
            #de = CuentaNivel1.objects.get(nombre__icontains="Egresos")
            #pro = Proveedor.objects.all().order_by("id")
            con = CuentaNivel3.objects.all().order_by("id")
            listf = []
            for i in range(11, 51):
                listf.append(i)
            return render_to_response('egresos/carga_egreso.html', {'nombreuser': tipouser.username,'pro': prov, 'con':listcuentas, 'listf':listf})
        return render_to_response('egresos/carga_egreso.html')
    else:
        return HttpResponseRedirect('/obispado/login/')

def list_egresos(request):
    #valormaximo = Venta.objects.all()
    #valpesmax = valormaximo.count()
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        valormaximo = Compra.objects.aggregate(Max('id'))
        valpesmax = valormaximo['id__max']
        listatot = []
        fact = ""
        fecha = ""
        fec = ""
        pro = ""
        fe = ""
        nro_fac = ""
        fechaiso=""
        filtro = 0
        montof = 0
        montoivad = 0
        montoivac = 0
        if 'pro' in request.GET and request.GET['pro']:
            pro = request.GET['pro']
        if 'date1xx' in request.GET and request.GET['date1xx']:
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
        if 'nrofac' in request.GET and request.GET['nrofac']:
            nro_fac = request.GET['nrofac']
            
        #des = User.objects.filter(de)
        if pro:
            filtro =1
        if fe:
            filtro =1
        if nro_fac:
            filtro =1
        
        if valpesmax == 0 or valpesmax == None:
            return render_to_response('egresos/lista.html', {'nombreuser': tipouser.username,'msj':'No hay egresos'})
            
        #if valpesmax > 50 and not filtro:
        #    valpesmax = 50    
        cuenta_iva10 = CuentaNivel3.objects.get(nombre="IVA 10% Credito")
        cuenta_iva5 = CuentaNivel3.objects.get(nombre="IVA 5% Credito")
        if not filtro:
            for i in range(1, int(valpesmax)+1):
                idv = Compra.objects.filter(id=i)
                if idv.count()>0:
                    idcompra = Compra.objects.get(id=i)
                    prov = Proveedor.objects.get(id=int(idcompra.proveedor_id))
                    listhd = AsientoDebeDetalle.objects.filter(asiento=idcompra.asiento_id).distinct()
                    if listhd.count()>0:
                        for z in range (0, listhd.count()):
                            if listhd[z].cuenta_id <> cuenta_iva10.id and listhd[z].cuenta_id <> cuenta_iva5.id:
                                cue = CuentaNivel3.objects.get(id=int(listhd[z].cuenta_id))
                                fact = idcompra.tipo_comprobante
                                if fact == "f":
                                    fact = "Factura"
                                elif fact == "r":
                                    fact = "Recibo"
                                elif fact == "a":
                                    fact = "Autofactura"
                                fecha = idcompra.fecha.timetuple()
                                fec = time.strftime("%d/%m/%Y", fecha)
                                if(cue.tipo_de_iva == 'd'):
                                    montoivad = listhd[z].monto * 0.100
                                    montoivad = round(montoivad, 0)
                                    montof = int(montoivad) + int(listhd[z].monto)
                                elif (cue.tipo_de_iva == 'c'):
                                    montoivac = listhd[z].monto * 0.05
                                    montoivac = round(montoivac, 0)
                                    montof = int(montoivac) + int(listhd[z].monto)
                                else:
                                    montof = listhd[z].monto
                                listatot.append({"id":listhd[z].asiento_id, "fecha":fec, "proveedor":prov.nombre,"nro_fac":idcompra.numero_comprobante,"tipo_doc":fact,"cuenta":cue.nombre,"monto":int(montof)})
        else:
            i=0
            bp = ""
            if pro:
                bp = Q(proveedor=pro)
            if fe:
                if bp:
                    bp = bp & Q(fecha = fechaiso)
                else:
                    bp = Q(fecha = fechaiso)
            if nro_fac:
                if bp:
                    bp = bp & Q(numero_comprobante=nro_fac)
                else:
                    bp = Q(numero_comprobante=nro_fac)
            #bp = Q(proveedor=pro) & Q(fecha = fechaiso) & Q(numero_comprobante=nro_fac)
            idv = Compra.objects.filter(bp)
            if idv.count()>0:
                for i in idv:
                    prov = Proveedor.objects.get(id=int(i.proveedor_id))
                    listhd = AsientoDebeDetalle.objects.filter(asiento__exact=i.asiento_id).distinct()
                    if listhd.count()>0:
                        for z in listhd:
                            if z.cuenta_id <> cuenta_iva10.id and z.cuenta_id <> cuenta_iva5.id:
                                cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                                fact = i.tipo_comprobante
                                if fact == "f":
                                    fact = "Factura"
                                elif fact == "r":
                                    fact = "Recibo"
                                elif fact == "a":
                                    fact = "Autofactura"
                                fecha = i.fecha.timetuple()
                                fec = time.strftime("%d/%m/%Y", fecha)
                                if(cue.tipo_de_iva == 'd'):
                                    montoivad = z.monto * 0.100
                                    montoivad = round(montoivad, 0)
                                    montof = int(montoivad) + int(z.monto)
                                elif (cue.tipo_de_iva == 'c'):
                                    montoivac = z.monto * 0.05
                                    montoivac = round(montoivac, 0)
                                    montof = int(montoivac) + int(z.monto)
                                else:
                                    montof = int(z.monto)
                                listatot.append({"id":i.asiento_id, "fecha":fec, "proveedor":prov.nombre,"nro_fac":i.numero_comprobante,"tipo_doc":fact,"cuenta":cue.nombre,"monto":montof})
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
        pro = Proveedor.objects.all().order_by("id")
        return render_to_response('egresos/lista.html', {'nombreuser': tipouser.username,'pro': pro,'ltot':contacts,'cant': valpesmax})
    else:
        return HttpResponseRedirect('/obispado/login/')

def edit_egresos(request, e_id):
    listatot = []
    listf = []
    fact = ""
    fec = ""
    montof = 0
    montoivad = 0
    montoivac = 0
    cont_real = 0
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        listcuentas = []
        n1 = CuentaNivel1.objects.filter(tipo__nombre__icontains="Egreso").order_by("id")
        for i in n1:
            n2 = CuentaNivel2.objects.filter(tipo = i.id).order_by("id")
            if n2.count()>0:
                for z in n2:
                    #listcuentas
                    n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id").order_by("id")
                    if n3.count()>0:
                        for y in n3:
                            listcuentas.append({"id":y.id, "nombre":y.nombre, "tipo_de_iva":str(y.tipo_de_iva)})
        pro = Proveedor.objects.all().order_by("id")
        if e_id:
            idventa = Compra.objects.filter(asiento=e_id)
            cuenta_iva10 = CuentaNivel3.objects.get(nombre="IVA 10% Credito")
            cuenta_iva5 = CuentaNivel3.objects.get(nombre="IVA 5% Credito")
            if idventa.count()>0:
                listhd = AsientoDebeDetalle.objects.filter(asiento=e_id).distinct()
                idcompra = Compra.objects.get(asiento=e_id)
                prov = Proveedor.objects.get(id=int(idcompra.proveedor_id))
                if listhd.count()>0:
                    for z in listhd:
                        if z.cuenta_id <> cuenta_iva10.id and z.cuenta_id <> cuenta_iva5.id:
                            cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                            fact = idcompra.tipo_comprobante
                            if fact == "f":
                                fact = "Factura"
                            elif fact == "r":
                                fact = "Recibo"
                            elif fact == "a":
                                fact = "Autofactura"
                            fecha = idcompra.fecha.timetuple()
                            fec = time.strftime("%d/%m/%Y", fecha)
                            if(cue.tipo_de_iva == 'd'):
                                montoivad = z.monto * 0.100
                                montoivad = round(montoivad, 0)
                                montof = int(montoivad) + int(z.monto)
                            elif (cue.tipo_de_iva == 'c'):
                                montoivac = z.monto * 0.05
                                montoivac = round(montoivac, 0)
                                montof = int(montoivac) + int(z.monto)
                            else:
                                montof = int(z.monto)
                            listatot.append({"id":z.asiento_id, "fecha":fec, "proveedor":prov.nombre,"nro_fac":idcompra.numero_comprobante,"tipo_doc":fact,"cuenta":cue.id,"monto":int(montof),"tipoiva":cue.tipo_de_iva})
                            cont_real = cont_real + 1
                cantfalta = 50 - int(cont_real)
                desde =int(cont_real) + 1
                for i in range(0, cantfalta):
                    listf.append(i+int(desde))
                listresto = []
                for i in range(11, 51):
                    listresto.append(i)
                #pro = Proveedor.objects.all().order_by("id")
                #con = CuentaNivel3.objects.all().order_by("id")
                #venta_edit = Venta.objects.get(asiento=id)
                return render_to_response('egresos/edit_egreso.html',{'nombreuser': tipouser.username,'pro': pro, 'con':listcuentas,'ltot':listatot, 'idpro':prov.id, 'rucval':prov.ruc, 'feval':fec, 'tipo_doc':fact, 'nro_fact':idcompra.numero_comprobante, 'cantval':cont_real, 'cantfalta':cantfalta, 'desde':desde, 'listf':listf, 'nro':e_id, 'listresto':listresto} )
            else:
                return HttpResponseRedirect('/obispado/egresos_list/')
        else:
            return HttpResponseRedirect('/obispado/egresos_list/')
        return HttpResponseRedirect('/obispado/egresos_list/')
    else:
        return HttpResponseRedirect('/obispado/login/')
    
def update_egresos(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        listcuentas = []
        n1 = CuentaNivel1.objects.filter(tipo__nombre__icontains="Egreso").order_by("id")
        for i in n1:
            n2 = CuentaNivel2.objects.filter(tipo = i.id).order_by("id")
            if n2.count()>0:
                for z in n2:
                    #listcuentas
                    n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id").order_by("id")
                    if n3.count()>0:
                        for y in n3:
                            listcuentas.append({"id":y.id, "nombre":y.nombre, "tipo_de_iva":str(y.tipo_de_iva)})
        prov = Proveedor.objects.all().order_by("id")
        if 'pro' in request.GET and request.GET['pro']:
            pro = request.GET['pro']
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
            if 'ruc' in request.GET and request.GET['ruc']:
                ruc = request.GET['ruc']
            nrofac = request.GET['nrofac']
            if 'tot' in request.GET and request.GET['tot']:
                tot = request.GET['tot']
            tipodoc = request.GET['tipodoc']
            nro_mod = request.GET['nro_mod']
            #else:
            #    tot = 1000
                
            #id_proveedor = Proveedor.objects.filter(nombre=pro)
            valormaximo = Proveedor.objects.aggregate(Max('id'))
            valapmax = valormaximo['id__max']
            if valapmax:
                valapmax = valapmax + 1
            else:
                valapmax = 1
            newasiento = AsientoContable.objects.get(id = nro_mod)
            newingreso = Compra.objects.get(asiento=nro_mod)
            fecha = time.strptime(str(date.today()), "%Y-%m-%d")
            #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
            path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
            archivo = open(path, "a")
            escribir = "El usuario " + tipouser.username + " ha modificado el egreso con numero de documento: "+str(newingreso.numero_comprobante)+ " el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
            archivo.write(escribir)
            if int(newingreso.numero_comprobante) != int(nrofac):
                escribir = "El usuario " + tipouser.username + " ha cambiado el numero de factura de egreso: de "+str(newingreso.numero_comprobante)+ " a "+ str(nrofac) +" el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
                archivo.write(escribir)

            archivo.close()
            
            #newasiento = AsientoContable(fecha = fechaiso)
            newasiento.fecha = fechaiso
            newasiento.save()
            tipo_doc_str = ''
            if tipodoc == '1':
                tipo_doc_str = 'f'
            elif tipodoc == '2':
                tipo_doc_str = 'r'
            elif tipodoc == '3':
                tipo_doc_str = 'a'
            newingreso = Compra.objects.get(asiento=nro_mod)
            verfac = Compra.objects.filter(numero_comprobante=nrofac)
            if verfac.count()>0 and verfac[0].numero_comprobante != newingreso.numero_comprobante:
                return render_to_response('egresos/carga_egreso.html', {'pro': prov, 'con':listcuentas, 'msj': 'Ya existe otro documento con ese numero.','button': 'Enviar', 'at': 'Ya existe otro documento con ese numero.'})    
            
            newingreso.fecha = fechaiso
            newingreso.proveedor_id = pro
            newingreso.numero_comprobante = nrofac
            newingreso.tipo_comprobante=tipo_doc_str
            #newingreso = Compra(fecha = fechaiso, proveedor_id = pro, numero_comprobante = nrofac, asiento = newasiento, tipo_comprobante=tipo_doc_str)
            newingreso.save()
            #newasiento.comentario = "egreso: " + str(newingreso.id))
            #newasiento.save()
            listcant = []
            listdes = []
            listpu = []
            lismon = []
            totiva = []
            g10 = []
            g5 = []
            listex = []
            cont = 0
            pos=-1
            
            delreg = AsientoDebeDetalle.objects.filter(asiento=nro_mod).distinct()
            if delreg.count()>0:
                for z in delreg:
                    z.delete()
            
            for i in range(1, 51):
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
                if 'mon'+str(i) in request.GET and request.GET['mon'+str(i)]:
                    lismon.append(request.GET['mon'+str(i)])
                else:
                    lismon.append('0')
                if 'totiva'+str(i) in request.GET and request.GET['totiva'+str(i)]:
                    totiva.append(request.GET['totiva'+str(i)])
                else:
                    totiva.append('0')
                if 'g10'+str(i) in request.GET and request.GET['g10'+str(i)]:
                    g10.append(request.GET['g10'+str(i)])
                else:
                    g10.append('0')
                if 'g5'+str(i) in request.GET and request.GET['g5'+str(i)]:
                    g5.append(request.GET['g5'+str(i)])
                else:
                    g5.append('0')
                if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                    listex.append(request.GET['ex'+str(i)])
                else:
                    listex.append('0')
            totivat = 0
            totgv10 = 0
            totgv5 = 0
            totex = 0
            totgral = 0
            if 'totivah' in request.GET and request.GET['totivah']:
                totivat = request.GET['totivah']
            if 'totgv10h' in request.GET and request.GET['totgv10h']:
                totgv10 = request.GET['totgv10h']
            if 'totgv5h' in request.GET and request.GET['totgv5h']:
                totgv5 = request.GET['totgv5h']
            if 'totexh' in request.GET and request.GET['totexh']:
                totex = request.GET['totexh']
            #if 'totgralh' in request.GET and request.GET['totgralh']:
            totgral = request.GET['totgralh']
            #else:
            #    totgral = 555;
            listipos = []
            
            for i in range(0, 50):
                if listdes[i] != '0':
                    tipos_iva = CuentaNivel3.objects.get(id=listdes[i])
                    if(tipos_iva.tipo_de_iva == 'd'):
                        listipos.append('d')
                    if(tipos_iva.tipo_de_iva == 'c'):
                        listipos.append('c')
                    if(tipos_iva.tipo_de_iva == 'e' or tipos_iva.tipo_de_iva == 'n'):
                        listipos.append('e')
                else:
                    listipos.append('0')
            summonto = 0
            for i in range(0, 50):
                if listdes[i] != '0':
                    if(listipos[i] == 'd'):
                        # traemos la cuenta iva 10 %
                        cuenta_iva = CuentaNivel3.objects.get(nombre="IVA 10% Credito")
                        # cargamos la gravada
                        newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = g10[i])
                        newventaasiento.save()
                        # calculamos el iva y cargamos
                        monto_iva = float(totiva[i]) - float(g10[i])
                        newivadebe = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(cuenta_iva.id), monto = monto_iva)
                        newivadebe.save()
                    elif(listipos[i] == 'c'):
                        # traemos la cuenta iva 5 %
                        cuenta_iva = CuentaNivel3.objects.get(nombre="IVA 5% Credito")
                        # cargamos la gravada
                        newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = g5[i])
                        newventaasiento.save()
                        # calculamos el iva y cargamos
                        monto_iva = float(totiva[i]) - float(g5[i])
                        newivadebe = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(cuenta_iva.id), monto = monto_iva)
                        newivadebe.save()
                    elif(listipos[i] == 'e' or tipos_iva.tipo_de_iva == 'n'):
                        newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = listex[i])
                        newventaasiento.save()
                
                # = summonto + int(listex[i])
            #summonto = reduce(sumar, listex)
            #Cambiar a "Caja"
            id_de_cuenta = CuentaNivel3.objects.get(nombre="Caja")
            #newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =id_de_cuenta.id, monto = float(totgral))
            
            newventaasiento = AsientoHaberDetalle.objects.get(asiento=nro_mod)
            newventaasiento.cuenta_id = id_de_cuenta.id
            newventaasiento.monto = float(totgral)
            
            #newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =1, monto = int(totgral))
            newventaasiento.save()
            
            nuevoidasiento = Compra.objects.get(id=newingreso.id)
            nuevoidasiento.asiento_id = newasiento.id
            nuevoidasiento.save()
            #return render_to_response('ingresos/carga_ingreso.html')
            #return HttpResponseRedirect('/carga_ingresos/')
            #return render_to_response('egresos/carga_egreso.html')
            #pro = Proveedor.objects.all().order_by("id")
            #con = CuentaNivel3.objects.all().order_by("id")
            #return render_to_response('egresos/carga_egreso.html', {'pro': pro, 'con':con, 'msj': 'Egreso Agregado Correctamente'})
            return HttpResponseRedirect('/obispado/egresos_list/')
            #return render_to_response('principal/index.html', {'final': listex})
            #return HttpResponseRedirect('/carga_egresos/')
        else:
            #de = CuentaNivel1.objects.get(nombre__contains="Egresos")
            #pro = Proveedor.objects.all().order_by("id")
            #con = CuentaNivel3.objects.all().order_by("id")
            return render_to_response('egresos/carga_egreso.html', {'nombreuser': tipouser.username,'pro': prov, 'con':listcuentas})
        return HttpResponseRedirect('/obispado/egresos_list/')
    else:
        return HttpResponseRedirect('/obispado/login/')
    
def solicitar_planilla_egresos(request):
    '''Solo muestra el template para pedir el csv'''
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        return render_to_response('egresos/solicitar_planilla_egresos.html', {'nombreuser': tipouser.username})
    else:
        return HttpResponseRedirect('/obispado/login/')

def generar_planilla_csv_egresos(request):
    '''Genera el csv, pero usa un metodo del modelo'''
    # dp vemos el parseo de fechas con Lore "javascript html css" Figueredo
    # mientras esto para probar
    #print 'funciona?'
    #print request.GET['fecha_inicio']
    #print request.GET['fecha_fin']
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        #tipouser = User.objects.get(id=user_id)
        fechaini = request.GET['date1xx']
        fechafin = request.GET['date1xx1']
        fechaini1 = time.strptime(str(fechaini), "%d/%m/%Y")
        fechaisoini = time.strftime("%Y-%m-%d", fechaini1)
        fechaini2 = time.strptime(str(fechafin), "%d/%m/%Y")
        fechaisofin = time.strftime("%Y-%m-%d", fechaini2)
        #fecha_inicio = date(2010, 1, 31) # quitar dp
        #fecha_fin = date.today() # quitar dp
        # aqui pedimos los datos del egreso
        datos_egresos = generar_resumen_egresos(fechaisoini, fechaisofin)

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=planila_egresos.csv'

        writer = csv.writer(response, delimiter=';')
        
        writer.writerow(['', '', 'Egresos']) # titulo
        # le dejo muchas lineas en blanco para que escriban lo que quieran
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        writer.writerow([]) # linea en blanco
        # escribimos las columnas
        writer.writerow(['', '', 'Numero', 'Fecha', 'Tipo', 'Identificador RUC o C.I.', 'Nombre del Proveedor', 'Gravadas 10%', 'Gravadas 5%', 'Exentas', 'Total Iva Incluido', 'Tasa 10%', 'Tasa 5%'])
        for egreso in datos_egresos:
            writer.writerow(['', '', str(egreso['nro_comprobante']), str(egreso['fecha']), str(egreso['tipo_comprobante']), str(egreso['ruc_proveedor']), str(egreso['proveedor']), int(egreso['gravadas10']), int(egreso['gravadas5']), int(egreso['exentas']), int(egreso['total']), int(egreso['iva10']), int(egreso['iva5'])])
        
        return response
    else:
        return HttpResponseRedirect('/obispado/login/')