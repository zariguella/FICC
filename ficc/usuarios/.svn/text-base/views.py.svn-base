# Create your views here.
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from obispado.ingresos.models import *
from obispado.aportantes.models import *
from obispado.libros_contables.models import *
from obispado.usuarios.forms import *
from obispado.plan_de_cuentas.models import *
from django.http import HttpResponse, HttpResponseRedirect
import datetime, string
import time
from datetime import date
import time
import csv
from django.db.models import Count  
from django.contrib.auth.models import User

from django.db.models import Q, Max, Min, Count
from django.template import Context, loader, RequestContext
from django.contrib.auth import logout, authenticate, login 
from django.contrib.auth.models import *
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import datetime, string
from django.contrib import auth

import os.path

SEED = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456780'

def random_pass(chars, length):
	import random,string
	return "".join( random.sample( chars*length, length ))
    
def login_up(request, error_message=''):
    form = RegisterForm()   
    if request.session.get('has_login',False):
        return HttpResponseRedirect('/obispado/')	
    if request.method == 'POST':
        registrar = request.POST.get('registrar','')
        if registrar!='registrar':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                request.session['has_login'] = True
                #if next:
                #	return HttpResponseRedirect(next)    
                fecha = time.strptime(str(date.today()), "%Y-%m-%d")
                #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
                path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
                archivo = open(path, "a")
                escribir = "El usuario " + username + " inicio sesion el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
                archivo.write(escribir)
                archivo.close()
                
                return HttpResponseRedirect('/obispado/')
            else:
                
                return render_to_response('usuarios/loginnew.html',{'error_message': 'Contrasenha o Nombre de usuario incorrecto','form': form})	
    else:
        return render_to_response('usuarios/loginnew.html',{'form': form})
	
def registrarse(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        form = RegisterForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                name_user = form.cleaned_data['username']
                firstname = form.cleaned_data['first_name']
                lastname = form.cleaned_data['last_name']
                #email_user = form.cleaned_data['email']
                #nacionalidad = form.cleaned_data['nacionalidad']
                pass_user = form.cleaned_data['password1']
                create_user = User(username= name_user, 
                               first_name = firstname,
                               last_name = lastname,
                               #email= email_user,
                               #nacionalidad = nacionalidad,
                               is_staff=True,
                               is_active=True,
                               is_superuser=True,
                               )
                create_user.set_password(pass_user)
                create_user.save()
                form1 = RegisterForm()
                return render_to_response('usuarios/registro.html',{'nombreuser': tipouser.username,'form': form1,'new_user':True})
            else:
                return render_to_response('usuarios/registro.html',{'nombreuser': tipouser.username,'form': form, 'error_msj':'Compruebe que los campos obligatorios esten completos'})
        else:
            return render_to_response('usuarios/registro.html',{'nombreuser': tipouser.username,'form': form})
    else:
        return HttpResponseRedirect('/obispado/login/')
    
def logged_out(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    tipouser = User.objects.get(id=user_id)
    try:
        del request.session['has_login']
        auth.logout(request)
    except KeyError:
        pass
    fecha = time.strptime(str(date.today()), "%Y-%m-%d")
    #path = "C:/Contabilidad/logs/Contabilidad/obispado/bitacora_mes_"+fecha[1]+"_"+fecha[0]+".log"
    path = "C:/Contabilidad/logs/bitacora_obispado_mes_"+str(fecha[1])+"_"+str(fecha[0])+".log"
    archivo = open(path, "a")
    escribir = "El usuario " + tipouser.username + " cerro sesion el " + str(fecha[2]) +"/"+str(fecha[1])+"/"+ str(fecha[0])+" a las "+str(time.strftime("%H:%M:%S")) + "\n"
    archivo.write(escribir)
    archivo.close()
                
    return HttpResponseRedirect('/obispado/login/')
    
def random_pass(chars, length):
	import random,string
	return "".join( random.sample( chars*length, length ))  

def recovery(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        tipouser = User.objects.get(id=user_id)
        if request.method == 'POST':
            username =request.POST.get('Username','')
            mail = request.POST.get('Mail','')
            enviar_recovery=False
            if mail:
                user=User.objects.filter(email=mail)
                if user:
                    enviar_recovery=True
            if username:
                user=User.objects.filter(username=username)
                if user:
                    enviar_recovery=True	
            if enviar_recovery:
                new_pass = random_pass(SEED,8)
                user_new_pass = User.objects.get(username=user[0].username)
                user_new_pass.set_password(new_pass) 
                user_new_pass.save()
                send_mail("Contrasenha solicitada por el usuario","""El sistema de contabilidad te envia tus datos para poder acceder al sistema \n\nNombre de usuario: %s\nContrasenha :%s\n\nIngresa a editar perfil en el sistema de contabilidad para cambiar tu contrasenha.\nSistema de Contabilidad.""" %(user[0].username,new_pass),'sistema.decontabilidad@gmail.com',[user[0].email], fail_silently=False)
            return HttpResponseRedirect('/obispado/login/')
        else:
            return render_to_response('usuarios/recuperar.html',{'nombreuser': tipouser.username})
    else:
        return HttpResponseRedirect('/obispado/login/')
