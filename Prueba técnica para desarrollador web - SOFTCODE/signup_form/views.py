from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Users
from re import match 
from json import dumps
# Create your views here.
def home(request):
    """
    args:
    request -> peticion HTTP

    renderiza la plantilla con el formulario
    """
    mensaje = messages.get_messages(request)
    print(mensaje)
    return render(request, "signup.html", {"message": mensaje})

def signup(request):
    """
    args:
    request -> peticion HTTP

    si los datos son validos los agrega a la base de datos, si no lanza un mensaje de error
    """
    if request.method == "POST":
        #validamos los datos antes de insertarlos
        data = {
            "name":request.POST.get("name"),
            "last_name":request.POST.get("last_name"),
            "email":request.POST.get("email"),
            "password_1":request.POST.get("passwd"),
            "password_2":request.POST.get("passwd_rpt")
        }
        is_valid = validar_datos(request, **data)
        if is_valid == True:
            usr = Users()
            usr.nombre = data["name"]
            usr.apellido = data["last_name"]
            usr.email = data["email"]
            usr.password = data["password_1"]
            usr.save()
            messages.success(request, "usuario creado satisfactoriamente")

        return redirect("home")

def validar_datos(request, **data):
    """
    Args: 
    request -> peticion HTTP
    **data -> type: dict

    valida los datos provenientes del frontend
    """
    #la funcion se va ejecutar siempre y cuando tenga las claves completas, si no retorna un error
    if "name" in data and "last_name" in data and "email" in data and "password_1" in data and "password_2" in data:
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

        #validamos que la variable [name] no este vacia y a su vez que su tamaño no sea menor a 3 caracteres
        if data["name"] == "" or len(data["name"]) <= 3:
            messages.error(request, "nombre invalido")
            return False

        #validamos que la variable [last_name] no este vacia y a su vez que su tamaño no sea menor a 3 caracteres
        elif data["last_name"] == "" or len(data["last_name"]) <= 3:
            messages.error(request, "apellido invalido")
            return False

        #validamos que el correo electronico tenga un formato valido
        elif match(expresion_regular, data["email"]) is None:
            messages.error(request, "correo electronico invalido")
            return False

        #validamos que la contraseña tenga 8 caracteres y contenga una mayuscula, una minuscula, un numero y un caracter especial
        elif match(r"^[a-zA-Z0-9_\-!_?@#$%^&*(){}]+$", data["password_1"]) is None or len(data["password_1"]) < 8:
            messages.error(request, "Contraseña invalida")
            return False

        #validamos que las contraseñas sean iguales
        elif data["password_1"] != data["password_2"]:
            messages.error(request, "las contraseñas no coinciden")
            return False

        #en caso de que este todo correcto retornamos True para indicar que todo esta bien
        else:
            return True
    else:
        messages.error(request, "error en el formulario")
        return False
    
def get_all_data(request):
    """
    args:
    response -> peticion HTTP

    almacena todos los datos de la tabla "Users" y los retorna como json para mostrarlos en el frontend 
    """
    usr = Users.objects.all()
    usr_data = list()
    for user in usr:
        usr_data.append({
            "id":user.id,
            "name": user.nombre,
            "apellido": user.apellido,
            "password": user.password,
            "email":user.email
        })
    json_data = dumps(usr_data)

    return JsonResponse(usr_data, safe=False)

def update_user(request, user_id):
    """"
    args:

    request -> peticon HTTP
    user_id(int) -> id del usuario a actualizar

    esta funcion se encarga de actualizar usuarios de la base de datos
    """
    if request.method == "GET":
        user = Users.objects.get(pk=user_id)
        return render(request, "update.html", {"usr_data" : {
            "id" :user.id,
            "name": user.nombre,
            "apellido": user.apellido,
            "password": user.password,
            "email":user.email
        }})
    else:
        try:
            usr = get_object_or_404(Users, pk=user_id)
            data = {
                "name":request.POST.get("name"),
                "last_name":request.POST.get("last_name"),
                "email":request.POST.get("email"),
                "password_1":request.POST.get("passwd"),
                "password_2":request.POST.get("passwd"),
            }
            print(data)
            is_valid = validar_datos(request, **data)
            if is_valid == True:
                usr.nombre = data["name"]
                usr.apellido = data["last_name"]
                usr.email = data["email"]
                usr.password = data["password_1"]
                usr.save()
                messages.success(request, "usuario actualizado satisfactoriamente")

            return redirect("home")
        except ValueError:
            message.error(request, "error actualizando al usuario")
            return redirect("home")

def delete_user(request, user_id):
    """"
    args:

    request -> peticon HTTP
    user_id(int) -> id del usuario a eliminar

    esta funcion se encarga de eliminar usuarios de la base de datos
    """
    try:
        user = Users.objects.get(pk=user_id)
        user.delete()
        return redirect('home')
    except:
        return redirect("home")