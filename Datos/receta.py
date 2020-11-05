class Receta:
    def __init__(self,index, autor, titulo, resumen,ingredientes,procedimiento,tiempo,imagen,comentarios):
        self.index = index
        self.autor = autor
        self.titulo = titulo
        self.resumen = resumen
        self.ingredientes = ingredientes
        self.procedimiento = procedimiento
        self.tiempo = tiempo
        self.imagen=imagen
        self.comentarios=comentarios