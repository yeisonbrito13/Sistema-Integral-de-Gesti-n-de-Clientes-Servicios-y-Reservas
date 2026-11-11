from abc import ABC, abstractmethod
from datetime import datetime


# REGISTRO DE EVENTOS Y ERRORES

def registrar(tipo, mensaje):
    archivo = open("registro.log", "a", encoding="utf-8")
    archivo.write(str(datetime.now()) + " - " + tipo + " - " + mensaje + "\n")
    archivo.close()


# ERRORES PERSONALIZADOS

class DatoInvalidoError(Exception):
    pass


class ReservaError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


# CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):

    def __init__(self, codigo):
        if codigo == "":
            raise DatoInvalidoError("Codigo vacio")
        self.codigo = codigo

    @abstractmethod
    def mostrar(self):
        pass
        
# CLASE CLIENTE 

class Cliente(Entidad):

    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo)

        if nombre == "":
            raise DatoInvalidoError("Nombre obligatorio")

        if "@" not in correo:
            raise DatoInvalidoError("Correo incorrecto")

        if len(telefono) < 7:
            raise DatoInvalidoError("Telefono incorrecto")

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

    def obtener_nombre(self):
        return self.__nombre

    def mostrar(self):
        print(self.codigo, self.__nombre, self.__correo)
        

    


