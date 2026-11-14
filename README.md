
from abc import ABC, abstractmethod
from datetime import datetime


# MOSTRAR DINERO EN PESOS

def pesos(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


# GUARDAR EVENTOS Y ERRORES

def registrar(tipo, mensaje):
    with open("registro.log", "a", encoding="utf-8") as archivo:
        archivo.write(str(datetime.now()) + " - " + tipo + " - " + mensaje + "\n")


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
            raise DatoInvalidoError("Codigo obligatorio")
        self.codigo = codigo

    @abstractmethod
    def mostrar(self):
        pass


# CLASE CLIENTE

class Cliente(Entidad):

    def __init__(self, codigo, nombre, correo, celular):
        super().__init__(codigo)

        if nombre.strip() == "":
            raise DatoInvalidoError("Nombre obligatorio")

        if "@" not in correo or "." not in correo:
            raise DatoInvalidoError("Correo incorrecto")

        if not celular.isdigit() or len(celular) != 10:
            raise DatoInvalidoError("Celular debe tener 10 digitos")

        self.__nombre = nombre
        self.__correo = correo
        self.__celular = celular

    def obtener_nombre(self):
        return self.__nombre

    def mostrar(self):
        print("Codigo:", self.codigo)
        print("Nombre:", self.__nombre)
        print("Correo:", self.__correo)
        print("Celular:", self.__celular)


# REGISTRO DE CLIENTE

def registrar_cliente(codigo):

    print("\nREGISTRO DE CLIENTE")

    while True:
        nombre = input("Ingrese su nombre: ").strip()

        if nombre == "":
            print("ERROR: Nombre obligatorio")
            registrar("ERROR", "Nombre vacio")
        else:
            break

    while True:
        correo = input("Ingrese su correo: ").strip()

        if "@" not in correo or "." not in correo:
            print("ERROR: Correo incorrecto")
            registrar("ERROR", "Correo incorrecto")
        else:
            break

    while True:
        celular = input("Ingrese su celular (10 digitos): ").strip()

        if not celular.isdigit() or len(celular) != 10:
            print("ERROR: El celular debe tener 10 digitos")
            registrar("ERROR", "Celular incorrecto")
        else:
            break

    cliente = Cliente(codigo, nombre, correo, celular)

    print("Cliente registrado correctamente")
    registrar("EVENTO", "Cliente registrado: " + nombre)

    return cliente


# CLASE ABSTRACTA SERVICIO

class Servicio(Entidad):

    def __init__(self, codigo, nombre, precio, disponible=True):
        super().__init__(codigo)

        if nombre.strip() == "":
            raise DatoInvalidoError("Nombre de servicio obligatorio")

        if precio <= 0:
            raise DatoInvalidoError("Precio incorrecto")

        self.nombre = nombre
        self.precio = precio
        self.disponible = disponible

    def mostrar(self):
        print(self.codigo, "-", self.nombre)
        print("Precio por hora:", pesos(self.precio))

    # PARAMETROS OPCIONALES PARA CALCULAR COSTOS

    def calcular_total(self, horas, impuesto=0, descuento=0):

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatoInvalidoError("Horas incorrectas")

        if not 0 <= impuesto <= 100:
            raise DatoInvalidoError("Impuesto incorrecto")

        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("Descuento incorrecto")

        subtotal = self.precio * horas
        valor_impuesto = subtotal * impuesto / 100
        valor_descuento = subtotal * descuento / 100

        total = subtotal + valor_impuesto - valor_descuento

        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass


# SERVICIO DE SALAS

class ServicioSala(Servicio):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.calcular_total(horas, impuesto, descuento)

    def describir(self):
        return "Reserva de salas"


# SERVICIO DE EQUIPOS

class ServicioEquipo(Servicio):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.calcular_total(horas, impuesto, descuento)

    def describir(self):
        return "Alquiler de equipos"


# SERVICIO DE ASESORIAS

class ServicioAsesoria(Servicio):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.calcular_total(horas, impuesto, descuento)

    def describir(self):
        return "Asesorias especializadas"


# CLASE RESERVA

class Reserva:

    def __init__(self, codigo, cliente, servicio, horas,
                 impuesto=0, descuento=0):

        if codigo == "":
            raise DatoInvalidoError("Codigo obligatorio")

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Cliente incorrecto")

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio incorrecto")

        servicio.calcular_costo(horas, impuesto, descuento)

        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.impuesto = impuesto
        self.descuento = descuento
        self.estado = "Pendiente"
        self.total = 0

    def confirmar(self):

        if self.estado != "Pendiente":
            raise ReservaError("Reserva no pendiente")

        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("Servicio ocupado")

        self.total = self.servicio.calcular_costo(
            self.horas, self.impuesto, self.descuento
        )

        self.estado = "Confirmada"

    def cancelar(self):

        if self.estado == "Cancelada":
            raise ReservaError("Reserva ya cancelada")

        self.estado = "Cancelada"

    def procesar(self):

        try:
            self.confirmar()
            print("\nReserva confirmada")
            print("Total a pagar:", pesos(self.total))

        except Exception as error:
            registrar("ERROR", str(error))
            raise ReservaError("Error al procesar reserva") from error

        finally:
            registrar("EVENTO", "Procesamiento de " + self.codigo)

    def mostrar(self):
        print("Reserva:", self.codigo)
        print("Cliente:", self.cliente.obtener_nombre())
        print("Servicio:", self.servicio.nombre)
        print("Horas:", self.horas)
        print("Impuesto:", str(self.impuesto) + "%")
        print("Descuento:", str(self.descuento) + "%")
        print("Estado:", self.estado)
        print("Total:", pesos(self.total))


# MENU DE SERVICIOS

def elegir_servicio(servicios):

    while True:

        print("\n========== MENU DE SERVICIOS ==========")

        for i in range(len(servicios)):
            print(
                str(i + 1) + ".",
                servicios[i].nombre,
                "-",
                pesos(servicios[i].precio),
                "por hora"
            )

        print("4. Cancelar servicio y salir")

        opcion = input("Seleccione una opcion (1-4): ").strip()

        if opcion in ("1", "2", "3"):
            servicio = servicios[int(opcion) - 1]
            print("Servicio elegido:", servicio.nombre)
            return servicio

        elif opcion == "4":
            print("Seleccion cancelada")
            registrar("EVENTO", "Seleccion cancelada")
            return None

        else:
            print("ERROR: Seleccione una opcion del 1 al 4")
            registrar("ERROR", "Opcion incorrecta")


# PEDIR HORAS

def pedir_horas():

    while True:

        try:
            horas = int(input("Cuantas horas necesita?: "))

            if horas <= 0:
                raise DatoInvalidoError("Las horas deben ser mayores a cero")

        except ValueError:
            print("ERROR: Ingrese un numero entero")
            registrar("ERROR", "Horas no numericas")

        except DatoInvalidoError as error:
            print("ERROR:", error)
            registrar("ERROR", str(error))

        else:
            return horas


# MENU PARA CALCULAR COSTOS

def elegir_calculo(servicio, horas):

    while True:

        print("\n========== CALCULO DEL SERVICIO ==========")
        print("1. Costo normal")
        print("2. Costo con impuesto del 19%")
        print("3. Costo con impuesto del 19% y descuento del 10%")
        print("4. Cancelar seleccion del calculo")

        opcion = input("Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            impuesto = 0
            descuento = 0
            total = servicio.calcular_costo(horas)
            break

        elif opcion == "2":
            impuesto = 19
            descuento = 0
            total = servicio.calcular_costo(horas, impuesto)
            break

        elif opcion == "3":
            impuesto = 19
            descuento = 10
            total = servicio.calcular_costo(
                horas, impuesto, descuento
            )
            break

        elif opcion == "4":
            print("Calculo cancelado")
            registrar("EVENTO", "Calculo cancelado")
            return None

        else:
            print("ERROR: Opcion incorrecta")
            registrar("ERROR", "Opcion de calculo incorrecta")

    print("\nSubtotal:", pesos(servicio.precio * horas))
    print("Impuesto:", str(impuesto) + "%")
    print("Descuento:", str(descuento) + "%")
    print("TOTAL:", pesos(total))

    return impuesto, descuento, total


# PEDIR CONFIRMACION

def pedir_confirmacion(mensaje):

    while True:
        respuesta = input(mensaje).strip().upper()

        if respuesta == "S" or respuesta == "N":
            return respuesta

        print("ERROR: Responda S o N")
        registrar("ERROR", "Respuesta incorrecta")


# PROGRAMA PRINCIPAL

clientes = []
servicios = []
reservas = []

print("=====================================")
print(" SISTEMA DE GESTION SOFTWARE FJ")
print("=====================================")


# OPERACION 1: REGISTRAR CLIENTE

print("\nOPERACION 1: REGISTRAR CLIENTE")

cliente1 = registrar_cliente("C01")
clientes.append(cliente1)


# OPERACION 2: CLIENTE INCORRECTO

print("\nOPERACION 2: VALIDAR CLIENTE INCORRECTO")

try:
    malo = Cliente("C02", "Pedro", "pedrogmail.com", "3001234567")
    clientes.append(malo)

except Exception as error:
    print("Error controlado:", error)
    registrar("ERROR", str(error))


# OPERACION 3: OTRO CLIENTE

print("\nOPERACION 3: REGISTRAR OTRO CLIENTE")

try:
    cliente2 = Cliente(
        "C03", "Andres", "andres@gmail.com", "3107654321"
    )
    clientes.append(cliente2)
    print("Cliente Andres registrado")
    registrar("EVENTO", "Cliente Andres registrado")

except Exception as error:
    print("Error:", error)
    registrar("ERROR", str(error))


# OPERACIONES 4, 5 Y 6: CREAR SERVICIOS

print("\nOPERACIONES 4, 5 Y 6: CREAR SERVICIOS")

servicios_nuevos = [
    ServicioSala("S01", "Reserva de sala", 50000),
    ServicioEquipo("S02", "Alquiler de equipo", 30000),
    ServicioAsesoria("S03", "Asesoria especializada", 80000)
]

for servicio in servicios_nuevos:
    try:
        servicios.append(servicio)
        print("Servicio creado:", servicio.nombre)
        registrar("EVENTO", "Servicio creado: " + servicio.nombre)

    except Exception as error:
        print("Error:", error)
        registrar("ERROR", str(error))


# OPERACION 7: PRECIO INCORRECTO

print("\nOPERACION 7: VALIDAR PRECIO INCORRECTO")

try:
    malo = ServicioSala("S04", "Sala", -20000)
    servicios.append(malo)

except Exception as error:
    print("Error controlado:", error)
    registrar("ERROR", str(error))


# OPERACION 8: RESERVA DEL USUARIO

print("\nOPERACION 8: REALIZAR RESERVA")

reserva1 = None

servicio_elegido = elegir_servicio(servicios)

if servicio_elegido is not None:

    horas = pedir_horas()

    calculo = elegir_calculo(servicio_elegido, horas)

    if calculo is not None:

        impuesto, descuento, total = calculo

        print("\n========== RESUMEN DEL SERVICIO ==========")
        print("Cliente:", cliente1.obtener_nombre())
        print("Servicio:", servicio_elegido.nombre)
        print("Precio por hora:", pesos(servicio_elegido.precio))
        print("Horas:", horas)
        print("Total a pagar:", pesos(total))

        respuesta = pedir_confirmacion(
            "\nDesea confirmar la reserva? (S/N): "
        )

        try:
            reserva1 = Reserva(
                "R01", cliente1, servicio_elegido,
                horas, impuesto, descuento
            )
            reservas.append(reserva1)

            if respuesta == "S":
                reserva1.procesar()
                registrar("EVENTO", "Reserva confirmada")

            else:
                reserva1.cancelar()
                print("Reserva cancelada")
                registrar("EVENTO", "Reserva cancelada")

        except Exception as error:
            print("Error:", error)
            registrar("ERROR", str(error))

        # CANCELAR UNA RESERVA CONFIRMADA

        if reserva1 is not None and reserva1.estado == "Confirmada":

            print("\n========== OPCIONES DE RESERVA ==========")
            print("1. Mantener reserva")
            print("2. Cancelar reserva")

            while True:
                opcion = input("Seleccione una opcion (1-2): ").strip()

                if opcion == "1":
                    print("Su reserva sigue confirmada")
                    break

                elif opcion == "2":
                    try:
                        reserva1.cancelar()
                        print("Reserva cancelada correctamente")
                        registrar("EVENTO", "Reserva cancelada")
                    except Exception as error:
                        print("Error:", error)
                        registrar("ERROR", str(error))
                    break

                else:
                    print("ERROR: Seleccione 1 o 2")
                    registrar("ERROR", "Opcion incorrecta")

    else:
        print("No se realizo ninguna reserva")

else:
    print("No se selecciono ningun servicio")


# OPERACION 9: SERVICIO NO DISPONIBLE

print("\nOPERACION 9: PROBAR SERVICIO OCUPADO")

try:
    ocupado = ServicioEquipo(
        "S05", "Proyector ocupado", 30000, False
    )

    reserva2 = Reserva("R02", cliente2, ocupado, 2)
    reservas.append(reserva2)
    reserva2.procesar()

except Exception as error:
    print("Error controlado:", error)
    registrar("ERROR", str(error))


# OPERACION 10: CANCELAR RESERVA DE PRUEBA

print("\nOPERACION 10: CANCELAR RESERVA DE PRUEBA")

try:
    reserva2.cancelar()
    print("Reserva de prueba cancelada")
    registrar("EVENTO", "Reserva R02 cancelada")

except Exception as error:
    print("Error:", error)
    registrar("ERROR", str(error))


# OPERACION 11: CANCELAR DOS VECES

print("\nOPERACION 11: CANCELAR DOS VECES")

try:
    reserva2.cancelar()

except Exception as error:
    print("Error controlado:", error)
    registrar("ERROR", str(error))


# OPERACION 12: DEMOSTRAR PARAMETROS OPCIONALES

print("\nOPERACION 12: DIFERENTES CALCULOS DE COSTO")

try:
    sala = servicios[0]

    normal = sala.calcular_costo(2)
    con_impuesto = sala.calcular_costo(2, 19)
    con_descuento = sala.calcular_costo(2, 19, 10)

    print("Costo normal:", pesos(normal))
    print("Costo con impuesto:", pesos(con_impuesto))
    print("Costo con impuesto y descuento:", pesos(con_descuento))

    registrar("EVENTO", "Tres variantes del calculo ejecutadas")

except Exception as error:
    print("Error:", error)
    registrar("ERROR", str(error))


# RESUMEN FINAL

print("\n=====================================")
print("             RESUMEN FINAL")
print("=====================================")

print("\nCLIENTES REGISTRADOS")

for cliente in clientes:
    cliente.mostrar()
    print("------------------------")


print("\nSERVICIOS")

for servicio in servicios:
    servicio.mostrar()
    print("Descripcion:", servicio.describir())
    print("------------------------")


print("\nRESERVAS")

if len(reservas) == 0:
    print("No hay reservas")

for reserva in reservas:
    reserva.mostrar()
    print("------------------------")


print("\nPROGRAMA FINALIZADO")



