from abc import ABC, abstractmethod
from datetime import datetime

# FUNCIONES PARA GUARDAR EVENTOS Y ERRORES  

def guardar_registro(tipo, mensaje):
    fecha = datetime.now()
    archivo = open("registro.log", "a", encoding="utf-8")
    archivo.write(str(fecha) + " - " + tipo + " - " + mensaje + "\n")
    archivo.close()

# EXCEPCIONES PERSONALIZADAS  

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
            raise DatoInvalidoError("El codigo no puede estar vacio.")
        self.codigo = codigo
    @abstractmethod
    def mostrar_informacion(self):
        pass


#CLASE CLIENTE 

class Cliente(Entidad):
    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo)
        if nombre == "":
            raise DatoInvalidoError("El nombre es obligatorio.")
        if "@" not in correo:
            raise DatoInvalidoError("El correo no es valido.")
        if len(telefono) < 7:
            raise DatoInvalidoError("El telefono debe tener minimo 7 digitos.")

  # DATOS PRIVADOS  (encapsulación)
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

    def obtener_nombre(self):
        return self.__nombre

    def obtener_correo(self):
        return self.__correo

    def mostrar_informacion(self):

        print("Codigo:", self.codigo)
        print("Nombre:", self.__nombre)
        print("Correo:", self.__correo)
        print("Telefono:", self.__telefono)


