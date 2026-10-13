from dominio.trilhas import Registro

class SessaoInicioPercurso:
    def iniciarPercurso(self, r: Registro) -> tuple[bool, str, Registro]:
        # Aqui poderia haver lógicas de validação (ex: clima, se a trilha está aberta)
        # Por enquanto, apenas inicia com sucesso.
        return True, "Percurso iniciado com sucesso!", r