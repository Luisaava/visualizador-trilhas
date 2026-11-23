from dominio.trilhas import Registro, Trilha
from dominio.usuarios import Usuario
from datetime import time
class SessaoIniciarPercursoIndividual:
    def iniciarPercurso(self, t:Trilha, h: time, u: Usuario) -> Registro | None:
        # Aqui poderia haver lógicas de validação (ex: clima, se a trilha está aberta)
        # Por enquanto, apenas inicia com sucesso.
        if u.percursoAtivo == None:
            r = self.criarRegistro(t,h)
            u.percursoAtivo = r
            return r
        else:
            return None
    def criarRegistro(self, t: Trilha, h: time):
        return Registro(t,h)