# Sistema de Torneo de Videojuegos - Lista Circular Enlazada
# Universidad de Cundinamarca - Estructuras de Informacion
# CORREGIDO: El usuario debe registrar minimo 6 jugadores manualmente

class NodoJugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "Activo"
        self.turnos_jugados = 0
        self.siguiente = None

class ListaCircularTorneo:
    def __init__(self):
        self.cabeza = None
        self.total_jugadores = 0
    
    def registrar_jugador(self, nombre):
        if not nombre or nombre.strip() == "":
            print("Error: El nombre no puede estar vacio.")
            return False
        
        # Verificar que no exista duplicado
        if self.buscar_jugador_silencioso(nombre):
            print(f"Error: El jugador '{nombre}' ya esta registrado.")
            return False
        
        nuevo = NodoJugador(nombre.strip())
        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo
            nuevo.siguiente = self.cabeza
        
        self.total_jugadores += 1
        print(f"Jugador '{nombre}' registrado exitosamente.")
        return True
    
    def buscar_jugador_silencioso(self, nombre):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while True:
            if actual.nombre.lower() == nombre.lower().strip():
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None
    
    def mostrar_jugadores(self):
        if self.cabeza is None:
            print("No hay jugadores registrados.")
            return
        print("\n" + "="*50)
        print("LISTA DE JUGADORES REGISTRADOS")
        print("="*50)
        print(f"{'#':<3} {'Nombre':<20} {'Estado':<10} {'Turnos':<8}")
        print("-"*50)
        actual = self.cabeza
        contador = 1
        while True:
            print(f"{contador:<3} {actual.nombre:<20} {actual.estado:<10} {actual.turnos_jugados:<8}")
            actual = actual.siguiente
            contador += 1
            if actual == self.cabeza:
                break
        print("="*50)
        print(f"Total: {self.total_jugadores} jugadores")
    
    def buscar_jugador(self, nombre):
        if self.cabeza is None:
            print("No hay jugadores registrados.")
            return None
        actual = self.cabeza
        while True:
            if actual.nombre.lower() == nombre.lower().strip():
                print(f"Jugador encontrado: {actual.nombre} | Estado: {actual.estado} | Turnos: {actual.turnos_jugados}")
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        print(f"Jugador '{nombre}' no encontrado.")
        return None
    
    def eliminar_jugador(self, nombre):
        if self.cabeza is None:
            print("No hay jugadores registrados.")
            return
        
        # BLOQUEO: No eliminar si quedarian menos de 6
        if self.total_jugadores <= 6:
            print(f"Error: No se puede eliminar. Deben mantenerse minimo 6 jugadores (actual: {self.total_jugadores}).")
            return
        
        if self.cabeza.siguiente == self.cabeza:
            if self.cabeza.nombre.lower() == nombre.lower().strip():
                print(f"Jugador '{nombre}' eliminado.")
                self.cabeza = None
                self.total_jugadores -= 1
                self.mostrar_jugadores()
                return
            else:
                print(f"Jugador '{nombre}' no encontrado.")
                return
        
        actual = self.cabeza
        anterior = None
        encontrado = False
        
        while True:
            if actual.nombre.lower() == nombre.lower().strip():
                encontrado = True
                break
            anterior = actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        
        if not encontrado:
            print(f"Jugador '{nombre}' no encontrado.")
            return
        
        if actual == self.cabeza:
            ultimo = self.cabeza
            while ultimo.siguiente != self.cabeza:
                ultimo = ultimo.siguiente
            self.cabeza = actual.siguiente
            ultimo.siguiente = self.cabeza
        else:
            anterior.siguiente = actual.siguiente
        
        self.total_jugadores -= 1
        print(f"Jugador '{nombre}' eliminado exitosamente.")
        self.mostrar_jugadores()
    
    def pausar_jugador(self, nombre):
        jugador = self.buscar_jugador(nombre)
        if jugador:
            if jugador.estado == "Pausado":
                print(f"El jugador '{nombre}' ya esta pausado.")
            else:
                # BLOQUEO: No pausar si quedarian menos de 2 activos
                activos = self.contar_activos()
                if activos <= 2:
                    print(f"Error: No se puede pausar. Deben quedar minimo 2 jugadores activos (actual: {activos}).")
                    return
                jugador.estado = "Pausado"
                print(f"Jugador '{nombre}' pausado. No participara en los turnos.")
    
    def reactivar_jugador(self, nombre):
        jugador = self.buscar_jugador(nombre)
        if jugador:
            if jugador.estado == "Activo":
                print(f"El jugador '{nombre}' ya esta activo.")
            else:
                jugador.estado = "Activo"
                print(f"Jugador '{nombre}' reactivado. Vuelve a participar.")
    
    def simular_turnos(self, cantidad_turnos=10):
        if self.cabeza is None:
            print("No hay jugadores registrados.")
            return
        
        # VALIDACION: Minimo 6 jugadores para simular
        if self.total_jugadores < 6:
            print(f"Error: Se requieren minimo 6 jugadores registrados (actual: {self.total_jugadores}).")
            return
        
        activos = self.contar_activos()
        if activos == 0:
            print("No hay jugadores activos para simular turnos.")
            return
        
        if activos == 1:
            print("Solo queda un jugador activo! El torneo ha terminado.")
            self.mostrar_ganador()
            return
        
        print(f"\nINICIANDO SIMULACION DE {cantidad_turnos} TURNOS")
        print("="*50)
        
        actual = self.cabeza
        turno_actual = 1
        
        while turno_actual <= cantidad_turnos:
            if actual.estado == "Pausado":
                actual = actual.siguiente
                continue
            
            print(f"\nTurno #{turno_actual}")
            print(f"   Jugador actual: {actual.nombre}")
            actual.turnos_jugados += 1
            print(f"   Turnos jugados por {actual.nombre}: {actual.turnos_jugados}")
            
            if self.contar_activos() == 1:
                print("\n" + "="*50)
                print("SOLO QUEDA UN JUGADOR ACTIVO!")
                self.mostrar_ganador()
                return
            
            actual = actual.siguiente
            turno_actual += 1
        
        print("\n" + "="*50)
        print(f"Simulacion completada: {cantidad_turnos} turnos realizados.")
    
    def mostrar_estadisticas(self):
        if self.cabeza is None:
            print("No hay jugadores registrados.")
            return
        
        total = self.total_jugadores
        activos = self.contar_activos()
        pausados = self.contar_pausados()
        
        jugador_top = self.cabeza
        max_turnos = self.cabeza.turnos_jugados
        
        actual = self.cabeza.siguiente
        while actual != self.cabeza:
            if actual.turnos_jugados > max_turnos:
                max_turnos = actual.turnos_jugados
                jugador_top = actual
            actual = actual.siguiente
        
        print("\n" + "="*50)
        print("ESTADISTICAS DEL TORNEO")
        print("="*50)
        print(f"Total de jugadores registrados: {total}")
        print(f"Jugadores activos: {activos}")
        print(f"Jugadores pausados: {pausados}")
        print(f"Jugador con mas turnos: {jugador_top.nombre} ({max_turnos} turnos)")
        print("="*50)
    
    def contar_activos(self):
        if self.cabeza is None:
            return 0
        contador = 0
        actual = self.cabeza
        while True:
            if actual.estado == "Activo":
                contador += 1
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return contador
    
    def contar_pausados(self):
        if self.cabeza is None:
            return 0
        contador = 0
        actual = self.cabeza
        while True:
            if actual.estado == "Pausado":
                contador += 1
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return contador
    
    def mostrar_ganador(self):
        if self.cabeza is None:
            print("No hay jugadores registrados.")
            return
        
        activos = self.contar_activos()
        
        if activos != 1:
            print(f"Aun hay {activos} jugadores activos. El torneo continua.")
            return
        
        actual = self.cabeza
        while True:
            if actual.estado == "Activo":
                print("\n" + "="*50)
                print("GANADOR DEL TORNEO")
                print("="*50)
                print(f"{actual.nombre}")
                print(f"Turnos totales jugados: {actual.turnos_jugados}")
                print("="*50)
                return
            actual = actual.siguiente
            if actual == self.cabeza:
                break


def menu_principal():
    torneo = ListaCircularTorneo()
    
    print("="*60)
    print("SISTEMA DE TORNEO DE VIDEOJUEGOS")
    print("Lista Circular - Estructuras de Informacion")
    print("="*60)
    
    # FASE 1: REGISTRO OBLIGATORIO DE MINIMO 6 JUGADORES
    print("\n>>> FASE DE REGISTRO: Se requieren minimo 6 jugadores <<<")
    
    while torneo.total_jugadores < 6:
        print(f"\nJugadores actuales: {torneo.total_jugadores}/6")
        nombre = input(f"Ingrese nombre del jugador #{torneo.total_jugadores + 1}: ")
        torneo.registrar_jugador(nombre)
    
    print(f"\n✓ Registro completo: {torneo.total_jugadores} jugadores registrados.")
    torneo.mostrar_jugadores()
    
    # FASE 2: MENU PRINCIPAL
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print(f"Jugadores: {torneo.total_jugadores} | Activos: {torneo.contar_activos()} | Pausados: {torneo.contar_pausados()}")
        print("-"*60)
        print("1. Registrar nuevo jugador")
        print("2. Mostrar jugadores registrados")
        print("3. Buscar jugador")
        print("4. Eliminar jugador")
        print("5. Pausar jugador")
        print("6. Reactivar jugador")
        print("7. Simular turnos automaticos")
        print("8. Mostrar estadisticas")
        print("9. Verificar ganador")
        print("0. Salir")
        print("="*60)
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            nombre = input("Ingrese nombre del jugador: ")
            torneo.registrar_jugador(nombre)
        
        elif opcion == "2":
            torneo.mostrar_jugadores()
        
        elif opcion == "3":
            nombre = input("Ingrese nombre a buscar: ")
            torneo.buscar_jugador(nombre)
        
        elif opcion == "4":
            nombre = input("Ingrese nombre a eliminar: ")
            torneo.eliminar_jugador(nombre)
        
        elif opcion == "5":
            nombre = input("Ingrese nombre a pausar: ")
            torneo.pausar_jugador(nombre)
        
        elif opcion == "6":
            nombre = input("Ingrese nombre a reactivar: ")
            torneo.reactivar_jugador(nombre)
        
        elif opcion == "7":
            if torneo.total_jugadores < 6:
                print(f"Error: Se requieren minimo 6 jugadores (actual: {torneo.total_jugadores}).")
                continue
            cantidad = input("Ingrese cantidad de turnos a simular (default 10): ")
            cantidad = int(cantidad) if cantidad.isdigit() else 10
            torneo.simular_turnos(cantidad)
        
        elif opcion == "8":
            torneo.mostrar_estadisticas()
        
        elif opcion == "9":
            torneo.mostrar_ganador()
        
        elif opcion == "0":
            print("Gracias por usar el sistema de torneo!")
            break
        
        else:
            print("Opcion no valida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()