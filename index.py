from flask import Flask, render_template, url_for, request, make_response, session, redirect, jsonify


from Datos.usuario import Usuario

import json

app = Flask(__name__)

usuario1 = Usuario("admin", "uno", "admin", "admin","Administrador","http://1.bp.blogspot.com/-TLjVIMk7fwY/US1ILs6P4kI/AAAAAAAAA9g/znLuGzKvhaw/s1600/Foto+yoona+snsd+terbaru+Dan+Tercantik+lengkap+1.jpg")


usuarios = [usuario1]

app.secret_key = b'mimamamemima'

recetas = []

def validar_login(user, contrasena):
    for usuario in usuarios:
        if usuario.usuario == user and usuario.contrasena == contrasena:
            return usuario
    return None
def repeticion_pass(contrasena, confirmacion):
    if contrasena == confirmacion:
        return True
    else:
        return False

def agregar_usuario(nombre, apellido, usuario, contraseña, tipo, foto):
    usuarios.append(Usuario(nombre, apellido, usuario, contraseña, tipo, foto))

def usuario_repetido(user):
    for usuario in usuarios:
        if usuario.usuario == user:
            return True
        else:
            return False    
             

@app.route('/')
def home():
    if 'usuario_logueado' in session:
        return render_template('home1.html', usuario=session['usuario_logueado'])
    return render_template('home1.html', usuario=None)

@app.route('/register',methods=['POST','GET'])
def registro():
    error1=None
    error2=None

    if request.method=='POST':
        confirmacion = repeticion_pass(request.form['contraseña'], request.form['confirmacion'])
        repetido = usuario_repetido(request.form['usuario'])
        
        if confirmacion==True: 
            if repetido == True:
                error1="Este Nombre de Usuario ya está en uso. Por favor eliga otro nombre de usuario"
                return render_template('register.html', error1=error1, error2=error2)
            else:
                agregar_usuario(request.form['nombre'],request.form['apellido'],request.form['usuario'], request.form['contraseña'], "Cliente", request.form['foto']  ) 
                return render_template('')   
        else:
            error1="Las contraseñas no coinciden"
            return render_template('register.html', usuario=None, error1=error1, error2=error2)
    return render_template('register.html', usuario=None, error1=error1, error2=error2)

@app.route('/recuperacion')  
def recuperacion():
    return render_template('recuperacion.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        usuario = validar_login(
            request.form['usuario'], request.form['contraseña'])
        if usuario != None:
            session['usuario_logeado'] = usuario.nombre
            return render_template('home1.html', usuario=usuario)
        else:
            error = 'El usuario o la contraseña son Incorrectos'
            return render_template('login.html', error=error)
    if 'usuario_logueado' in session:
        return render_template('home1.html', usuario=usuario)       
    return render_template('login.html', error=error)



@app.route('/logout', methods=['GET'])
def logout():
    session.pop('usuario_logeado', None)
    return redirect('login')    

if __name__ == '__main__':
    app.run(debug=True)

