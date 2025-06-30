class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def __repr__(self):
        return f"{self.rol}: {self.nombre}"


class Paciente(Usuario):
    def __init__(self, nombre, id_paciente):
        super().__init__(nombre, "Paciente")
        self.id_paciente = id_paciente
        self.historial_clinico = []
        self.historial_psicologico = []

    def agregar_historial_clinico(self, nota):
        self.historial_clinico.append(nota)

    def agregar_historial_psicologico(self, nota):
        self.historial_psicologico.append(nota)


class Profesional(Usuario):
    def __init__(self, nombre, rol):
        super().__init__(nombre, rol)
        self.citas = []

    def agregar_cita(self, cita):
        self.citas.append(cita)


class Medico(Profesional):
    def __init__(self, nombre, id_medico):
        super().__init__(nombre, "Medico")
        self.id_medico = id_medico

    def registrar_diagnostico(self, paciente, diagnostico):
        nota = f"Diagnostico por {self.nombre}: {diagnostico}"
        paciente.agregar_historial_clinico(nota)


class Psicologo(Profesional):
    def __init__(self, nombre, id_psicologo):
        super().__init__(nombre, "Psicologo")
        self.id_psicologo = id_psicologo

    def registrar_sesion(self, paciente, observacion):
        nota = f"Sesion con {self.nombre}: {observacion}"
        paciente.agregar_historial_psicologico(nota)


class Administrador(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, "Administrador")


class Recepcion(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, "Recepcion")


class Cita:
    def __init__(self, paciente, profesional, fecha):
        self.paciente = paciente
        self.profesional = profesional
        self.fecha = fecha
        self.estado = "pendiente"

    def __repr__(self):
        return f"Cita con {self.profesional.nombre} para {self.paciente.nombre} el {self.fecha} - {self.estado}"


class Plataforma:
    def __init__(self):
        self.pacientes = {}
        self.profesionales = {}
        self.citas = []

    def registrar_paciente(self, nombre, id_paciente):
        paciente = Paciente(nombre, id_paciente)
        self.pacientes[id_paciente] = paciente
        return paciente

    def registrar_profesional(self, profesional):
        if isinstance(profesional, Profesional):
            self.profesionales[profesional.nombre] = profesional

    def agendar_cita(self, id_paciente, profesional_nombre, fecha):
        paciente = self.pacientes.get(id_paciente)
        profesional = self.profesionales.get(profesional_nombre)
        if paciente and profesional:
            cita = Cita(paciente, profesional, fecha)
            self.citas.append(cita)
            profesional.agregar_cita(cita)
            return cita
        raise ValueError("Paciente o profesional no encontrado")

    def obtener_historial_paciente(self, id_paciente):
        paciente = self.pacientes.get(id_paciente)
        if not paciente:
            raise ValueError("Paciente no encontrado")
        return {
            "clinico": paciente.historial_clinico,
            "psicologico": paciente.historial_psicologico,
        }

    def resumen_estadisticas(self):
        total_pacientes = len(self.pacientes)
        total_citas = len(self.citas)
        return {
            "total_pacientes": total_pacientes,
            "total_citas": total_citas,
        }


def demo():
    plataforma = Plataforma()
    p1 = plataforma.registrar_paciente("Juan", "P001")
    m1 = Medico("Dr. Rojas", "M001")
    plataforma.registrar_profesional(m1)
    c1 = plataforma.agendar_cita("P001", "Dr. Rojas", "2025-07-01")
    m1.registrar_diagnostico(p1, "Chequeo general")

    historial = plataforma.obtener_historial_paciente("P001")
    stats = plataforma.resumen_estadisticas()

    print(c1)
    print("Historial clinico:", historial["clinico"])
    print("Estadisticas:", stats)


if __name__ == "__main__":
    demo()
