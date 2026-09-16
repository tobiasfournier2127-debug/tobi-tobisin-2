"""
Trabajo Práctico N° 3: Operación CREATE Avanzada y POO
Materia: Programación 1 - ESC. 4-130 TÉCNICA EN PROGRAMACIÓN "Jorge de la Reta"
Profesor: Cristian Carrió
Curso: 4° 3°

================================================================================
SECCIÓN 2: VERDADERO O FALSO (TEORÍA)
================================================================================
1. [FALSO]
   En Python no existen modificadores de acceso estrictamente privados ni se requiere 
   de librerías externas como 'private_mode'. Se utiliza una convención de nombres:
   un guion bajo (_atributo) para indicar que es protegido, y doble guion bajo (__atributo)
   para activar Name Mangling y dificultar el acceso externo desde fuera de la clase.

2. [VERDADERO]
   El método __init__ actúa como el constructor/inicializador del objeto, donde se definen
   los atributos iniciales e instancian los valores en memoria RAM al crear un objeto.

3. [FALSO]
   La herencia permite reocupar código, pero las clases hijas (subclases) pueden extender
   y agregar nuevos atributos y métodos propios, además de sobrescribir (override) los
   existentes en la clase padre.

4. [VERDADERO]
   El polimorfismo permite que objetos de distintas clases respondan al mismo llamado
   de interfaz (método con el mismo nombre) ejecutando lógica interna específica de cada una.
================================================================================
"""

from abc import ABC, abstractmethod


# ==============================================================================
# SECCIÓN 3: PRÁCTICA - EJERCICIO 1: Abstracción, Herencia y Encapsulamiento
# ==============================================================================

class Persona(ABC):
    """
    Clase abstracta base que representa a una persona en el sistema.
    Aplica encapsulamiento protegiendo sus atributos con guion bajo (_).
    """
    def __init__(self, nombre: str, apellido: str, dni: str):
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni

    # Getters
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def dni(self) -> str:
        return self._dni


class Alumno(Persona):
    """
    Clase Alumno que hereda de Persona.
    Añade atributos específicos encapsulados: _curso y _promedio.
    """
    def __init__(self, nombre: str, apellido: str, dni: str, curso: str, promedio: float):
        super().__init__(nombre, apellido, dni)
        self._curso = curso
        self._promedio = promedio

    # Getters específicos
    @property
    def curso(self) -> str:
        return self._curso

    @property
    def promedio(self) -> float:
        return self._promedio

    def obtener_informacion(self) -> str:
        """Devuelve una representación formateada de los datos del alumno."""
        return (f"Alumno: {self.apellido}, {self.nombre} | "
                f"DNI: {self.dni} | Curso: {self.curso} | Promedio: {self.promedio}")


# ==============================================================================
# SECCIÓN 3: PRÁCTICA - EJERCICIO 3: Polimorfismo y Estrategias de Persistencia
# ==============================================================================

class EstrategiaGuardado(ABC):
    """
    Clase base abstracta (Interfaz) para implementar las estrategias de guardado.
    Demuestra polimorfismo mediante el método abstracto 'guardar'.
    """
    @abstractmethod
    def guardar(self, datos: str) -> bool:
        pass


class GuardadoMemoria(EstrategiaGuardado):
    """Estrategia que simula la persistencia guardando los datos en la memoria RAM."""
    def guardar(self, datos: str) -> bool:
        print(f"[MEMORIA RAM] Datos guardados temporalmente: {datos}")
        return True


class GuardadoArchivoTXT(EstrategiaGuardado):
    """Estrategia que persiste los datos en un archivo físico de texto plano (.txt)."""
    def __init__(self, nombre_archivo: str = "registro_alumnos.txt"):
        self._nombre_archivo = nombre_archivo

    def guardar(self, datos: str) -> bool:
        try:
            with open(self._nombre_archivo, "a", encoding="utf-8") as file:
                file.write(datos + "\n")
            print(f"[ARCHIVO TXT] Guardado exitosamente en '{self._nombre_archivo}'.")
            return True
        except Exception as e:
            print(f"[ERROR TXT] No se pudo escribir en el archivo: {e}")
            return False


# ==============================================================================
# SECCIÓN 3: PRÁCTICA - EJERCICIO 2 Y 3: El Gestor y la Operación CREATE Segura
# ==============================================================================

class GestorAcademico:
    """
    Gestor encargado de la administración de alumnos y de la operación CREATE.
    Aplica Inyección de Dependencias al recibir la estrategia de guardado en el __init__.
    """
    def __init__(self, estrategia_guardado: EstrategiaGuardado):
        self._base_datos_alumnos: list[Alumno] = []
        self._estrategia_guardado = estrategia_guardado  # Inyección de dependencia

    def existe_alumno(self, dni: str) -> bool:
        """Verifica si ya existe un alumno registrado con el mismo DNI."""
        for alumno in self._base_datos_alumnos:
            if alumno.dni == dni:
                return True
        return False

    def registrar_nuevo_alumno(self, alumno: Alumno) -> bool:
        """
        Operación CREATE segura.
        Valida que el DNI no esté duplicado antes de agregar y guardar al alumno.
        """
        print(f"\n--- Intentando registrar alumno: {alumno.nombre} {alumno.apellido} (DNI: {alumno.dni}) ---")
        
        # Regla de negocio crítica: Validación de duplicados
        if self.existe_alumno(alumno.dni):
            print(f"  [ALERTA DE SEGURIDAD] Operación CREATE rechazada: El DNI {alumno.dni} ya se encuentra registrado.")
            return False

        # Si supera la validación, agregamos a la base de datos local
        self._base_datos_alumnos.append(alumno)
        
        # Delegación del guardado a la estrategia configurada (Polimorfismo)
        info_alumno = alumno.obtener_informacion()
        self._estrategia_guardado.guardar(info_alumno)
        print(f"  [ÉXITO] Operación CREATE realizada correctamente.")
        return True

    def listar_alumnos(self):
        """Muestra en consola todos los alumnos registrados en el gestor."""
        print("\n================ LISTADO ACTUAL DE ALUMNOS ================")
        if not self._base_datos_alumnos:
            print("No hay alumnos registrados.")
            return
        for i, alumno in enumerate(self._base_datos_alumnos, 1):
            print(f"{i}. {alumno.obtener_informacion()}")
        print("==========================================================")


# ==============================================================================
# PRUEBAS Y EJECUCIÓN DEL SISTEMA
# ==============================================================================

if __name__ == "__main__":
    print("==========================================================")
    print("     SISTEMA ACADÉMICO DE MATRICULACIÓN - POO Y CREATE     ")
    print("==========================================================")

    # 1. Demostración Ejercicio 1: Instanciación e impresión vía getters
    alumno_test = Alumno("Juan", "Pérez", "45123456", "4° 3°", 8.75)
    print("\n[Prueba Ejercicio 1] Objeto instanciado correctamente:")
    print(f"Nombre completo: {alumno_test.nombre} {alumno_test.apellido}")
    print(f"DNI: {alumno_test.dni} | Curso: {alumno_test.curso} | Promedio: {alumno_test.promedio}")

    # 2. Prueba de Inyección de Dependencias y Polimorfismo con GuardadoMemoria
    print("\n----------------------------------------------------------")
    print("PRUEBA 1: Gestor con Estrategia GuardadoMemoria")
    estrategia_memoria = GuardadoMemoria()
    gestor_memoria = GestorAcademico(estrategia_guardado=estrategia_memoria)

    a1 = Alumno("María", "Gómez", "44111222", "4° 3°", 9.50)
    a2 = Alumno("Carlos", "López", "43222333", "4° 3°", 7.20)
    a3_duplicado = Alumno("Carlos", "Repetido", "43222333", "4° 1°", 6.00)

    gestor_memoria.registrar_nuevo_alumno(a1)
    gestor_memoria.registrar_nuevo_alumno(a2)
    gestor_memoria.registrar_nuevo_alumno(a3_duplicado)  # Debe rebotar por DNI duplicado

    # 3. Prueba con GuardadoArchivoTXT (Persistencia Real)
    print("\n----------------------------------------------------------")
    print("PRUEBA 2: Gestor con Estrategia GuardadoArchivoTXT")
    estrategia_txt = GuardadoArchivoTXT("registro_alumnos.txt")
    gestor_txt = GestorAcademico(estrategia_guardado=estrategia_txt)

    a4 = Alumno("Lucía", "Fernández", "45999888", "4° 3°", 9.10)
    a5 = Alumno("Mateo", "Díaz", "46123987", "4° 3°", 8.40)
    a6_duplicado = Alumno("Lucía", "Clon", "45999888", "4° 2°", 5.00)

    gestor_txt.registrar_nuevo_alumno(a4)
    gestor_txt.registrar_nuevo_alumno(a5)
    gestor_txt.registrar_nuevo_alumno(a6_duplicado)  # Debe rebotar por DNI duplicado

    # Mostrar listado final
    gestor_txt.listar_alumnos()