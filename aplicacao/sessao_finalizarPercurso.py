from dominio.trilhas import Registro
from datetime import time

class SessaoFinalizarPercurso:
    def finalizarPercurso(self, r: Registro, duracao: time, nota: float) -> tuple[bool, str]:
        r.duracao = duracao
        r.nota = nota
        
        # adiciona registro a lista de trilhas concluidas do usuario
        r.usuario.trilhasConcluidas.append(r)
        
        return True, "Percurso finalizado e registrado com sucesso!"