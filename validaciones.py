import index

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
  

def repeticion_pass(contrasena, confirmacion):
    
        if str(contrasena) == str(confirmacion):
            return True
        else:
            return False

def usuario_repetido(user):
        y=False
        for x in index.usuarios:
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

def campos_vac(nombre,apellido,usuario,contraseña,confirmacion, foto):
        if nombre=="" or apellido=="" or usuario=="" or contraseña=="" or confirmacion=="" or foto=="":
            return False
        return True    