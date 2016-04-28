# Create your views here.
from django.shortcuts import render_to_response
from obispado.egresos.models import *
from obispado.ingresos.models import *
from obispado.proveedores.models import *
from obispado.plan_de_cuentas.models import *
from obispado.aportantes.models import *
from obispado.libros_contables.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q, Max, Min
import datetime, string
import time
from datetime import date
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def cargar_asiento(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        listcuentasd = []
        listcuentash = []
        tc = TipoCuenta.objects.filter(tipo_de_saldo='d')
        if tc.count()>0:
            for x in tc:
                n1 = CuentaNivel1.objects.filter(tipo=x.id)
                for y in n1:
                    n2 = CuentaNivel2.objects.filter(tipo = y.id)
                    for z in n2:
                        n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id")
                        if n3.count()>0:
                            for a in n3:
                                listcuentasd.append({"id":a.id, "nombre":a.nombre})
                        
        tc = TipoCuenta.objects.filter(tipo_de_saldo='h')
        if tc.count()>0:
            for x in tc:
                n1 = CuentaNivel1.objects.filter(tipo=x.id)
                for y in n1:
                    n2 = CuentaNivel2.objects.filter(tipo = y.id)
                    for z in n2:
                        n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id")
                        if n3.count()>0:
                            for a in n3:
                                listcuentash.append({"id":a.id, "nombre":a.nombre})
        tipouser = User.objects.get(id=user_id)
        if 'date1xx' in request.GET and request.GET['date1xx']:
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
            com = request.GET['comentarios']
            cuentad=[]
            cuentah=[]
            montod=[]
            montoh=[]
            newasiento = AsientoContable(fecha = fechaiso, comentario = str(com))
            newasiento.save()
            cont = 0
            for i in range(1, 11):
                if 'cd'+str(i) in request.GET and request.GET['cd'+str(i)]:
                        cuentad.append(request.GET['cd'+str(i)])
                        cont = cont + 1
                if 'd'+str(i) in request.GET and request.GET['d'+str(i)]:
                        montod.append(request.GET['d'+str(i)])
                if 'ch'+str(i) in request.GET and request.GET['ch'+str(i)]:
                        cuentah.append(request.GET['ch'+str(i)])
                if 'h'+str(i) in request.GET and request.GET['h'+str(i)]:
                        montoh.append(request.GET['h'+str(i)])
            for i in range(0, cont):
                haber = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id = int(cuentah[i]), monto = float(montoh[i]))
                haber.save()
                debe = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id = int(cuentad[i]), monto = float(montod[i]))
                debe.save()
            #cn3 = CuentaNivel3.objects.all()
            fecha = time.strptime(str(date.today()), "%Y-%m-%d")
            #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
            path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
            archivo = open(path, "a")
            escribir = "El usuario " + tipouser.username + " cargo un asiento contable el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
            archivo.write(escribir)
            archivo.close()
            return render_to_response('asiento/asiento.html', {'nombreuser': tipouser.username,'listcuentasd': listcuentasd, 'listcuentash':listcuentash, 'msj':'Asiento Cargado Correctamente'})
        else:
            #cn3 = CuentaNivel3.objects.all()
            return render_to_response('asiento/asiento.html', {'nombreuser': tipouser.username,'listcuentasd': listcuentasd, 'listcuentash':listcuentash})
        return render_to_response('asiento/asiento.html')
    else:
        return HttpResponseRedirect('/obispado/login/')
        
        
def list_asientos(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        #valormaximo = Venta.objects.all()
        #valpesmax = valormaximo.count()
        valormaximo = AsientoContable.objects.aggregate(Max('id'))
        valpesmax = valormaximo['id__max']
        listatoth = []
        listatotd = []
        listagral = []
        fact = ""
        fecha = ""
        fec = ""
        ap = ""
        fe = ""
        nro_fac = ""
        fechaiso=""
        venta=0
        compra=0
        filtro = 0
        if 'date1xx' in request.GET and request.GET['date1xx']:
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
        
        #des = User.objects.filter(de)
        if fe:
            filtro =1
        
        if valpesmax == 0 or valpesmax == None:
            return render_to_response('asiento/lista.html', {'nombreuser': tipouser.username,'msj':'No hay asientos'})
            
        #if valpesmax > 50 and not filtro:
        #    valpesmax = 50 
            
        if not filtro:
            for i in range(1, int(valpesmax)+1):
                idv = AsientoContable.objects.filter(id=i)
                if idv.count()>0:
                    idventa = AsientoContable.objects.get(id=i)
                    venta = Venta.objects.filter(asiento=idventa.id)
                    compra = Compra.objects.filter(asiento=idventa.id)
                    if(venta.count()<=0 and compra.count()<=0):
                        #apor = Aportante.objects.get(id=int(idventa.aportante_id))
                        listhd = AsientoHaberDetalle.objects.filter(asiento=idventa.id).distinct().order_by('id')
                        if listhd.count()>0:
                            for z in listhd:
                                cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                                fecha = idventa.fecha.timetuple()
                                fec = time.strftime("%d/%m/%Y", fecha)
                                listatoth.append({"id":z.asiento_id, "fecha":fec, "cuenta":cue.nombre,"monto":int(z.monto)})
            for i in range(1, int(valpesmax)+1):
                idv = AsientoContable.objects.filter(id=i)
                if idv.count()>0:
                    idventa = AsientoContable.objects.get(id=i)
                    venta = Venta.objects.filter(asiento=idventa.id)
                    compra = Compra.objects.filter(asiento=idventa.id)
                    if(venta.count()<=0 and compra.count()<=0):
                        #apor = Aportante.objects.get(id=int(idventa.aportante_id))
                        listhd = AsientoDebeDetalle.objects.filter(asiento=idventa.id).distinct().order_by('id')
                        if listhd.count()>0:
                            for z in listhd:
                                cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                                fecha = idventa.fecha.timetuple()
                                fec = time.strftime("%d/%m/%Y", fecha)
                                listatotd.append({"id":z.asiento_id, "fecha":fec, "cuenta":cue.nombre,"monto":int(z.monto)})
        else:
            i=0
            bp = ""
            if fe:
                if bp:
                    bp = bp & Q(fecha = fechaiso)
                else:
                    bp = Q(fecha = fechaiso)
            #bp = Q(aportante=ap) & Q(fecha = fechaiso) & Q(numero_factura=nro_fac)
            idv = AsientoContable.objects.filter(bp)
            if idv.count()>0:
                for i in idv:
                    #apor = Aportante.objects.get(id=int(i.aportante_id))
                    listhd = AsientoHaberDetalle.objects.filter(asiento__exact=i.id).distinct()
                    if listhd.count()>0:
                        for z in listhd:
                            venta = Venta.objects.filter(asiento=z.asiento)
                            compra = Compra.objects.filter(asiento=z.asiento)
                            if(venta.count()<=0 and compra.count()<=0):
                                cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                                fecha = i.fecha.timetuple()
                                fec = time.strftime("%d/%m/%Y", fecha)
                                listatoth.append({"id":i.id, "fecha":fec, "cuenta":cue.nombre,"monto":int(z.monto)})
                for i in idv:
                    #apor = Aportante.objects.get(id=int(i.aportante_id))
                    listhd = AsientoDebeDetalle.objects.filter(asiento__exact=i.id).distinct()
                    if listhd.count()>0:
                        for z in listhd:
                            venta = Venta.objects.filter(asiento=z.asiento)
                            compra = Compra.objects.filter(asiento=z.asiento)
                            if(venta.count()<=0 and compra.count()<=0):
                                cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                                fecha = i.fecha.timetuple()
                                fec = time.strftime("%d/%m/%Y", fecha)
                                listatotd.append({"id":i.id, "fecha":fec, "cuenta":cue.nombre,"monto":int(z.monto)})
                    #i = i + 1
                    
        #apo = Aportante.objects.all().order_by("id")
        long = len(listatotd)
        for i in range(0,long):
            listagral.append({"id":listatotd[i]['id'],"fecha":listatotd[i]['fecha'],"cuentad":listatotd[i]['cuenta'],"montod":listatotd[i]['monto'], "cuentah":listatoth[i]['cuenta'],"montoh":listatoth[i]['monto']})
        
        paginator = Paginator(listagral, 25)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            contacts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            contacts = paginator.page(paginator.num_pages)
        
        return render_to_response('asiento/lista.html', {'nombreuser': tipouser.username,'ltot':contacts,'cant': valpesmax})
    else:
        return HttpResponseRedirect('/obispado/login/')
        
def edit_asientos(request, a_id):
    listatot = []
    listatoth = []
    listatotd = []
    listagral = []
    listf = []
    fact = ""
    fec = ""
    fechaf = ""
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        listcuentasd = []
        listcuentash = []
        tc = TipoCuenta.objects.filter(tipo_de_saldo='d')
        if tc.count()>0:
            for x in tc:
                n1 = CuentaNivel1.objects.filter(tipo=x.id)
                for y in n1:
                    n2 = CuentaNivel2.objects.filter(tipo = y.id)
                    for z in n2:
                        n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id")
                        if n3.count()>0:
                            for a in n3:
                                listcuentasd.append({"id":a.id, "nombre":a.nombre})
                        
        tc = TipoCuenta.objects.filter(tipo_de_saldo='h')
        if tc.count()>0:
            for x in tc:
                n1 = CuentaNivel1.objects.filter(tipo=x.id)
                for y in n1:
                    n2 = CuentaNivel2.objects.filter(tipo = y.id)
                    for z in n2:
                        n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id")
                        if n3.count()>0:
                            for a in n3:
                                listcuentash.append({"id":a.id, "nombre":a.nombre})
        tipouser = User.objects.get(id=user_id)
        if a_id:
            idventaf = AsientoContable.objects.filter(id=a_id)
            if idventaf.count()>0:
                idventa = AsientoContable.objects.get(id=a_id)
                venta = Venta.objects.filter(asiento=idventa.id)
                compra = Compra.objects.filter(asiento=idventa.id)
                if(venta.count()<=0 and compra.count()<=0):
                    #apor = Aportante.objects.get(id=int(idventa.aportante_id))
                    listhd = AsientoHaberDetalle.objects.filter(asiento=idventa.id).distinct().order_by('id')
                    if listhd.count()>0:
                        for z in listhd:
                            cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                            fecha = idventa.fecha.timetuple()
                            fec = time.strftime("%d/%m/%Y", fecha)
                            listatoth.append({"id":z.asiento_id, "fecha":fec, "cuentah":cue.id,"montoh":int(z.monto)})
                    listhd = AsientoDebeDetalle.objects.filter(asiento=idventa.id).distinct().order_by('id')
                    if listhd.count()>0:
                        for z in listhd:
                            cue = CuentaNivel3.objects.get(id=int(z.cuenta_id))
                            fecha = idventa.fecha.timetuple()
                            fec = time.strftime("%d/%m/%Y", fecha)
                            listatotd.append({"id":z.asiento_id, "fecha":fec, "cuentad":cue.id,"montod":int(z.monto)})
            
            cantfalta = 12 - int(listhd.count())
            desde =int(listhd.count()) + 1
            for i in range(0, cantfalta):
                listf.append(i+int(desde))
            #pro = Proveedor.objects.all().order_by("id")
            #con = CuentaNivel3.objects.all().order_by("id")
            #venta_edit = Venta.objects.get(asiento=id)
            long = len(listatotd)
            for i in range(0,long):
                listagral.append({"id":listatotd[i]['id'],"fecha":listatotd[i]['fecha'],"cuentad":listatotd[i]['cuentad'],"montod":listatotd[i]['montod'], "cuentah":listatoth[i]['cuentah'],"montoh":listatoth[i]['montoh']})
            return render_to_response('asiento/edit_asiento.html',{'nombreuser': tipouser.username,'listcuentasd': listcuentasd, 'listcuentash':listcuentash, 'cantfalta':cantfalta, 'ltot': listagral, 'cantval':listhd.count(), 'listf':listf, 'cantfalta':cantfalta, 'desde':desde, 'fecha':fec, 'nro':a_id} )
        else:
            return HttpResponseRedirect('/asientos_list/')
        return HttpResponseRedirect('/asientos_list/')
    else:
        return HttpResponseRedirect('/obispado/login/')
        


def update_asientos(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        listcuentasd = []
        listcuentash = []
        tc = TipoCuenta.objects.filter(tipo_de_saldo='d')
        if tc.count()>0:
            for x in tc:
                n1 = CuentaNivel1.objects.filter(tipo=x.id)
                for y in n1:
                    n2 = CuentaNivel2.objects.filter(tipo = y.id)
                    for z in n2:
                        n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id")
                        if n3.count()>0:
                            for a in n3:
                                listcuentasd.append({"id":a.id, "nombre":a.nombre})
                        
        tc = TipoCuenta.objects.filter(tipo_de_saldo='h')
        if tc.count()>0:
            for x in tc:
                n1 = CuentaNivel1.objects.filter(tipo=x.id)
                for y in n1:
                    n2 = CuentaNivel2.objects.filter(tipo = y.id)
                    for z in n2:
                        n3 = CuentaNivel3.objects.filter(tipo = z.id).order_by("id")
                        if n3.count()>0:
                            for a in n3:
                                listcuentash.append({"id":a.id, "nombre":a.nombre})
        tipouser = User.objects.get(id=user_id)
        if 'date1xx' in request.GET and request.GET['date1xx']:
            fe = request.GET['date1xx']
            fecha = time.strptime(str(fe), "%d/%m/%Y")
            fechaiso = time.strftime("%Y-%m-%d", fecha)
            com = request.GET['comentarios']
            nro_mod = request.GET['nro_mod']
            cuentad=[]
            cuentah=[]
            montod=[]
            montoh=[]
            #newasiento = AsientoContable(fecha = fechaiso, comentario = str(com))
            newasiento = AsientoContable.objects.get(id=nro_mod)
            
            fecha = time.strptime(str(date.today()), "%Y-%m-%d")
            #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
            path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
            archivo = open(path, "a")
            escribir = "El usuario " + tipouser.username + " ha modificado el asiento con fecha: "+str(fechaiso)+ " el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
            archivo.write(escribir)
            if (newasiento.fecha) != (fechaiso):
                escribir = "El usuario " + tipouser.username + " ha cambiado la fecha del asiento: de "+str(newasiento.fecha)+ " a "+ str(fechaiso) +" el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
                archivo.write(escribir)

            archivo.close()
            
            newasiento.fecha = fechaiso
            newasiento.comentario = com
            newasiento.save()
            cont = 0
            for i in range(1, 11):
                if 'cd'+str(i) in request.GET and request.GET['cd'+str(i)]:
                        cuentad.append(request.GET['cd'+str(i)])
                        cont = cont + 1
                if 'd'+str(i) in request.GET and request.GET['d'+str(i)]:
                        montod.append(request.GET['d'+str(i)])
                if 'ch'+str(i) in request.GET and request.GET['ch'+str(i)]:
                        cuentah.append(request.GET['ch'+str(i)])
                if 'h'+str(i) in request.GET and request.GET['h'+str(i)]:
                        montoh.append(request.GET['h'+str(i)])
                        
            delreg = AsientoDebeDetalle.objects.filter(asiento=nro_mod).distinct()
            if delreg.count()>0:
                for z in delreg:
                    z.delete()
            delreg = AsientoHaberDetalle.objects.filter(asiento=nro_mod).distinct()
            if delreg.count()>0:
                for z in delreg:
                    z.delete()
                       
            for i in range(0, cont):
                haber = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id = int(cuentah[i]), monto = float(montoh[i]))
                haber.save()
                debe = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id = int(cuentad[i]), monto = float(montod[i]))
                debe.save()
            #cn3 = CuentaNivel3.objects.all()
            return HttpResponseRedirect('/obispado/asientos_list/')
            #return render_to_response('asiento/asiento.html', {'nombreuser': tipouser.username,'listcuentasd': listcuentasd, 'listcuentash':listcuentash, 'msj':'Asiento Cargado Correctamente'})
        else:
            #cn3 = CuentaNivel3.objects.all()
            return render_to_response('asiento/asiento.html', {'nombreuser': tipouser.username,'listcuentasd': listcuentasd, 'listcuentash':listcuentash})
        return render_to_response('asiento/asiento.html')
    else:
        return HttpResponseRedirect('/obispado/login/')
        
