def calcular_total(self, horas, impuesto=0, descuento=0):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatoInvalidoError("Horas incorrectas")
        if not 0 <= impuesto <= 100:
            raise DatoInvalidoError("Impuesto incorrecto")
        
        # aplicacion descuentos
        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("Descuento incorrecto")

        subtotal = self.precio * horas
        
        # descuento por cantidad horas mayor a 5hrs 5%
        descuento_por_volumen = 5 if horas >= 5 else 0
        descuento_total_porcentaje = min(100, descuento + descuento_por_volumen)

        valor_impuesto = subtotal * (impuesto / 100)
        valor_descuento = subtotal * (descuento_total_porcentaje / 100)

        total = subtotal + valor_impuesto - valor_descuento
        return round(total, 2)
# ====================================================================================================

class ReservaSalas(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        # descuento especial para categoria salas (añade un 2% adicional base)
        return self.calcular_total(horas, impuesto, descuento + 2)

    def describir(self):
        return "Reserva de salas"

class AlquilerEquipos(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        # mantener el descuento obtenido 
        return self.calcular_total(horas, impuesto, descuento)

    def describir(self):
        return "Alquiler de equipos"

#===============================================================================================================

# menu de descuentos 
print("\n========== CALCULO DEL SERVICIO ==========")
    print("1. Costo normal (Sin impuestos ni descuentos)")
    print("2. Costo con impuesto del 19%")
    print("3. Costo con impuesto del 19% y descuento del 10%") # <-- Opción de descuento
    print("4. Cancelar selección del calculo")

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
        descuento = 10  # <--- Asignación del descuento seleccionado
        total = servicio.calcular_costo(horas, impuesto, descuento)
        break