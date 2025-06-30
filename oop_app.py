class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludo(self):
        return f"Hola, soy {self.nombre} y tengo {self.edad} a\u00f1os."


class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self.carrera = carrera

    def descripcion(self):
        return f"Soy estudiante de {self.carrera}."


class Profesor(Persona):
    def __init__(self, nombre, edad, materia):
        super().__init__(nombre, edad)
        self.materia = materia

    def descripcion(self):
        return f"Ense\u00f1o la materia de {self.materia}."


def main():
    estudiante = Estudiante("Ana", 20, "Ingenier\u00eda")
    profesor = Profesor("Dr. Smith", 45, "Matem\u00e1ticas")

    print(estudiante.saludo(), estudiante.descripcion())
    print(profesor.saludo(), profesor.descripcion())


if __name__ == "__main__":
    main()
