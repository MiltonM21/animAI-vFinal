from django.shortcuts import render, redirect
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth
from .models import MiModelo
from .forms import userForm
from .forms import loginForm
from .forms import testUser
from pyrebase import pyrebase
from django.template import RequestContext
from django.http import JsonResponse
from google.cloud.firestore_v1 import FieldFilter
import datetime
import json
import requests

from inference_sdk import InferenceHTTPClient

firebaseConfig = {
  "apiKey": "AIzaSyCRw5jZZPvmdA3TgP_jRnuUHp_Y92to9Ew",
  "authDomain": "anim-ai-13c1d.firebaseapp.com",
  "databaseURL": "https://anim-ai-13c1d-default-rtdb.firebaseio.com",
  "projectId": "anim-ai-13c1d",
  "storageBucket" : "anim-ai-13c1d.appspot.com",
  "messagingSenderId" : "508533010561",
  "appId": "1:508533010561:web:3600df94f907b6be7bdd80",
  "measurementId": "G-KMK4THVYBZ"
}

try:
    firebase = pyrebase.initialize_app(config=firebaseConfig)
    print("Firebase initialized successfully")
except Exception as e:
    print("Firebase initialization error:", e)

authen = firebase.auth()

cred = credentials.Certificate("C:/Users/User/Desktop/V6.1.3/proyecto/AnimAI/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def index(request):
    objetos = MiModelo.objects.all()
    if request.method == "POST":
        form = userForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                emailS = data['email']
                passwordS = data['contraseña']
                
                user = authen.sign_in_with_email_and_password(emailS, passwordS)
                print(user["idToken"])
                testF = testUser()

                # Obtener el nombre y apellido del usuario desde Firestore
                uid = user['localId']
                db = firestore.client()
                collUsuarios = db.collection("USUARIOS")
                user_data = collUsuarios.document(uid).get().to_dict()
            
                
                # Guardar los datos del usuario en la sesión
                request.session['user_info'] = user_data
                nombre = user_data.get('nombre', '')
                apellido = user_data.get('apellido', '')
                saludo = f"Hola, {nombre} {apellido}!"

                # Configurar la cookie del token de usuario
                response = render(request, 'inicio.html', {"form": testF, "saludo": saludo})
                response.set_cookie('idToken', user["idToken"])

                # Establecer mensaje de éxito
                messages.success(request, 'Inicio de sesión exitoso.', extra_tags='success')

                return response
            except Exception as e:
                print(f"Error al iniciar sesión: {e}")
                messages.error(request, 'Error al iniciar sesión. Por favor, verifica tus credenciales e intenta nuevamente.', extra_tags='danger')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.', extra_tags='warning')
    else:
        form = userForm()
    return render(request, 'index.html', {'form': form, 'objetos': objetos})

def insertIntoFirestore(id, data, collection):
    db = firestore.client()
    print("db client")
    docRef = db.collection(collection)
    docRef.add(data,id)

def getIdUser(emailU):
    user = auth.get_user_by_email(emailU)
    print(user.uid + " es")
    print()
    return user.uid


def getIdUserByToken(request):
    user = auth.verify_id_token(request.COOKIES["idToken"])
    print("this is id" + user["uid"])
    return user["uid"]


def registrarme(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nameI = data['nombre']
            lastnameI = data['apellido']
            emailI = data['email']
            passwordI = data['contraseña']
            try:
                # Crear usuario en Firebase Authentication
                user = authen.create_user_with_email_and_password(emailI, passwordI)
                
                # Obtener UID del usuario creado
                uid = user['localId']
                
                # Conectar a Firestore
                db = firestore.client()
                
                # Guardar los datos adicionales en Firestore usando el UID como clave
                collUsuarios = db.collection("USUARIOS")
                collUsuarios.document(uid).set({
                    "nombre": nameI,
                    "apellido": lastnameI,
                    "email": emailI,
                    "contraseña": passwordI,
                })
                
                # Guardar el nombre y apellido del usuario en la sesión
                request.session['user_info'] = {'nombre': nameI, 'apellido': lastnameI}
                
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.', extra_tags='success')  # Mensaje de éxito
                form = loginForm()  # Limpia el formulario
            except requests.exceptions.HTTPError as e:
                error_response = e.response
                if error_response:
                    try:
                        error_json = error_response.json()
                        error_message = error_json.get('error', {}).get('message', '')
                        if error_message == "EMAIL_EXISTS":
                            messages.error(request, 'El correo electrónico ya está registrado. Por favor, inicia sesión.', extra_tags='danger')  # Mensaje de error
                        else:
                            messages.error(request, f'Error al registrar usuario: {error_message}', extra_tags='danger')  # Mensaje de error genérico
                    except ValueError:
                        messages.error(request, 'Error al procesar la respuesta del servidor.', extra_tags='danger')
                else:
                    messages.error(request, 'Error al registrar usuario: No se recibió respuesta del servidor.', extra_tags='danger')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.', extra_tags='warning')  # Mensaje de error de formulario
            return render(request, 'registrarme.html', {'form': form})
    else:
        form = loginForm()
    return render(request, 'registrarme.html', {'form': form})


def inicio(request):
    print("Entrando en la vista inicio")
    if request.method == 'POST':
        form = testUser(request.POST, request.FILES)
        if form.is_valid():
            print("Formulario válido")
            data = form.cleaned_data
            name = data['titulo']
            file = request.FILES['archivo']
            print("Subiendo archivo")

            CLIENT = InferenceHTTPClient(
              api_url="https://detect.roboflow.com",
              api_key="r56rxjEk6avETe2qMGg7"
            )
            print(type(file))
            
            
            strg = firebase.storage()
            print("Subida en progreso")
            strg.child(name).put(file)
            urlImg = getImgUrl(name)
            result = CLIENT.infer(urlImg, model_id="stanford-dogs-0pff9/3")
            date = datetime.datetime.now()
            datet = date.strftime("%x")
            insertIntoFirestore(None, {"usuario": getIdUserByToken(request), "img": name, "date": datet, "bread" : result["predictions"][0]["class"], "url" : urlImg}, "ARCHIVOS")
            print("Datos de la imagen insertados en Firestore correctamente")
        else:
            print("Formulario no válido")
    else:
        print("Solicitud no es POST, mostrando formulario")
        form = testUser()
        
    user_info = request.session.get('user_info')
    if user_info is not None:
        print("Información del usuario encontrada en la sesión:", user_info)
        nombre = user_info.get('nombre', '')
        apellido = user_info.get('apellido', '')
        saludo = f"Hola, {nombre} {apellido}!"
    else:
        print("No se encontró información del usuario en la sesión")
        saludo = "Hola"

    return render(request, 'inicio.html', {'form': form, 'saludo': saludo, 'bread' : result["predictions"][0]["class"]})


def configuracion(request):
    objetos = MiModelo.objects.all()
    return render(request, 'configuracion.html', {'objetos': objetos})

def cuenta(request):
    objetos = MiModelo.objects.all()
    return render(request, 'cuenta.html', {'objetos': objetos})

def historial(request):
    fechas = MiModelo.objects.all()
    fechas = dateHistorial(request)
    return render(request, 'historial.html', {'fecha': fechas})

def img(request):
    if(request.method == 'POST'):
        dat = json.load(request)
        data = dat["post_data"]
        print(data)
        return JsonResponse(dateImages(request,data))
    
def dateHistorial(request):
    try:
      date = []
      db = firestore.client()
      collection = db.collection("ARCHIVOS")
      idUser = getIdUserByToken(request)
      query = collection.where(filter = FieldFilter("usuario","==",idUser))
      for fecha in query.stream():
        dictFecha = fecha.to_dict()
        fechaDoc = dictFecha["date"]
        if(date.count(fechaDoc) == 0):
            date.append(fechaDoc)
    except:

        print("n")
    print(date)
    return date



def dateImages(request,data):
    try:
        print("da")
        date = {}
        db = firestore.client()
        storage = firebase.storage()
        collection = db.collection("ARCHIVOS")
        idUser = getIdUserByToken(request)
        query = collection.where(filter = FieldFilter("usuario","==",idUser)).where(filter = FieldFilter("date","==",data))
        print("her")
        a = 0
        for jsonData in query.stream():            
            dictImg = jsonData.to_dict()
            print(dictImg)
            nameImg = dictImg["img"]
            link = storage.child(nameImg).get_url(0)
            print(link)
            date["p"+ str(a)] = link
            a = a+1
    except:
        print("e")
    print(date)
    return date



def getImgUrl(name):
    try:
        strg = firebase.storage()
    except:
        print("er")
    return strg.child(name).get_url(0)