from flask import Flask, render_template, url_for, request, make_response, session, redirect, jsonify, Response


from Datos.usuario import Usuario
from Datos.receta import Receta
from Datos.comentario import Comentario
from os import environ

import json
import base64
import csv
import subprocess
import os

app = Flask(__name__)
comentarios1=[]
comentarios2=[]
usuario1 = Usuario("admin", "uno", "admin", "admin","Administrador","http://1.bp.blogspot.com/-TLjVIMk7fwY/US1ILs6P4kI/AAAAAAAAA9g/znLuGzKvhaw/s1600/Foto+yoona+snsd+terbaru+Dan+Tercantik+lengkap+1.jpg")
receta1= Receta(0,"Administrador","Lasaña","¿A quién no le gusta la lasaña? Este clásico plato de la cocina italiana hace las delicias de los más pequeños y triunfa entre los no tan pequeños. Es perfecto, además, para preparar en cantidades, congelar y llevar al trabajo o al cole. El relleno puede ser de casi cualquier cosa pero, nosotros, no hemos decantado por la clásica lasaña de carne. Una receta fácil y deliciosa para tomar en familia.",
"0.75 l de Leche \n 40 g de Mantequilla\n40 g de Harina\n1 pizca de Nuez moscada molida\nSal","\n1.En una sartén, sofreír en un poco de aceite de oliva la cebolla y la zanahoria peladas y cortadas en dados bien pequeños.\n2.Pelar el tomate y cortarlo en dados pequeños. Añadirlo a la sartén. Salpimentar y dejar unos 20 minutos a fuego medio-bajo, hasta que esté en su punto.\n3.Incorporamos los champiñones laminados y los salteamos con la carne.","1:30","https://th.bing.com/th/id/OIP.rSF_epgUbdjkLMui98fKNAHaE8?w=278&h=185&c=7&o=5&pid=1.7",comentarios1)
receta2= Receta(1,"Administrador","Ensalada","¿A quién no le gusta la lasaña? Este clásico plato de la cocina italiana hace las delicias de los más pequeños y triunfa entre los no tan pequeños. Es perfecto, además, para preparar en cantidades, congelar y llevar al trabajo o al cole. El relleno puede ser de casi cualquier cosa pero, nosotros, no hemos decantado por la clásica lasaña de carne. Una receta fácil y deliciosa para tomar en familia.",
"0.75 l de Leche \n 40 g de Mantequilla\n40 g de Harina\n1 pizca de Nuez moscada molida\nSal","1.En una sartén, sofreír en un poco de aceite de oliva la cebolla y la zanahoria peladas y cortadas en dados bien pequeños.\n2.Pelar el tomate y cortarlo en dados pequeños. Añadirlo a la sartén. Salpimentar y dejar unos 20 minutos a fuego medio-bajo, hasta que esté en su punto.\n3.Incorporamos los champiñones laminados y los salteamos con la carne.","1:30","https://th.bing.com/th/id/OIP.chnEAkI4xogn108YLrpDegHaGF?pid=Api&rs=1",comentarios2)

usuarios = [usuario1]

app.secret_key = b'asjdlfajsdf'

recetas = [receta1,receta2]
recientes=[]

indice=1

def get_recientes():
    recientes.clear()
    for receta in recetas[0:3]:
            recientes.append(receta)
      



def campos_vacios(nombre,apellido,usuario,contraseña,confirmacion):
    if nombre=="" or apellido=="" or usuario=="" or contraseña=="" or confirmacion=="":
        return False
    return True

def campo_vacio(usuario):
    if usuario=="":
        return False
    return True

def campos_vaciosLogin(usuario,contraseña):
    if usuario=="" or contraseña=="":
        return False
    return True

def validar_login(user, contrasena):
    for usuario in usuarios:
        if usuario.usuario == user and usuario.contrasena == contrasena:
            return usuario
    return None
def repeticion_pass(contrasena, confirmacion):
    
    if str(contrasena) == str(confirmacion):
        return True
    else:
        return False

def agregar_usuario(nombre, apellido, usuario, contraseña, tipo, foto):
    usuarios.append(Usuario(nombre, apellido, usuario, contraseña, tipo, foto))
    for usuario in usuarios:
        print(usuario.usuario)

def usuario_repetido(user):
    y=False
    for x in usuarios:
        if str(user)!=str(x.usuario):
            y=False
        else:
            y=True
            return y
    return y        
              
def validar_estructura(user):
    usuario=str(user)
    if usuario!="":
        k=usuario[0]
        y=user.isalnum()
        x=k.isalpha()
        
        if x==True and y==True:
            return True
        else:
            return False
    return False          

def buscar_user(usuario):
    for x in usuarios:
        if str(x.usuario)==str(usuario):
            return x
              

def get_index():
    global indice 
    indice =indice+1
    return indice

def search_recipe(index):
    for x in recetas:
        if int(x.index) == int(index) :
            return x

def search_photo(user):
    photo="http://1.bp.blogspot.com/-TLjVIMk7fwY/US1ILs6P4kI/AAAAAAAAA9g/znLuGzKvhaw/s1600/Foto+yoona+snsd+terbaru+Dan+Tercantik+lengkap+1.jpg"
    for x in usuarios:
        if x.usuario==user:
            photo=x.foto
    return photo        

def agregarComent(id,comentario):
    for x in recetas:
        if int(x.index)==int(id):
            x.comentarios.insert(0, comentario)

def modificarUsuario(usuarioViejo,usuario):
    for x in usuarios:
        if str(x.usuario)==str(usuarioViejo):
           x.nombre=usuario.nombre
           x.apellido=usuario.apellido
           x.usuario=usuario.usuario
           session['usuario_logeado']=usuario.usuario
           x.contrasena=usuario.contrasena
           
           x.foto=usuario.foto

def campos_vac(nombre,apellido,usuario,contraseña,confirmacion, foto):
    if nombre=="" or apellido=="" or usuario=="" or contraseña=="" or confirmacion=="" or foto=="":
        return False
    return True

def modificarReceta(indice,receta):   
    for x in recetas:
        if int(x.index)==int(indice):
           x.titulo=receta.titulo
           x.resumen=receta.resumen
           x.ingredientes=receta.ingredientes
           x.procedimiento=receta.procedimiento
           x.imagen=receta.imagen    
           x.tiempo=receta.tiempo

def eliminarReceta(indice):
    receta=search_recipe(indice)
    recetas.remove(receta)

@app.route('/')
def iniciar():
    return redirect('index')

@app.route('/index', methods=['GET'])
def home():
    
    get_recientes()
    if 'usuario_logeado' in session:
        user=session['usuario_logeado']
        usuario=buscar_user(user)
        tipo=usuario.tipo
        return render_template('home1.html', usuario=session['usuario_logeado'], recientes=recientes, tipo=tipo)
    return render_template('home1.html',recientes=recientes, usuario=None, recetas=recetas)


@app.route('/register',methods=['POST','GET'])
def registro():
    error=None
    
    if request.method=='POST':
        campos_llenos=campos_vacios(request.form['nombre'],request.form['apellido'],request.form['usuario'],request.form['contraseña'],request.form['confirmacion'])
        confirmacion = repeticion_pass(request.form['contraseña'], request.form['confirmacion'])
        repetido = usuario_repetido(request.form['usuario'])
        estructura= validar_estructura(request.form['usuario'])
        if campos_llenos==True:
            if confirmacion==True: 
                if estructura==True:
                    if repetido==False:
                        agregar_usuario(request.form['nombre'],request.form['apellido'],request.form['usuario'], request.form['contraseña'], "Cliente", "https://cdn4.vectorstock.com/i/1000x1000/92/93/chef-profile-avatar-icon-vector-10179293.jpg" ) 
                       
                        return redirect("login")  
                    
                    else:
                        error="Este Nombre de Usuario ya está en uso. Por favor eliga otro nombre de usuario"
                        return render_template('register.html', error=error)
                else:
                    error="El nombre de usuario debe iniciar con una letra, y puede contener solamente letras y números."
                    return render_template('register.html', usuario=None, error=error )        
            else:
                error="Las contraseñas no coinciden"
                return render_template('register.html', usuario=None, error=error )
        else:
            error="Debe llenar todos los campos"
            return render_template('register.html', usuario=None, error=error )

    return render_template('register.html', usuario=None, error=error, recetas=recetas)



@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    registrado=None
    tipo=None
    
    if request.method == 'POST':
        campos_llenosLogin=campos_vaciosLogin(request.form['usuario'],request.form['contraseña'])
        if campos_llenosLogin==True:
            usuario = validar_login(request.form['usuario'], request.form['contraseña'])    
            if usuario != None:
                session['usuario_logeado'] = usuario.usuario
                tipo=usuario.tipo
                return redirect('index')
            else:
                error = 'El usuario o la contraseña son Incorrectos'
                return render_template('login.html', error=error, registrado=registrado)
        else:
            error = 'Debe llenar todos los campos'
            return render_template('login.html', error=error, usuario=None, registrado=registrado)       
    if 'usuario_logueado' in session:
        nombre=session['usuario_logueado']
        usuario=buscar_user(nombre)
        tipo=usuario.tipo
        get_recientes()
        return redirect('index')    
    return render_template('login.html', error=error, registrado=registrado, tipo=tipo)

@app.route('/recuperacion',methods=['POST', 'GET'])  
def recuperacion():
    if request.method == 'POST':
        campo_lleno=campo_vacio(request.form['usuario'])
        if campo_lleno==True:
            usuario=buscar_user(request.form['usuario'])
            if usuario !=None: 
                contraseña=usuario.contrasena
                mensaje="La contraseña es: "+ contraseña
                return render_template('recuperacion.html', mensaje=mensaje)
            else:
                mensaje="El nombre de usuario ingresado no existe"
                return render_template('recuperacion.html', mensaje=mensaje)    
        else:
            mensaje="Debe ingresar el nombre de usuario"
            return render_template('recuperacion.html', mensaje=mensaje)
    return render_template('recuperacion.html', mensaje=None)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('usuario_logeado', None)
    
    return redirect('login')


@app.route('/recetas', methods=['GET','POST'])
def allrecipes():
    if 'usuario_logueado' in session:
        return render_template('recetas.html', usuario=session['usuario_logueado'], recetas=recetas,error=None)
    return render_template('recetas.html',  recetas=recetas, error=None, usuario=session['usuario_logeado'])

@app.route('/postReceta', methods=['POST'])
def agregarReceta():
    datos = request.get_json()
    if datos['titulo'] == '' or datos['resumen'] == '' or datos['ingredientes'] == '' or datos['procedimiento']=='' or datos['hora']=='' or datos['imagen']=='':
        return {"msg": 'Error en contenido'}
    else:
        id= get_index() 
        comentarios=[]
        receta = Receta(id,str(datos['autor']),str(datos['titulo']), str(datos['resumen']), str(datos['ingredientes']), str(datos['procedimiento']),str(datos['hora']), str(datos['imagen']),comentarios)
        recetas.insert(0, receta)
    for receta in recetas:
        print(str(receta.autor))
    return {"msg": 'Receta agregada'}    


@app.route('/receta/<int:id>')
def recipe(id):
    this_receta= search_recipe(id)
    comentarios=this_receta.comentarios
    resumen=str(this_receta.resumen)
    print(this_receta)
    return render_template('receta.html',  receta=this_receta, error=None, usuario=session['usuario_logeado'],comentarios=comentarios,resumen=resumen)

@app.route('/receta/logout')    
def deslogear():
    if 'usuario_logeado' in session:
        return redirect(url_for('logout'))

@app.route('/receta/inicio')    
def backtohome():
    return redirect(url_for('iniciar'))

@app.route('/receta/allrecipes')    
def backtorecipes():
    return redirect(url_for('allrecipes'))    

@app.route('/receta/perfil')    
def backtoperfil():
    return redirect(url_for('profile')) 

@app.route('/receta/administracion')    
def gotoadmon():
    return redirect(url_for('admon'))       

@app.route('/postComentario', methods=['POST'])
def agregarComentario():
    datos = request.get_json()
    if datos['mensaje'] == '':
        return {"msg": 'Error en contenido'}
    else:
        foto=search_photo(str(datos['autor']))        
    
        comentario = Comentario(str(datos['autor']),foto,str(datos['mensaje']),str(datos['fecha']))
        agregarComent(datos['id_receta'],comentario)
        
        
    return {"msg": 'Comentario agregado'}    

@app.route('/perfil', methods=['POST','GET'])
def profile():
    repetido=False
    estructura=True
    if request.method == 'POST':
        campos_llenos=campos_vac(request.form['nombre'],request.form['apellido'],request.form['usuario'],request.form['contraseña'],request.form['confirmacion'],request.form['foto'])
        confirmacion = repeticion_pass(request.form['contraseña'], request.form['confirmacion'])
        repetido=False
        estructura=True
        if request.form['usuario'] != session['usuario_logeado']:
            repetido = usuario_repetido(request.form['usuario'])
            estructura= validar_estructura(request.form['usuario'])

        if campos_llenos==True:
            if confirmacion==True: 
                if estructura==True:
                    if repetido==False:
                        usuario=Usuario(request.form['nombre'],request.form['apellido'],request.form['usuario'], request.form['contraseña'], "Cliente", request.form['foto'] )
                        modificarUsuario(session['usuario_logeado'],usuario)
                        error="Los datos han sido modificados con exito" 
                        user=session['usuario_logeado']
                        usuario=buscar_user(user)
                        return render_template('perfil.html', error=error, usuario=usuario)
                    
                    else:
                        error="Este Nombre de Usuario ya está en uso. Por favor eliga otro nombre de usuario"
                        user=session['usuario_logeado']
                        usuario=buscar_user(user)
                        return render_template('perfil.html', error=error, usuario=usuario )
                else:
                    error="El nombre de usuario debe iniciar con una letra, y puede contener solamente letras y números."
                    user=session['usuario_logeado']
                    usuario=buscar_user(user)
                    return render_template('perfil.html', usuario=usuario, error=error)        
            else:
                error="Las contraseñas no coinciden"
                user=session['usuario_logeado']
                usuario=buscar_user(user)
                return render_template('perfil.html', usuario=usuario, error=error )
        else:
            error="Debe llenar todos los campos"
            user=session['usuario_logeado']
            usuario=buscar_user(user)
            return render_template('perfil.html', usuario=usuario, error=error )    

    user=session['usuario_logeado']
    usuario=buscar_user(user)
    return render_template('perfil.html', usuario=usuario,error=None)
   
@app.route('/modificarPerfil', methods=['POST'])    
def modificacion():
    datos = request.get_json()  
    confirm = repeticion_pass(str(datos['contraseña']),str(datos['confirmacion']))
    repetido = usuario_repetido(str(datos['usuario']))
    estructura= validar_estructura(str(datos['usuario']))
    if confirm==True: 
        if estructura==True:
            if repetido==False:      
                usuario = Usuario(str(datos['nombre']),str(datos['apellido']),str(datos['usuario']),str(datos['contraseña']),str(datos['tipo']),str(datos['foto']))
                print(str(datos['nombre'])+str(datos['apellido'])+str(datos['usuario'])+str(datos['contraseña'])+str(datos['tipo'])+str(datos['foto']))
                modificarUsuario(str(datos['viejo']),usuario)
                session['usuario_logeado'] = str(datos['usuario'])
                
            else:
                return {"msg": 'Este Nombre de Usuario ya está en uso. Por favor eliga otro nombre de usuario'}
        else:
            return {"msg": 'El nombre de usuario debe iniciar con una letra, y puede contener solamente letras y números.'}      
    else:
        return {"msg": 'Las contraseñas no coinciden'}

@app.route('/administracion')
def admon():
    user=session['usuario_logeado']
    usuario=buscar_user(user)
    return render_template('administracion.html', usuario=usuario,error=None, usuarios=usuarios, recetas=recetas)

@app.route('/modificarReceta/<indice>', methods=['POST','GET'])
def modification(indice):
    
    if request.method == 'POST':

        this_receta=Receta(indice,str(request.form['autor']),str(request.form['titulo']),str(request.form['resumen']), str(request.form['ingredientes']), str(request.form['procedimiento']), str(request.form['tiempo']),str(request.form['imagen']),str(request.form['tiempo'] ))
        modificarReceta(indice,this_receta)
        error="Los datos han sido modificados con exito" 
        user=session['usuario_logeado']
        usuario=buscar_user(user)
        receta=search_recipe(indice)
        return render_template('modificarReceta.html', error=error, usuario=usuario, receta=receta)  
    else:
        receta=search_recipe(indice)
        user=session['usuario_logeado']
        usuario=buscar_user(user)
        return render_template('modificarReceta.html', usuario=usuario,error=None, receta=receta)   

@app.route('/eliminarReceta',methods=['POST'])        
def eliminacion():    
    datos = request.get_json() 
    eliminarReceta(datos['index_receta']) 
    return {"msg": 'La receta fue eliminada'}

@app.route('/verComentarios/<indice>',methods=['POST','GET'])        
def vercoments(indice):    
    receta=search_recipe(indice)
    user=session['usuario_logeado']
    usuario=buscar_user(user)
    comentarios=receta.comentarios
    return render_template('verComentarios.html', usuario=usuario, receta=receta, comentarios=comentarios)

@app.route('/verComentarios/regresar')        
def returnadmon():   
    return redirect(url_for('admon'))      

@app.route('/addAdmin',methods=['POST'])        
def addadmin():   
    datos = request.get_json()
    campos_llenos=campos_vacios(str(datos['nombre']),str(datos['apellido']),str(datos['usuario']),str(datos['contraseña']),str(datos['confirmacion']))
    confirmacion = repeticion_pass(str(datos['contraseña']), str(datos['confirmacion']))
    repetido = usuario_repetido(str(datos['usuario']))
    estructura= validar_estructura(str(datos['usuario']))
    if campos_llenos==True:
            if confirmacion==True: 
                if estructura==True:
                    if repetido==False:
                        agregar_usuario(str(datos['nombre']),str(datos['apellido']),str(datos['usuario']), str(datos['contraseña']),"Administrador", "https://cdn4.vectorstock.com/i/1000x1000/92/93/chef-profile-avatar-icon-vector-10179293.jpg" ) 
                       
                        return {"msg": 'Usuario creado con exito'}
                    
                    else:
                       
                        return {"msg": 'Este Nombre de Usuario ya está en uso. Por favor eliga otro nombre de usuario'}
                else:
                   
                   return {"msg": 'El nombre de usuario debe iniciar con una letra, y puede contener solamente letras y números.'}        
            else:
                return {"msg": 'Las contraseñas no coinciden'}
    else:
        return {"msg": 'Debe llenar todos los campos'}

@app.route('/cargarArchivo', methods=['POST'])
def agregarRecetas():
    datos = request.get_json()
    contenido = base64.b64decode(datos['data']).decode('utf-8')
    filas = contenido.splitlines()
    reader = csv.reader(filas, delimiter=',')
    for row in reader:
        indice= get_index() 
        comentarios=[]
        receta = Receta(indice,row[0], row[1], row[2],row[3],row[4],row[5],row[6],comentarios)
        recetas.append(receta)

    return {"msg": 'Receta agregada'}

if __name__ == '__main__':
    app.run(debug=True)

